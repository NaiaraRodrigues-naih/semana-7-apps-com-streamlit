import streamlit as st
import requests
import os
import base64

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
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.04;
        z-index: 0;
        pointer-events: none;
    }}
    </style>
    """

st.set_page_config(page_title="Chat com IA", page_icon="🤖")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] { background-color: #050510 !important; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #050510 0%, #0a0520 50%, #050510 100%) !important;
}
[data-testid="stSidebar"] {
    background: #08081a !important;
    border-right: 1px solid #ff006e44;
}
[data-testid="stSidebar"] * { color: #e0e0ff !important; }
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ff006e !important;
    text-shadow: 0 0 20px #ff006e, 0 0 40px #ff006e66;
}
p, label, div { font-family: 'Rajdhani', sans-serif !important; color: #e0e0ff !important; }

[data-testid="stTextInput"] input {
    background: #0d0d2b !important;
    border: 1px solid #00d4ff !important;
    border-radius: 8px !important;
    color: #00d4ff !important;
    box-shadow: 0 0 10px #00d4ff22;
}
[data-testid="stSelectbox"] > div > div {
    background: #0d0d2b !important;
    border: 1px solid #ff006e !important;
    color: #ff006e !important;
    border-radius: 8px !important;
}
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #ff006e, #cc0055) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 0 20px #ff006e66 !important;
    width: 100% !important;
}
[data-testid="stButton"] button:hover {
    box-shadow: 0 0 30px #ff006e !important;
    transform: translateY(-2px) !important;
}

/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 12px !important;
    margin: 6px 0 !important;
    border: 1px solid #ffffff11 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #1a0a2e, #0d0d2b) !important;
    border-color: #ff006e33 !important;
    box-shadow: 0 0 15px #ff006e11 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, #0a1a2e, #050520) !important;
    border-color: #00d4ff33 !important;
    box-shadow: 0 0 15px #00d4ff11 !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    border: 2px solid #00d4ff !important;
    border-radius: 12px !important;
    background: #0d0d2b !important;
    box-shadow: 0 0 25px rgba(0,212,255,0.3) !important;
}
[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    background: transparent !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(0,212,255,0.5) !important;
    font-style: italic !important;
}
hr { border-color: #ff006e22 !important; }
</style>
""", unsafe_allow_html=True)

AVATAR      = os.path.join(os.path.dirname(__file__), "..", "avatar.png")
KENSEI_LOGO = os.path.join(os.path.dirname(__file__), "..", "kensei_logo.png")
st.markdown(bg_css(KENSEI_LOGO), unsafe_allow_html=True)
st.markdown("<h1>🤖 Chat com IA</h1>", unsafe_allow_html=True)

AVATAR = os.path.join(os.path.dirname(__file__), "..", "avatar.png")

with st.sidebar:
    if os.path.exists(KENSEI_LOGO):
        st.image(KENSEI_LOGO, use_container_width=True)
    st.markdown("<div style='text-align:center; color:#ff006e; font-family:Orbitron,sans-serif; font-size:0.8rem; letter-spacing:2px;'>KENSEI AI</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("## ⚙️ Configurações")
    modelo = st.selectbox("Modelo", ["llama3.2", "mistral"])
    st.write("")
    if st.button("🗑️ Limpar conversa"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.caption("🦙 Rodando local com Ollama")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json={"model": modelo, "messages": st.session_state.messages, "stream": False},
                    timeout=120,
                )
                resposta = response.json()["message"]["content"]
                st.write(resposta)

        st.session_state.messages.append({"role": "assistant", "content": resposta})

    except Exception as e:
        st.error(f"Erro ao conectar com Ollama: {e}")
