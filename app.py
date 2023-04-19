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
    st.header('Orientação de uso')
    st.write('1 - Cole o tema e o texto nos campos indicados. O limite é de 4000 caracteres entre tema e redação.')
    st.write('2 - Pressione o botão para que a análise seja processada.')
    
    # st.header('Parameters')
   
    temperature = 0.7
    # temperature = st.slider('Temperature', 0, 100, 50, 1)/100
    # st.write('Temperature for action. Smaller values are more accurate, larger values are riskier.')
    # st.markdown("""---""")
    max_tokens = 4050
    # max_tokens = st.slider('Limit words', 10, 4000, 1000, 100)
    # st.write('Limit of words for the response.')
    
    prompt = ''
    prompt_base = """Tópico: avaliação de questionário.
                    Persona: seja um professor de língua portuguesa e avalie a redação abaixo.
                    Contexto: Redação de aluno do 1º ano do Ensino Médio do Brasil
                    O que avaliar (num máximo de 100 pontos com as seguintes ponderações):
                    Coerência do seu texto com as opções assinaladas (30pontos)
                    Informações sobre as empresas, trabalhos e funções descritas (30pontos)
                    Qualidade do texto (português, pontuação etc) (30pontos)
                    Perspectivas futuras no estudo ou trabalho (10pontos)"""
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
            max_tokens=max_tokens - len(tema) - len(redacao) - len(prompt) - len(frase1) - len(frase2) - len(final),
            n=1,
            stop=None,
            temperature=temperature,
        )

    message = completions.choices[0].text
    return message

def check_text(text1, text2):
    if text1 and text2 and (max_tokens - len(tema) - len(redacao) - len(prompt) - len(frase1) - len(frase2) - len(final) > 0):
        return True
    st.info('Um dos campos está vazio ou o tamanhos dos textos ultrapassou o limite viável!', icon="⚠️")
    return False



# título
Title = f'Avaliação de Redação (ChatGPT)'
st.title(Title)

prompt = st.text_area("Tema", value=prompt_base, max_chars=800, height=100, key='prompt_area_field')
tema = st.text_area("Tema", max_chars=800, height=100, key='theme_area_field')
redacao = st.text_area("Redação", max_chars=3200, height=400, key='speech_area_field')

botSummary = st.button("Pressione aqui para a avaliação da redação com relação ao tema")
if botSummary:
    if check_text(tema, redacao):
        revised_text = revise_text(tema, redacao, max_tokens, temperature)
        st.write(revised_text)
        # readText(revised_text, language)