import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Criando users para o meu amor", page_icon="💖")

try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Alterado para 'gemini-pro' que tem maior compatibilidade com a v1
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.error("A chave 'GEMINI_API_KEY' não foi encontrada nos Secrets!")
except Exception as e:
    st.error(f"Erro na configuração: {e}")

st.title("💖 Criando users para o meu amor")
entrada = st.text_input("Escolha os temas", placeholder="Ex: Nayeon, Gatos, Tarot")

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner('Criando sugestões...'):
            try:
                prompt = f"Gere 10 nomes de usuário curtos para Twitter sobre: {entrada}. Apenas os nomes, um por linha, sem @ e sem explicações."
                response = model.generate_content(prompt)
                
                st.success("Aqui estão as ideias para você:")
                # O Gemini Pro às vezes retorna texto formatado, vamos garantir a limpeza
                sugestoes = response.text.strip().split('\n')
                for nome in sugestoes:
                    if nome:
                        user_limpo = nome.replace("*", "").replace("-", "").strip().lower().replace(" ", "")
                        st.code(f"@{user_limpo}")
            except Exception as e:
                st.error(f"Erro detalhado: {e}")
    else:
        st.warning("Escreva os temas primeiro, amor!")
