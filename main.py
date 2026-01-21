import streamlit as st
from faker import Faker
import random

# Configuração da página (deixa o site com ícone e título na aba)
st.set_page_config(page_title="Gerador de Usernames", page_icon="✨")

fake = Faker('pt_BR')

st.title("✨ Gerador de Usernames")
st.write("Crie nomes criativos para o Twitter/Instagram sem precisar de código!")

# Campo de entrada
tema = st.text_input("Qual o tema? (Ex: Twice, Gatos, Romani)", placeholder="Digite aqui...")

if st.button("Gerar Nomes"):
    if tema:
        # Lista de termos estilo "fã" para misturar
        termos_fan = ["archive", "fancam", "stan", "core", "soft", "pics", "daily", "update", "files"]
        
        st.success(f"Sugestões para o tema: {tema}")
        
        # Gera 5 opções diferentes
        for _ in range(5):
            estilo = random.randint(1, 5)
            
            if estilo == 1:
                user = f"{tema}_{fake.word()}"
            elif estilo == 2:
                user = f"{random.choice(termos_fan)}_{tema}"
            elif estilo == 3:
                user = f"{tema}{random.randint(10, 99)}"
            elif estilo == 4:
                user = f"{tema}_{fake.first_name().lower()}"
            else:
                user = f"{fake.color_name()}_{tema}"
            
            # st.code cria um campo que a pessoa clica e já copia o nome
            st.code(f"@{user.replace(' ', '')}") 
    else:
        st.error("Por favor, digite um tema antes de clicar!")
