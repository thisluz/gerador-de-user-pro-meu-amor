import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Criando users para o meu amor",
    page_icon="💖"
)

st.title("💖 Criando users para o meu amor")

entrada = st.text_input(
    "Escolha os temas",
    placeholder="Ex: Nayeon, Gatos, Tarot"
)

# Botão SEMPRE renderiza
gerar = st.button("Gerar nomes agora")

# A partir daqui, só roda se o botão for clicado
if gerar:
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Chave GEMINI_API_KEY não encontrada nos Secrets.")
        st.stop()

    API_KEY = st.secrets["GEMINI_API_KEY"]
    BASE_URL = "https://generativelanguage.googleapis.com/v1"

    def listar_modelos_validos():
        resp = requests.get(
            f"{BASE_URL}/models?key={API_KEY}",
            timeout=20
        )

        if resp.status_code != 200:
            raise Exception(f"Erro ao listar modelos: {resp.text}")

        data = resp.json()
        return [
            m["name"]
            for m in data.get("models", [])
            if "generateContent" in m.get("supportedGenerationMethods", [])
        ]

    def gerar_nomes(prompt: str, modelo: str) -> str:
        url = f"{BASE_URL}/{modelo}:generateContent"

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
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

    if entrada:
        with st.spinner("Criando sugestões..."):
            try:
                modelos = listar_modelos_validos()
                modelo_escolhido = modelos[0]

                st.caption(f"Modelo utilizado: {modelo_escolhido}")

                prompt = (
                    "Gere 10 nomes de usuário para redes sociais "
                    f"baseados em: {entrada}. "
                    "Cada nome deve ter entre 6 e 12 caracteres, "
                    "usar apenas letras, sem números ou símbolos, "
                    "ser criativo e fácil de ler. "
                    "Apenas os nomes, um por linha, sem @ e sem explicações."
                )

                texto = gerar_nomes(prompt, modelo_escolhido)

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

                    if 6 <= len(user_limpo) <= 12:
                        st.code(f"@{user_limpo}")

            except Exception as e:
                st.error(f"Erro ao gerar nomes: {e}")
    else:
        st.warning("Escreva os temas primeiro, amor!")
