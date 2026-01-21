import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Criando users para o meu amor", page_icon="💖")

# Tenta configurar a IA
try:
    # Verificação se a chave existe nos Secrets
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("A chave 'GEMINI_API_KEY' não foi encontrada nos Secrets!")
except Exception as e:
    st.error(f"Erro na configuração: {e}")

st.title("💖 Criando users para o meu amor")
entrada = st.text_input("Quais temas vamos usar hoje, vida?", placeholder="Ex: Nayeon, Gatos, Tarot")

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner('Criando sugestões...'):
            try:
                prompt = f"Gere 10 nomes de usuário para Twitter sobre: {entrada}. Apenas os nomes, um por linha, sem @."
                response = model.generate_content(prompt)
                
                st.success("Aqui estão as ideias para você:")
                for nome in response.text.strip().split('\n'):
                    if nome:
                        st.code(f"@{nome.strip().lower().replace(' ', '')}")
            except Exception as e:
                # ESTA LINHA VAI NOS DIZER O ERRO REAL
                st.error(f"Erro detalhado: {e}")
    else:
        st.warning("Escreva os temas primeiro, amor!")
