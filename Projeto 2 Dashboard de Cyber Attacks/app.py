import streamlit as st
import pandas as pd
import plotly.express as px
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
        opacity: 0.10;
        z-index: 0;
        pointer-events: none;
    }}
    </style>
    """

st.set_page_config(layout="wide", page_title="Cyber Attacks Dashboard", page_icon="🛡️")

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
    border-right: 1px solid #00d4ff44;
}
[data-testid="stSidebar"] * { color: #e0e0ff !important; }
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00d4ff !important;
    text-shadow: 0 0 20px #00d4ff, 0 0 40px #00d4ff66;
}
p, label, div { font-family: 'Rajdhani', sans-serif !important; color: #e0e0ff !important; }
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d0d2b, #0a1a2e) !important;
    border: 1px solid #00d4ff !important;
    border-radius: 12px !important;
    padding: 20px !important;
    box-shadow: 0 0 20px #00d4ff33, inset 0 0 20px #00d4ff11 !important;
}
[data-testid="stMetricValue"] {
    color: #ff006e !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 2rem !important;
    text-shadow: 0 0 15px #ff006e !important;
}
[data-testid="stMetricLabel"] {
    color: #00d4ff !important;
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 1px !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid #00d4ff33 !important;
    border-radius: 8px !important;
}
hr { border-color: #00d4ff22 !important; }
[data-testid="stMultiSelect"] span {
    background: #ff006e !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

AVATAR      = os.path.join(os.path.dirname(__file__), "..", "avatar.png")
KENSEI_LOGO = os.path.join(os.path.dirname(__file__), "..", "kensei_logo.png")
st.markdown(bg_css(AVATAR), unsafe_allow_html=True)
st.markdown("<h1>🛡️ Dashboard de Cyber Attacks</h1>", unsafe_allow_html=True)

CSV_PATH = os.path.join(os.path.dirname(__file__), "cyber_attacks.csv")

if not os.path.exists(CSV_PATH):
    st.error("Arquivo `cyber_attacks.csv` não encontrado nesta pasta.")
    st.info("Baixe em: https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024\n\nSalve como `cyber_attacks.csv` na mesma pasta.")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(CSV_PATH, encoding="latin-1")

df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

pais_col = next((c for c in df.columns if "countr" in c or "pais" in c or "país" in c), df.columns[0])
ano_col  = next((c for c in df.columns if "year" in c or "ano" in c), None)
tipo_col = next((c for c in df.columns if "attack" in c and "type" in c), None)
dano_col = next((c for c in df.columns if "loss" in c or "financial" in c or "dano" in c), None)

PLOTLY_THEME = dict(
    paper_bgcolor="#050510",
    plot_bgcolor="#0a0520",
    font=dict(color="#e0e0ff", family="Rajdhani"),
    title_font=dict(color="#00d4ff", family="Orbitron"),
)

if os.path.exists(KENSEI_LOGO):
    st.sidebar.image(KENSEI_LOGO, use_container_width=True)
st.sidebar.markdown("<div style='text-align:center; color:#00d4ff; font-family:Orbitron,sans-serif; font-size:0.8rem; letter-spacing:2px;'>KENSEI AI</div>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("## ⚡ Filtros")
paises = sorted(df[pais_col].dropna().unique())
sel_paises = st.sidebar.multiselect("País", paises, default=paises[:10])
if ano_col:
    anos = sorted(df[ano_col].dropna().unique())
    sel_anos = st.sidebar.multiselect("Ano", anos, default=anos)
else:
    sel_anos = None
if tipo_col:
    tipos = sorted(df[tipo_col].dropna().unique())
    sel_tipos = st.sidebar.multiselect("Tipo de Ataque", tipos, default=tipos)
else:
    sel_tipos = None

filt = df[df[pais_col].isin(sel_paises)] if sel_paises else df.copy()
if sel_anos and ano_col:
    filt = filt[filt[ano_col].isin(sel_anos)]
if sel_tipos and tipo_col:
    filt = filt[filt[tipo_col].isin(sel_tipos)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("⚡ Total de Ataques", f"{len(filt):,}")
col2.metric("🌍 Países", filt[pais_col].nunique())
if dano_col:
    col3.metric("💸 Prejuízo Total (M$)", f"{filt[dano_col].sum():,.1f}")
elif tipo_col:
    col3.metric("🎯 Tipos de Ataque", filt[tipo_col].nunique())

st.divider()

# Gráfico 1
st.markdown("### ⚡ Ataques por País")
ataques_pais = filt[pais_col].value_counts().reset_index()
ataques_pais.columns = ["País", "Ataques"]
fig1 = px.bar(ataques_pais.head(20), x="País", y="Ataques", color="Ataques",
              color_continuous_scale=[[0, "#0a0520"], [0.5, "#00d4ff"], [1, "#ff006e"]])
fig1.update_layout(**PLOTLY_THEME, xaxis=dict(gridcolor="#ffffff11"), yaxis=dict(gridcolor="#ffffff11"))
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2
if tipo_col:
    st.markdown("### 🎯 Distribuição por Tipo de Ataque")
    tipo_count = filt[tipo_col].value_counts().reset_index()
    tipo_count.columns = ["Tipo", "Quantidade"]
    fig2 = px.pie(tipo_count, names="Tipo", values="Quantidade", hole=0.4,
                  color_discrete_sequence=px.colors.sequential.Plasma_r)
    fig2.update_layout(**PLOTLY_THEME)
    st.plotly_chart(fig2, use_container_width=True)
elif ano_col:
    st.markdown("### 📅 Ataques por Ano")
    ano_count = filt[ano_col].value_counts().sort_index().reset_index()
    ano_count.columns = ["Ano", "Quantidade"]
    fig2 = px.line(ano_count, x="Ano", y="Quantidade", markers=True,
                   color_discrete_sequence=["#00d4ff"])
    fig2.update_layout(**PLOTLY_THEME, xaxis=dict(gridcolor="#ffffff11"), yaxis=dict(gridcolor="#ffffff11"))
    st.plotly_chart(fig2, use_container_width=True)

# Mapa
st.markdown("### 🗺️ Mapa Mundial de Ataques")
mapa = filt[pais_col].value_counts().reset_index()
mapa.columns = ["País", "Ataques"]
fig_map = px.choropleth(mapa, locations="País", locationmode="country names",
                        color="Ataques",
                        color_continuous_scale=[[0, "#0a0520"], [0.5, "#00d4ff"], [1, "#ff006e"]])
fig_map.update_layout(**PLOTLY_THEME, margin=dict(l=0, r=0, t=40, b=0),
                      geo=dict(bgcolor="#050510", showframe=False, showcoastlines=True,
                               coastlinecolor="#00d4ff33", landcolor="#0a0520",
                               showocean=True, oceancolor="#05051a"))
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("### 📋 Dados Filtrados")
st.dataframe(filt, use_container_width=True)
