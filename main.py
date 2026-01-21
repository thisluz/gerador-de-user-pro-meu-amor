import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Criando users para o meu amor", page_icon="💖")

# Configuração da IA - Usando a versão 'latest' para evitar o erro 404
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # 'gemini-1.5-flash-latest' é o caminho mais seguro para evitar o 404
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    else:
        st.error("Chave não encontrada nos Secrets!")
except Exception as e:
    st.error(f"Erro na configuração: {e}")

st.title("💖 Criando users para o meu amor")

# Entrada conforme solicitado
entrada = st.text_input("Escolha os temas", placeholder="Ex: Nayeon, Gatos, Tarot")

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner('Criando sugestões...'):
            try:
                # Prompt direto para manter a essência dos seus temas
                prompt = f"Gere 10 nomes de usuário curtos para redes sociais baseados em: {entrada}. Apenas os nomes, um por linha, sem @ e sem explicações."
                
                response = model.generate_content(prompt)
                
                if response.text:
                    st.success("Aqui estão as ideias para você:")
                    sugestoes = response.text.strip().split('\n')
                    for nome in sugestoes:
                        if nome:
                            # Limpeza total de símbolos para o user ficar perfeito
                            user_limpo = nome.replace("*", "").replace("-", "").replace(".", "").strip().lower().replace(" ", "")
                            st.code(f"@{user_limpo}")
            except Exception as e:
                # Se ainda der erro, o log nos dirá se é algo na chave ou no modelo
                st.error(f"Erro detalhado: {e}")
    else:
        st.warning("Escreva os temas primeiro, amor!")
