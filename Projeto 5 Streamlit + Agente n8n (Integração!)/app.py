import streamlit as st
import requests
import json
from datetime import datetime
from fpdf import FPDF
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

st.set_page_config(page_title="SOC Investigator", page_icon="🛡️", layout="wide")

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
    font-family: 'Orbitron', sans-serif !important;
    box-shadow: 0 0 10px #00d4ff22;
}
[data-testid="stTextInput"] input:focus {
    border-color: #ff006e !important;
    box-shadow: 0 0 15px #ff006e44 !important;
}
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #ff006e, #cc0055) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    box-shadow: 0 0 20px #ff006e66 !important;
    transition: all 0.3s !important;
}
[data-testid="stButton"] button:hover {
    box-shadow: 0 0 35px #ff006e !important;
    transform: translateY(-2px) !important;
}
[data-testid="stSuccess"] {
    background: #001a0d !important;
    border-left: 4px solid #00ff88 !important;
    border-radius: 8px !important;
}
[data-testid="stError"] {
    background: #1a0005 !important;
    border-left: 4px solid #ff006e !important;
    border-radius: 8px !important;
}
[data-testid="stWarning"] {
    background: #1a0d00 !important;
    border-left: 4px solid #ffaa00 !important;
    border-radius: 8px !important;
}
.resultado-box {
    background: linear-gradient(135deg, #0d0d2b, #0a1a2e);
    border: 1px solid #00d4ff;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 0 30px #00d4ff22, inset 0 0 20px #00d4ff11;
    margin: 10px 0;
}
.kv-row {
    display: flex;
    border-bottom: 1px solid #ffffff11;
    padding: 8px 0;
}
.kv-key { color: #00d4ff; font-family: 'Orbitron', sans-serif; font-size: 0.85rem; min-width: 180px; }
.kv-val { color: #e0e0ff; font-family: 'Rajdhani', sans-serif; }
hr { border-color: #ff006e22 !important; }
</style>
""", unsafe_allow_html=True)

AVATAR      = os.path.join(os.path.dirname(__file__), "..", "avatar.png")
KENSEI_LOGO = os.path.join(os.path.dirname(__file__), "..", "kensei_logo.png")
st.markdown(bg_css(KENSEI_LOGO), unsafe_allow_html=True)
st.markdown("<h1>🛡️ SOC Investigator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#00d4ff; font-family:Orbitron,sans-serif; font-size:0.85rem; letter-spacing:2px;'>POWERED BY OLLAMA — IA LOCAL</p>", unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(135deg,#0d0d2b,#0a1a2e);border-left:3px solid #00d4ff;
border-radius:8px;padding:12px 16px;margin:10px 0 18px 0;color:#b0c4de;
font-family:'Rajdhani',sans-serif;font-size:0.95rem;line-height:1.6;">
📌 <b>O que é este app?</b> Um investigador de segurança com IA rodando 100% local.
Digite um <b>endereço IP</b> ou <b>URL</b> suspeito e o modelo de IA vai analisar o alvo, avaliar o risco
e gerar um relatório de triagem — como faz um analista de SOC no dia a dia.
</div>""", unsafe_allow_html=True)

with st.sidebar:
    if os.path.exists(KENSEI_LOGO):
        st.image(KENSEI_LOGO, use_container_width=True)
    st.markdown("<div style='text-align:center; color:#ff006e; font-family:Orbitron,sans-serif; font-size:0.8rem; letter-spacing:2px;'>KENSEI AI</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("## ⚙️ Configuração")
    modelo = st.selectbox("🦙 Modelo Ollama", ["llama3.2", "mistral"])
    st.divider()
    st.markdown("## 📋 Histórico")

    if "historico" not in st.session_state:
        st.session_state.historico = []

    if st.session_state.historico:
        for item in reversed(st.session_state.historico):
            with st.expander(f"🔍 {item['alvo']} — {item['data']}"):
                st.caption(item["resumo"])
    else:
        st.caption("Nenhuma investigação ainda.")

# --- Input ---
col1, col2 = st.columns([4, 1])
with col1:
    alvo = st.text_input("🎯 IP ou URL para investigar", placeholder="Ex: 192.168.1.1  |  malicious-site.com")
with col2:
    st.write("")
    st.write("")
    investigar = st.button("🔍 INVESTIGAR", use_container_width=True)

PROMPT_SOC = """Você é um analista de SOC (Security Operations Center) experiente.
Analise o seguinte alvo de segurança e forneça um relatório de triagem estruturado:

Alvo: {alvo}

Responda SEMPRE neste formato exato:

**CLASSIFICAÇÃO:** [SEGURO / SUSPEITO / CRÍTICO]

**TIPO DE ALVO:** [IP público / IP privado / Domínio / URL / Outro]

**ANÁLISE DE RISCO:**
- [3 pontos de análise sobre o alvo]

**INDICADORES DE COMPROMETIMENTO:**
- [Possíveis IOCs ou "Nenhum identificado"]

**RECOMENDAÇÕES:**
- [2 a 3 ações recomendadas para o analista]

**VEREDICTO FINAL:** [Uma frase resumindo a situação]
"""

# --- Investigação ---
if investigar and alvo:
    with st.spinner("⚡ Agente de IA analisando o alvo..."):
        try:
            r = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": modelo,
                    "messages": [{"role": "user", "content": PROMPT_SOC.format(alvo=alvo)}],
                    "stream": False,
                },
                timeout=120,
            )
            resultado_str = r.json()["message"]["content"]

            st.success("✅ Análise concluída!")
            st.markdown("### 📊 Relatório de Triagem SOC")
            st.markdown(f'<div class="resultado-box" style="white-space:pre-wrap;">{resultado_str}</div>', unsafe_allow_html=True)

            st.session_state.historico.append({
                "alvo": alvo,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "resumo": resultado_str[:200],
                "resultado_completo": resultado_str,
            })

            st.divider()
            st.markdown("### 📥 Exportar Relatório")
            if st.button("📄 Gerar PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Helvetica", "B", 16)
                pdf.cell(0, 10, "Relatorio SOC - Investigacao", ln=True)
                pdf.set_font("Helvetica", size=11)
                pdf.cell(0, 8, f"Alvo: {alvo}", ln=True)
                pdf.cell(0, 8, f"Modelo: {modelo}", ln=True)
                pdf.cell(0, 8, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
                pdf.ln(5)
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 8, "Resultado:", ln=True)
                pdf.set_font("Helvetica", size=10)
                for linha in resultado_str.split("\n"):
                    pdf.multi_cell(0, 6, linha.encode("latin-1", "replace").decode("latin-1"))
                pdf_bytes = pdf.output()
                st.download_button(
                    label="⬇️ Baixar PDF",
                    data=bytes(pdf_bytes),
                    file_name=f"soc_{alvo.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf",
                )

        except Exception as e:
            st.error(f"Erro ao conectar com Ollama: {e}")

elif investigar and not alvo:
    st.warning("Digite um IP ou URL para investigar.")
