import streamlit as st
import openai
from io import StringIO
import pdfplumber
# from gtts import gTTS
# import pygame
import re
import time

# Insira sua chave de API aqui
openai.api_key = st.secrets['api_key_openai']

with st.sidebar:
    st.header('Usage guidance')
    st.write('1 - Upload an TXT or PDF file to be treated. Or paste a text in the indicated box. The limit is 4000 characters.')
    st.write('2 - Choose the tab desired and press the button to perform the action.')
    st.write('3 - The final text will be in the same language as the original.')
    st.write('4 - Use the parameters below to change responses.')
    
    st.header('Parameters')
    
    # TODO discover why in Streamlit (server) it does not work
    # read_text = st.radio(
    #     "Read text after executed?",
    #     ('Yes', 'No'), 1)
    # st.markdown("""---""")
    
    temperature = st.slider('Temperature', 0, 100, 50, 1)/100
    st.write('Temperature for action. Smaller values are more accurate, larger values are riskier.')
    st.markdown("""---""")
    
    max_tokens = st.slider('Limit words', 10, 4000, 1000, 100)
    st.write('Limit of words for the response.')
    
    st.header('About')
    st.write('Details about this project can be found in: https://github.com/htsnet/StreamlitChatgpt')
    
    
def revise_text(text, acao, max_tokens, temperature):
    with st.spinner('Wait for it...'):
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=acao + '"' + text + ' "' + ", mantenha a língua na do texto tratado",
            # max_tokens=max_tokens-len(text), # to not pass the limit of 4097 tokens for this engine
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )

    message = completions.choices[0].text
    # print(message)
    with st.spinner('Just one more minute...'):
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt='qual é a língua do texto a seguir, em apenas uma palavra: "' + message,
        )
    # define language
    language = completions.choices[0].text.upper()
    # st.write(language)
    # print(language)
    if re.search("PORT", language):
        sigla_language = 'pt'
    elif re.search("NGL", language):
        sigla_language = 'en'
    else:
        sigla_language = 'en'
    return message, sigla_language

def check_text(text):
    if text:
        return True
    st.info('The text field is empty!', icon="⚠️")
    return False

# def readText(text, language) :
#     print(read_text)
#     print(language)
#     if read_text == "Yes":
#         with st.spinner('Sit back and enjoy the speech ...'):
#             # initialize pygame
#             pygame.init()
#             # generate MP3
#             tts = gTTS(text, lang=language)
#             tts.save("text.mp3")
#             # convert and load MP3
#             time.sleep(10)
#             pygame.mixer.music.load("text.mp3")
#             # play MP3
#             pygame.mixer.music.play()
#             # wait finish
#             while pygame.mixer.music.get_busy():
#                 pygame.time.Clock().tick(10)
#             # quit pygame
#             pygame.quit()

# título
Title = f'Analysis and Improvement of Texts with AI (ChatGPT)'
st.title(Title)

#colunas
col1, col2 = st.columns([0.3, 0.7])

text_base = ''

with col1:
    uploaded_file = st.file_uploader("Choose a file to upload",  type=['txt', 'pdf'], help="Only txt/pdf file.")
    if uploaded_file is not None:
        nameFile = uploaded_file.name.upper().split('.')
        if nameFile[-1] == 'PDF':
            with pdfplumber.open(uploaded_file) as pdf:
                text_base = ''
                pages = pdf.pages
                for p in pages:
                    text_base = text_base + p.extract_text()
                if len(text_base)>4000:
                    text_base = text_base[0:4000]
                    st.info('The text was reduced to 4000 characters!', icon="⚠️")
        elif nameFile[-1] == 'TXT':
            text_base = uploaded_file.read().decode('utf-8')
        else:
            st.error('Wrong type!')

with col2:
    text = st.text_area("or paste your text into the box below.", value=text_base, max_chars=4000, height=400, key='text_area_field')

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['Summary', 'Sentiment', 'Rewriting', 'Change Style', 'Questions', 'Child'])


# show tabs to choose the action
with tab1:
    st.write('Make a short summary of the text')
    botSummary = st.button("Text Summary")
    if botSummary:
        if check_text(text):
            revised_text, language = revise_text(text, "Faça um resumo rápido deste texto, mantendo a língua do texto original ", max_tokens, temperature)
            st.write(revised_text)
            # readText(revised_text, language)
                

with tab2:    
    st.write('Identify the principal sentiment')
    botSentiment = st.button("Text Sentiment")
    if botSentiment:
        if check_text(text):
            revised_text, language = revise_text(text, "Qual o sentimento deste texto? Descreva na mesma língua do texto a seguir ", max_tokens, temperature)
            st.write(revised_text)    

        
with tab3:        
    st.write('Rewrite and try to improve the text')
    botRewriting = st.button("Text Rewriting")
    if botRewriting:
        if check_text(text):
            revised_text, language = revise_text(text, "Reescreva e melhore o texto a seguir, mantendo a língua do texto original  ", max_tokens, temperature)
            st.write(revised_text)   
            # readText(revised_text, language)


with tab4:        
    st.write('Change the style to humorous')
    botStyle = st.button("Change Style")
    if botStyle:
        if check_text(text):
            revised_text, language = revise_text(text, "Reescreva o texto em estilo humorístico, mantendo a língua do texto  ", max_tokens, temperature)
            st.write(revised_text)                  
            # readText(revised_text, language)

with tab5:        
    st.write('Questions')
    botQuestions = st.button("Possible questions")
    if botQuestions:
        if check_text(text):
            revised_text, language = revise_text(text, "Faça perguntas sobre o texto, mantendo a língua do texto  ", max_tokens, temperature)
            st.write(revised_text)                  
            # readText(revised_text, language)

with tab6:        
    st.write('Child')
    botChild = st.button("Child explanation")
    if botChild:
        if check_text(text):
            revised_text, language = revise_text(text, "explique o texto em linguagem infantil, mantendo a língua do texto  ", max_tokens, temperature)
            st.write(revised_text)                  
            # readText(revised_text, language)