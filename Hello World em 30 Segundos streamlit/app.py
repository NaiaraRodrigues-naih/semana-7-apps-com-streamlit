import streamlit as st

st.title("Meu Primeiro App Streamlit")
st.write("Bem-vindo ao Kensei AI Foundations 2026!")

name = st.text_input("Digite seu nome:", value="")

if st.button("Clique em mim!"):
    if name:
        st.success(f"Funcionou! Olá, {name}! Você é dev web!")
    else:
        st.success("Funcionou! Você é dev web!")

st.write("\nUse o campo acima para personalizar a mensagem quando clicar no botão.")
