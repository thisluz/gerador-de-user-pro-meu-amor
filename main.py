import streamlit as st
from faker import Faker
import random

# Configuração da página
st.set_page_config(page_title="Gerador de Usernames Multi-Temas", page_icon="✨")

fake = Faker('pt_BR')

st.title("✨ Gerador de Usernames Pro")
st.write("Digite um ou mais temas separados por vírgula (ex: Nayeon, Gatos, Tarot)")

# Entrada de texto
entrada_usuario = st.text_input("Temas:", placeholder="Nayeon, Gatos, Tarot")

if st.button("Gerar Sugestões"):
    if entrada_usuario:
        # Transforma a frase em uma lista de temas, removendo espaços inúteis
        lista_temas = [t.strip().lower().replace(" ", "") for t in entrada_usuario.split(",")]
        
        # Termos de estilo para deixar o nome com cara de Twitter
        termos_fan = ["archive", "fancam", "stan", "core", "soft", "pics", "daily", "update", "files", "source"]
        
        st.success(f"Misturando os temas: {', '.join(lista_temas)}")
        
        # Gera 8 opções variadas
        for _ in range(8):
            # Sorteia qual tema dessa vez
            tema_da_vez = random.choice(lista_temas)
            estilo = random.randint(1, 5)
            
            if estilo == 1:
                user = f"{tema_da_vez}_{fake.word()}"
            elif estilo == 2:
                user = f"{random.choice(termos_fan)}_{tema_da_vez}"
            elif estilo == 3:
                user = f"{tema_da_vez}{random.randint(10, 999)}"
            elif estilo == 4:
                # Mistura dois temas se houver mais de um
                if len(lista_temas) > 1:
                    outro_tema = random.choice(lista_temas)
                    while outro_tema == tema_da_vez:
                        outro_tema = random.choice(lista_temas)
                    user = f"{tema_da_vez}_{outro_tema}"
                else:
                    user = f"{tema_da_vez}_{fake.first_name().lower()}"
            else:
                user = f"{fake.color_name()}_{tema_da_vez}"
            
            # Exibe o código para copiar
            st.code(f"@{user}")
    else:
        st.error("Digite pelo menos um tema!")
