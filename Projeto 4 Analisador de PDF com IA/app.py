import streamlit as st
from pypdf import PdfReader
from google import genai
from datetime import datetime
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
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.11;
        z-index: 0;
        pointer-events: none;
    }}
    </style>
    """

st.set_page_config(page_title="Analisador de PDF", page_icon="📄")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] { background-color: #050510 !important; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #050510 0%, #0a0520 50%, #050510 100%) !important;
}
[data-testid="stSidebar"] {
    background: #08081a !important;
    border-right: 1px solid #00d4ff44;
}
[data-testid="stSidebar"] * { color: #e0e0ff !important; }
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00d4ff !important;
    text-shadow: 0 0 20px #00d4ff, 0 0 40px #00d4ff66;
}
p, label, div { font-family: 'Rajdhani', sans-serif !important; color: #e0e0ff !important; }

[data-testid="stTextInput"] input {
    background: #0d0d2b !important;
    border: 1px solid #ff006e !important;
    border-radius: 8px !important;
    color: #ff006e !important;
    box-shadow: 0 0 10px #ff006e22;
}
[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #0d0d2b, #0a1a2e) !important;
    border: 2px dashed #00d4ff !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 0 20px #00d4ff22 !important;
}
[data-testid="stFileUploader"] * { color: #00d4ff !important; }
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #00d4ff, #0099cc) !important;
    color: #050510 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 0 20px #00d4ff66 !important;
}
[data-testid="stButton"] button:hover {
    box-shadow: 0 0 30px #00d4ff !important;
}
[data-testid="stInfo"] {
    background: #0a1a2e !important;
    border-left: 4px solid #00d4ff !important;
    border-radius: 8px !important;
}
[data-testid="stSuccess"] {
    background: #001a0d !important;
    border-left: 4px solid #00ff88 !important;
    border-radius: 8px !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #1a0a2e, #0d0d2b) !important;
    border: 1px solid #ff006e33 !important;
    border-radius: 12px !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, #0a1a2e, #050520) !important;
    border: 1px solid #00d4ff33 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"] {
    border: 1px solid #00d4ff !important;
    border-radius: 12px !important;
    background: #0d0d2b !important;
    box-shadow: 0 0 20px #00d4ff22 !important;
}
[data-testid="stChatInput"] textarea { color: #e0e0ff !important; background: transparent !important; }
hr { border-color: #00d4ff22 !important; }
</style>
""", unsafe_allow_html=True)

AVATAR      = os.path.join(os.path.dirname(__file__), "..", "avatar.png")
KENSEI_LOGO = os.path.join(os.path.dirname(__file__), "..", "kensei_logo.png")
st.markdown(bg_css(AVATAR), unsafe_allow_html=True)
st.markdown("<h1>📄 Analisador de PDF com IA</h1>", unsafe_allow_html=True)

AVATAR = os.path.join(os.path.dirname(__file__), "..", "avatar.png")

with st.sidebar:
    if os.path.exists(KENSEI_LOGO):
        st.image(KENSEI_LOGO, use_container_width=True)
    st.markdown("<div style='text-align:center; color:#00d4ff; font-family:Orbitron,sans-serif; font-size:0.8rem; letter-spacing:2px;'>KENSEI AI</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("## ⚙️ Configurações")
    api_key = st.text_input("Gemini API Key", type="password",
                            value=os.getenv("GEMINI_API_KEY", ""))
    modelo = st.selectbox("Modelo", ["gemini-2.0-flash", "gemini-2.0-flash-lite"])

    st.divider()
    st.markdown("## 📚 Histórico")

    if "historico" not in st.session_state:
        st.session_state.historico = []

    if st.session_state.historico:
        for item in reversed(st.session_state.historico):
            with st.expander(f"📄 {item['nome']} — {item['data']}"):
                st.caption(item["resumo"][:300] + "...")
    else:
        st.caption("Nenhum PDF analisado ainda.")

arquivo = st.file_uploader("Envie seu PDF", type="pdf")

if arquivo:
    reader = PdfReader(arquivo)
    texto = "".join(p.extract_text() or "" for p in reader.pages)
    st.info(f"📄 **{arquivo.name}** — {len(reader.pages)} páginas, {len(texto)} caracteres")

    if not api_key:
        st.warning("Insira sua Gemini API Key na sidebar.")
        st.stop()

    client = genai.Client(api_key=api_key)
    texto_truncado = texto[:12000]

    if "resumo_atual" not in st.session_state or st.session_state.get("pdf_atual") != arquivo.name:
        with st.spinner("🔍 Analisando documento..."):
            try:
                response = client.models.generate_content(
                    model=modelo,
                    contents=(
                        f"Analise o documento abaixo e forneça:\n"
                        f"1. **Tipo/Classificação** do documento\n"
                        f"2. **Resumo** em 5 bullet points\n"
                        f"3. **Pontos de atenção** relevantes\n\n"
                        f"Documento:\n{texto_truncado}"
                    ),
                )
                resumo = response.text
                st.session_state.resumo_atual = resumo
                st.session_state.pdf_atual = arquivo.name
                st.session_state.historico.append({
                    "nome": arquivo.name,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "resumo": resumo,
                })
            except Exception as e:
                st.error(f"Erro ao gerar resumo: {e}")
                st.stop()

    st.markdown("### 🧠 Análise do Documento")
    st.markdown(st.session_state.resumo_atual)
    st.divider()

    st.markdown("### 💬 Faça perguntas sobre o documento")
    if "chat_pdf" not in st.session_state or st.session_state.get("pdf_atual") != arquivo.name:
        st.session_state.chat_pdf = []

    for msg in st.session_state.chat_pdf:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if pergunta := st.chat_input("Pergunte algo sobre o PDF..."):
        st.session_state.chat_pdf.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.write(pergunta)
        with st.chat_message("assistant"):
            with st.spinner("Analisando..."):
                try:
                    resp = client.models.generate_content(
                        model=modelo,
                        contents=f"Documento:\n{texto_truncado}\n\nPergunta: {pergunta}",
                    )
                    resposta = resp.text
                    st.write(resposta)
                    st.session_state.chat_pdf.append({"role": "assistant", "content": resposta})
                except Exception as e:
                    st.error(f"Erro: {e}")
