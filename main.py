import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Criando users para o meu amor",
    page_icon="💖"
)

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Chave GEMINI_API_KEY não encontrada nos Secrets.")
    st.stop()

API_KEY = st.secrets["GEMINI_API_KEY"]

st.title("💖 Criando users para o meu amor")

entrada = st.text_input(
    "Escolha os temas",
    placeholder="Ex: Nayeon, Gatos, Tarot"
)

def gerar_nomes(prompt: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1/models/"
        "gemini-1.0-pro:generateContent"
    )

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
    return data["candidates"][0]["content"]["parts"][0]["text"]

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner("Criando sugestões..."):
            try:
                prompt = (
                    "Gere 10 nomes de usuário curtos para redes sociais "
                    f"baseados em: {entrada}. "
                    "Apenas os nomes, um por linha, sem @ e sem explicações."
                )

                texto = gerar_nomes(prompt)

                st.success("Aqui estão as ideias para você:")

                for nome in texto.splitlines():
                    user_limpo = (
                        nome.replace("*", "")
                        .replace("-", "")
                        .replace(".", "")
                        .strip()
                        .lower()
                        .replace(" ", "")
                    )
                    if user_limpo:
                        st.code(f"@{user_limpo}")

            except Exception as e:
                st.error(f"Erro ao gerar nomes: {e}")
    else:
        st.warning("Escreva os temas primeiro, amor!")
