import streamlit as st
import google.generativeai as genai

# Isso aqui faz o código ler a chave que você colocou nos Secrets do Streamlit
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Erro ao carregar a chave da IA. Verifique se salvou nos Secrets!")

st.title("🤖 Gerador de Usernames com IA")

entrada = st.text_input("Digite os temas (ex: Nayeon, Gatos, Tarot):")

if st.button("Gerar com Inteligência Artificial"):
    if entrada:
        with st.spinner('O Gemini está criando nomes incríveis...'):
            try:
                # O "comando" para a IA
                prompt = f"Gere 8 nomes de usuário criativos e curtos para Twitter sobre: {entrada}. Apenas os nomes, um por linha, sem @."
                
                response = model.generate_content(prompt)
                
                st.success("Sugestões da IA:")
                for nome in response.text.strip().split('\n'):
                    if nome:
                        st.code(f"@{nome.strip().lower().replace(' ', '')}")
            except Exception as e:
                st.error("A IA deu um erro. Tente novamente!")
    else:
        st.warning("Escreva algo primeiro!")
