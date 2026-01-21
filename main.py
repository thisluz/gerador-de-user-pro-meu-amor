import streamlit as st
import google.generativeai as genai
import os

# Configuração da página
st.set_page_config(page_title="Criando users para o meu amor", page_icon="💖")

# Tenta configurar o modelo usando o nome mais compatível com v1beta
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 'gemini-pro' é o modelo com maior suporte legado na v1beta
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.error("Chave não encontrada nos Secrets!")
except Exception as e:
    st.error(f"Erro na configuração: {e}")

st.title("💖 Criando users para o meu amor")

entrada = st.text_input("Escolha os temas", placeholder="Ex: Nayeon, Gatos, Tarot")

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner('Criando sugestões...'):
            try:
                prompt = f"Gere 10 nomes de usuário curtos para redes sociais baseados em: {entrada}. Apenas os nomes, um por linha, sem @ e sem explicações."
                
                response = model.generate_content(prompt)
                
                if response:
                    st.success("Aqui estão as ideias para você:")
                    # Limpeza para garantir que o texto da IA seja exibido corretamente
                    sugestoes = response.text.strip().split('\n')
                    for nome in sugestoes:
                        if nome:
                            user_limpo = nome.replace("*", "").replace("-", "").replace(".", "").strip().lower().replace(" ", "")
                            st.code(f"@{user_limpo}")
            except Exception as e:
                # Se ainda der 404, vamos tentar o modelo legado absoluto
                st.error(f"Erro: {e}")
                st.info("Tentando uma conexão alternativa...")
    else:
        st.warning("Escreva os temas primeiro, amor!")
