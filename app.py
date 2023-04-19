import streamlit as st
import openai
# from io import StringIO
# import pdfplumber
# from gtts import gTTS
# import pygame
# import re
# import time

# Insira sua chave de API aqui
openai.api_key = st.secrets['api_key_openai']

with st.sidebar:
    st.header('Orientação de uso')
    st.write('1 - Cole o tema e o texto nos campos indicados. O limite é de 4000 caracteres entre tema e redação.')
    st.write('2 - Pressione o botão para que a análise seja processada.')
    
    # st.header('Parameters')
   
    temperature = 0.4
    # temperature = st.slider('Temperature', 0, 100, 50, 1)/100
    # st.write('Temperature for action. Smaller values are more accurate, larger values are riskier.')
    # st.markdown("""---""")
    max_tokens = 4096
    # max_tokens = st.slider('Limit words', 10, 4000, 1000, 100)
    # st.write('Limit of words for the response.')
    
    limiteModelo = 4096
    limiteResposta = 400
    
    prompt = ''
    prompt_base = """Você é um professor de língua portuguesa. 
                    Ação: avaliar a redação do aluno do 1º ano do Ensino Médio do Brasil
                    Critério: máximo de 100 pontos com as seguintes ponderações:
                    a) Coerência do seu texto com as opções assinaladas :30pontos
                    b) Informações sobre as empresas, trabalhos e funções descritas:30pontos
                    c) Qualidade do texto (português, pontuação etc):30pontos
                    d) Perspectivas futuras no estudo ou trabalho:10pontos
                    Responder apenas a letra e a quantidade de pontos"""
    frase1 = "Tema: '"
    frase2 = "' Redação do aluno a ser avaliada: '"
    final = "'"
   
    st.header('Sobre')
    st.write('Detalhe sobre este projeto pode ser encontrado em: https://github.com/htsnet/AvaliacaoRedacao')
    
    
def revise_text(tema, redacao, max_tokens, temperature):
    with st.spinner('Aguarde...'):
        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt + frase1 + tema + frase2 + redacao + final,
            # max_tokens=max_tokens - len(tema) - len(redacao) - len(prompt) - len(frase1) - len(frase2) - len(final),
            max_tokens=limiteResposta, # é suficiente para a resposta curta
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0,
            temperature=temperature,
        )

    message = completions.choices[0].text
    return message

def check_text():
    if not (tema and redacao):
        st.info('Um dos campos está vazio!', icon="⚠️")
        return False
    if (limiteModelo - len(tema) - len(redacao) - len(prompt) - len(frase1) - len(frase2) - len(final) - limiteResposta > limiteModelo):
        st.info('O tamanho dos textos ultrapassou o limite viável!', icon="⚠️")
        return False
    return True 

def atualizaUsado():
    usado.write(f'Caracteres usados: {len(tema) + len(redacao) + len(prompt) + len(frase1) + len(frase2) + len(final)}/{limiteModelo}')
    if limiteResposta + len(tema) + len(redacao) + len(prompt) + len(frase1) + len(frase2) + len(final) > limiteModelo:
        st.info('Atenção ao limite de texto possível!', icon="⚠️")

# título
Title = f'Avaliação de Redação (ChatGPT)'
st.title(Title)

prompt = st.text_area("Orientação", value=prompt_base, max_chars=800, height=200, key='prompt_area_field', on_change=atualizaUsado)
tema = st.text_area("Tema", max_chars=800, height=100, key='theme_area_field', on_change=atualizaUsado)
redacao = st.text_area("Redação", max_chars=3200, height=400, key='speech_area_field', on_change=atualizaUsado)

#criando uma área para mostrar a quantidade de caracteres usada
usado = st.empty()
atualizaUsado()

botSummary = st.button("Pressione aqui para a avaliação da redação com relação ao tema")
if botSummary:
    if check_text():
        revised_text = revise_text(tema, redacao, max_tokens, temperature)
        st.write(revised_text)
        # readText(revised_text, language)