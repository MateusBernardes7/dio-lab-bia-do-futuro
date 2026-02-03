import pandas as pd
import json
import requests
import streamlit as st

OLLAM_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

perfil = json.load(open('./data/perfil_investidos.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
produtos = json.load(open('./data/produtos_financeiros.json'))

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIOES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}

"""

SYSTEM_PROMPT = """ 
Você é o INVEST-MAN, responsável por dar informações sobre investimentos financeiros de forma objetiva e sem enrolar, mas sempre sem educado

OBJETIVO: Demonstar os diferentes tipos de investimentos que existem, deixando mais fácil o entendimento do usuário sobre o assunto

REGRAS:
1. Nunca recomende investimentos específicos - queremos apenas explicações
2. Use os dados fornecidos para dar exemplos personalizados
3. Se não souber algo, admita e ofereça alternativas
4. Linguagem simples, como se explicasse pra um amigo
5. Sempre pergunte se o usuário entendeu

[CONTEXTO: USO DA BASE DE CONHECIMENTO]

"""

def perguntar(msg):
    prompt = f""" 
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAM_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

st.title("INVEST-MAN")

if pergunta := st.chat_input("Sua dúvida sobre finanças..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))