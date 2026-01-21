import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="Criando users para o meu amor", page_icon="💖")

# Configura a IA forçando a versão v1 (estável)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Aqui está o segredo: models/gemini-1.5-flash é o mais atual
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    else:
        st.error("Chave não encontrada nos Secrets!")
except Exception as e:
    st.error(f"Erro na configuração: {e}")

st.title("💖 Criando users para o meu amor")

# Entrada conforme você pediu
entrada = st.text_input("Escolha os temas", placeholder="Ex: Nayeon, Gatos, Tarot")

if st.button("Gerar nomes agora"):
    if entrada:
        with st.spinner('Criando sugestões...'):
            try:
                # Prompt direto para manter o estilo original
                prompt = f"Gere 10 nomes de usuário curtos para Twitter sobre: {entrada}. Apenas os nomes, um por linha, sem @ e sem explicações."
                
                response = model.generate_content(prompt)
                
                st.success("Aqui estão as ideias para você:")
                sugestoes = response.text.strip().split('\n')
                for nome in sugestoes:
                    if nome:
                        # Garante que o nome saia limpo e sem símbolos
                        user_limpo = nome.replace("*", "").replace("-", "").strip().lower().replace(" ", "")
                        st.code(f"@{user_limpo}")
            except Exception as e:
                st.error(f"Erro detalhado: {e}")
                st.info("Dica: Tente atualizar a página. Se o erro 404 persistir, pode ser uma instabilidade momentânea na sua região.")
    else:
        st.warning("Escreva os temas primeiro, amor!")
