import streamlit as st
from google import genai

st.set_page_config(
    page_title="Criando users para o meu amor",
    page_icon="💖"
)

if "GEMINI_API_KEY" not in st.secrets:
    st.error("Chave GEMINI_API_KEY não encontrada nos Secrets.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("💖 Criando users para o meu amor")

entrada = st.text_input(
    "Escolha os temas",
    placeholder="Ex: Nayeon, Gatos, Tarot"
)

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner("Criando sugestões..."):
            try:
                prompt = (
                    "Gere 10 nomes de usuário curtos para redes sociais "
                    f"baseados em: {entrada}. "
                    "Apenas os nomes, um por linha, sem @ e sem explicações."
                )

                response = client.models.generate_content(
                    model="models/gemini-1.5-pro",
                    contents=prompt
                )

                st.success("Aqui estão as ideias para você:")

                for nome in response.text.splitlines():
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
