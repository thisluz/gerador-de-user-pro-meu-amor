import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(
    page_title="Criando users para o meu amor",
    page_icon="💖"
)

# Verificação da chave da API
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Chave GEMINI_API_KEY não encontrada nos Secrets.")
    st.stop()

API_KEY = st.secrets["GEMINI_API_KEY"]
BASE_URL = "https://generativelanguage.googleapis.com/v1"

st.title("💖 Criando users para o meu amor")

entrada = st.text_input(
    "Escolha os temas",
    placeholder="Ex: Nayeon, Gatos, Tarot"
)

def listar_modelos_validos():
    resp = requests.get(
        f"{BASE_URL}/models?key={API_KEY}",
        timeout=20
    )

    if resp.status_code != 200:
        raise Exception(f"Erro ao listar modelos: {resp.text}")

    data = resp.json()
    modelos = []

    for m in data.get("models", []):
        if "generateContent" in m.get("supportedGenerationMethods", []):
            modelos.append(m["name"])

    if not modelos:
        raise Exception("Nenhum modelo compatível com generateContent encontrado.")

    return modelos

def gerar_nomes(prompt: str, modelo: str) -> str:
    url = f"{BASE_URL}/{modelo}:generateContent"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        f"{url}?key={API_KEY}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()
    return data["candidates"][0]["content"]["parts"]
