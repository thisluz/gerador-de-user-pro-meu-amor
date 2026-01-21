import streamlit as st
import google.generativeai as genai

# Configuração da página - O que aparece na aba do navegador
st.set_page_config(page_title="Criando users para o meu amor", page_icon="💖")

# Conexão com a chave que você salvou nos Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Erro ao carregar a chave nos Secrets.")

# Visual do site - Personalizado para vocês
st.title("💖 Criando users para o meu amor")
st.write("Aqui estão seus users, gatinha!")

# Entrada de temas
entrada = st.text_input("Escolha seus temas", placeholder="Ex: Nayeon, Gatos, Tarot")

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner('Criando sugestões...'):
            try:
                # Prompt focado apenas nos temas, sem forçar palavras extras
                prompt = f"""Gere 10 sugestões de nomes de usuário curtos e criativos para redes sociais 
                baseados estritamente nos temas: {entrada}. 
                Regras: 
                - Use apenas as palavras dos temas ou variações diretas.
                - Use letras minúsculas.
                - Pode usar underscores ou números.
                - Retorne apenas os nomes, um por linha, sem o símbolo @."""
                
                response = model.generate_content(prompt)
                
                st.success("Aqui estão as ideias para você:")
                for nome in response.text.strip().split('\n'):
                    if nome:
                        # Limpa espaços e garante o formato de user
                        user_limpo = nome.strip().lower().replace(" ", "")
                        st.code(f"@{user_limpo}")
            except Exception as e:
                st.error("Houve um probleminha ao gerar. Tente de novo!")
    else:
        st.warning("Escreva os temas primeiro, amor!")
