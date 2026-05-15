import streamlit as st
import os
import base64

AVATAR      = os.path.join(os.path.dirname(__file__), "..", "avatar.png")
KENSEI_LOGO = os.path.join(os.path.dirname(__file__), "..", "kensei_logo.png")

def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def bg_css(path):
    if not os.path.exists(path):
        return ""
    data = img_b64(path)
    return f"""
    <style>
    [data-testid="stAppViewContainer"]::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: url('data:image/png;base64,{data}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.12;
        z-index: 0;
        pointer-events: none;
    }}
    </style>
    """

st.set_page_config(page_title="Calculadora IMC", page_icon="🏆", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #050510 !important;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #050510 0%, #0a0520 50%, #050510 100%) !important;
}
[data-testid="stSidebar"] {
    background: #08081a !important;
    border-right: 1px solid #ff006e44;
}
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff006e !important;
    text-shadow: 0 0 20px #ff006e, 0 0 40px #ff006e66;
}
p, label, div {
    font-family: 'Rajdhani', sans-serif !important;
    color: #e0e0ff !important;
}
[data-testid="stNumberInput"] input {
    background: #0d0d2b !important;
    border: 1px solid #00d4ff !important;
    border-radius: 8px !important;
    color: #00d4ff !important;
    font-family: 'Orbitron', sans-serif !important;
    box-shadow: 0 0 10px #00d4ff33;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #ff006e !important;
    box-shadow: 0 0 15px #ff006e66 !important;
}
button[kind="primary"], [data-testid="stButton"] button {
    background: linear-gradient(135deg, #ff006e, #cc0055) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    box-shadow: 0 0 20px #ff006e66, 0 0 40px #ff006e33 !important;
    transition: all 0.3s !important;
}
button[kind="primary"]:hover, [data-testid="stButton"] button:hover {
    box-shadow: 0 0 30px #ff006e, 0 0 60px #ff006e66 !important;
    transform: translateY(-2px) !important;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d0d2b, #1a0a2e) !important;
    border: 1px solid #ff006e !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 0 20px #ff006e33 !important;
}
[data-testid="stMetricValue"] {
    color: #ff006e !important;
    font-family: 'Orbitron', sans-serif !important;
    text-shadow: 0 0 15px #ff006e !important;
}
[data-testid="stMetricLabel"] {
    color: #00d4ff !important;
    font-family: 'Orbitron', sans-serif !important;
}
[data-testid="stSuccess"] {
    background: #001a0d !important;
    border-left: 4px solid #00ff88 !important;
    border-radius: 8px !important;
    color: #00ff88 !important;
}
[data-testid="stWarning"] {
    background: #1a0d00 !important;
    border-left: 4px solid #ffaa00 !important;
    border-radius: 8px !important;
}
[data-testid="stError"] {
    background: #1a0005 !important;
    border-left: 4px solid #ff006e !important;
    border-radius: 8px !important;
}
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #ff006e, #00d4ff) !important;
    box-shadow: 0 0 10px #ff006e !important;
    border-radius: 10px !important;
}
[data-testid="stProgress"] > div {
    background: #1a1a3a !important;
    border-radius: 10px !important;
}
hr {
    border-color: #ff006e33 !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if os.path.exists(KENSEI_LOGO):
        st.image(KENSEI_LOGO, use_container_width=True)
    st.markdown("<div style='text-align:center; color:#ff006e; font-family:Orbitron,sans-serif; font-size:0.8rem; letter-spacing:2px;'>KENSEI AI</div>", unsafe_allow_html=True)
    st.divider()

st.markdown(bg_css(AVATAR), unsafe_allow_html=True)
st.markdown("<h1>🏆 Calculadora de IMC</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("⚡ Peso (kg)", 30.0, 200.0, value=70.0)
with col2:
    altura = st.number_input("📏 Altura (m)", 1.0, 2.5, value=1.75)

st.write("")
if st.button("CALCULAR IMC"):
    imc = peso / (altura ** 2)
    st.metric("Seu IMC", f"{imc:.1f}")

    if imc < 18.5:
        st.warning("⚠️ Abaixo do peso")
        faixa = "Abaixo do peso"
    elif imc < 25:
        st.success("✅ Peso normal")
        faixa = "Peso normal"
    elif imc < 30:
        st.warning("⚠️ Sobrepeso")
        faixa = "Sobrepeso"
    else:
        st.error("🚨 Acima do peso")
        faixa = "Acima do peso"

    st.markdown("### Faixas de IMC")
    faixas = {
        "Abaixo do peso": (0, 18.5),
        "Peso normal":    (18.5, 25),
        "Sobrepeso":      (25, 30),
        "Acima do peso":  (30, 40),
    }
    for nome, (minv, maxv) in faixas.items():
        valor = min(max(imc, minv), maxv) - minv
        total = maxv - minv
        progresso = valor / total if nome == faixa else (1.0 if imc >= maxv else 0.0)
        marcador = " ◄ você está aqui" if nome == faixa else ""
        st.write(f"**{nome}** ({minv} – {maxv}){marcador}")
        st.progress(progresso)
