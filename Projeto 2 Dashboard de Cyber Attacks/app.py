import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
        opacity: 0.03;
        z-index: 0;
        pointer-events: none;
    }}
    </style>
    """

st.set_page_config(layout="wide", page_title="Cyber Attacks Dashboard", page_icon="🛡️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] { background-color: #050510 !important; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #050510 0%, #0a0520 50%, #050510 100%) !important;
}
[data-testid="stSidebar"] {
    background: #08081a !important;
    border-right: 1px solid rgba(0,212,255,0.27);
}
[data-testid="stSidebar"] * { color: #e0e0ff !important; }
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00d4ff !important;
    text-shadow: 0 0 20px #00d4ff, 0 0 40px rgba(0,212,255,0.4);
}
p, label, div { font-family: 'Rajdhani', sans-serif !important; color: #e0e0ff !important; }
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #0d0d2b, #0a1a2e) !important;
    border: 1px solid #00d4ff !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2), inset 0 0 20px rgba(0,212,255,0.07) !important;
}
[data-testid="stMetricValue"] {
    color: #ff006e !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 1.8rem !important;
    text-shadow: 0 0 15px #ff006e !important;
}
[data-testid="stMetricLabel"] {
    color: #00d4ff !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
}
[data-testid="stDataFrame"] { border: 1px solid rgba(0,212,255,0.2) !important; border-radius: 8px !important; }
hr { border-color: rgba(0,212,255,0.13) !important; }
[data-testid="stMultiSelect"] span { background: #ff006e !important; border-radius: 4px !important; }
</style>
""", unsafe_allow_html=True)

KENSEI_LOGO = os.path.join(os.path.dirname(__file__), "..", "kensei_logo.png")
st.markdown(bg_css(KENSEI_LOGO), unsafe_allow_html=True)

CSV_PATH = os.path.join(os.path.dirname(__file__), "cyber_attacks.csv")
if not os.path.exists(CSV_PATH):
    st.error("Arquivo `cyber_attacks.csv` não encontrado.")
    st.stop()

try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(CSV_PATH, encoding="latin-1")

df.columns = [c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "") for c in df.columns]

pais_col   = next((c for c in df.columns if "countr" in c), df.columns[0])
ano_col    = next((c for c in df.columns if "year" in c), None)
tipo_col   = next((c for c in df.columns if "attack" in c and "type" in c), None)
dano_col   = next((c for c in df.columns if "loss" in c or "financial" in c), None)
users_col  = next((c for c in df.columns if "affected" in c or "users" in c), None)
setor_col  = next((c for c in df.columns if "industry" in c or "target" in c), None)
vuln_col   = next((c for c in df.columns if "vulnerab" in c), None)
defesa_col = next((c for c in df.columns if "defense" in c or "defesa" in c), None)
source_col = next((c for c in df.columns if "source" in c), None)
resolv_col = next((c for c in df.columns if "resolution" in c or "hours" in c), None)

GRID   = "rgba(255,255,255,0.07)"
THEME  = dict(
    paper_bgcolor="#050510",
    plot_bgcolor="#0a0520",
    font=dict(color="#e0e0ff", family="Rajdhani"),
    margin=dict(l=10, r=10, t=10, b=10),
)
SCALE  = [[0, "#0a0520"], [0.5, "#00d4ff"], [1, "#ff006e"]]
COLORS = ["#00d4ff","#ff006e","#7b2fff","#00ff88","#ffaa00","#ff6600","#00ffcc","#ff3399"]

# Sidebar
if os.path.exists(KENSEI_LOGO):
    st.sidebar.image(KENSEI_LOGO, use_container_width=True)
st.sidebar.markdown("<div style='text-align:center;color:#00d4ff;font-family:Orbitron,sans-serif;font-size:0.75rem;letter-spacing:2px;'>KENSEI AI</div>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.markdown("## ⚡ Filtros")

paises    = sorted(df[pais_col].dropna().unique())
sel_paises = st.sidebar.multiselect("🌍 País", paises, default=paises[:10])
anos      = sorted(df[ano_col].dropna().unique()) if ano_col else []
sel_anos  = st.sidebar.multiselect("📅 Ano", anos, default=anos) if ano_col else None
tipos     = sorted(df[tipo_col].dropna().unique()) if tipo_col else []
sel_tipos = st.sidebar.multiselect("🎯 Tipo de Ataque", tipos, default=tipos) if tipo_col else None

filt = df[df[pais_col].isin(sel_paises)] if sel_paises else df.copy()
if sel_anos and ano_col:
    filt = filt[filt[ano_col].isin(sel_anos)]
if sel_tipos and tipo_col:
    filt = filt[filt[tipo_col].isin(sel_tipos)]

# Header
st.markdown("<h1>🛡️ Global Cyber Attacks Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='color:rgba(0,212,255,0.7);font-family:Orbitron,sans-serif;font-size:0.75rem;letter-spacing:2px;'>2015 – 2024 · {len(filt):,} INCIDENTES ANALISADOS</p>", unsafe_allow_html=True)
st.divider()

def card(texto, cor="#00d4ff"):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d0d2b,#0a1a2e);border-left:3px solid {cor};
    border-radius:8px;padding:12px 16px;margin-bottom:12px;color:#b0c4de;
    font-family:'Rajdhani',sans-serif;font-size:0.95rem;line-height:1.5;">
    {texto}
    </div>""", unsafe_allow_html=True)

# Intro
card("📌 <b>Como usar este painel:</b> use os <b>filtros na barra lateral</b> para selecionar países, anos e tipos de ataque. "
     "Todos os gráficos e métricas atualizam automaticamente com base na sua seleção. "
     "Passe o mouse sobre os gráficos para ver os valores exatos.")

# KPIs
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("⚡ Total de Ataques", f"{len(filt):,}")
k2.metric("🌍 Países", filt[pais_col].nunique())
if dano_col:
    k3.metric("💸 Prejuízo Total (M$)", f"{filt[dano_col].sum():,.0f}")
if users_col:
    k4.metric("👥 Usuários Afetados", f"{int(filt[users_col].sum()):,}")
if resolv_col:
    k5.metric("⏱️ Resolução Média (h)", f"{filt[resolv_col].mean():.0f}")
elif tipo_col:
    k5.metric("🎯 Tipos de Ataque", filt[tipo_col].nunique())

card("💡 <b>Lendo os números:</b> "
     "o <b>Total de Ataques</b> conta todos os incidentes registrados no período selecionado. "
     "O <b>Prejuízo</b> é medido em milhões de dólares. "
     "A <b>Resolução Média</b> indica quantas horas as equipes de segurança levaram para conter cada ataque — quanto menor, melhor a resposta.", "#ffaa00")

st.divider()

# Row 1: Timeline + Tipo de Ataque
col_a, col_b = st.columns([3, 2])

with col_a:
    if ano_col:
        st.markdown("### 📅 Evolução de Ataques por Ano")
        card("Este gráfico mostra <b>quantos ataques aconteceram em cada ano</b>. "
             "Picos indicam anos com maior atividade maliciosa — podem refletir novas ondas de malware, conflitos geopolíticos ou falhas críticas descobertas no período.")
        ano_data = filt.groupby(ano_col).size().reset_index(name="Ataques")
        fig_line = px.area(ano_data, x=ano_col, y="Ataques",
                           color_discrete_sequence=["#00d4ff"],
                           labels={ano_col: "Ano"})
        fig_line.update_traces(fill="tozeroy", fillcolor="rgba(0,212,255,0.1)", line=dict(width=2))
        fig_line.update_layout(**THEME, xaxis=dict(gridcolor=GRID), yaxis=dict(gridcolor=GRID))
        st.plotly_chart(fig_line, use_container_width=True)

with col_b:
    if tipo_col:
        st.markdown("### 🎯 Tipos de Ataque")
        card("Cada fatia representa uma <b>categoria de ataque cibernético</b>.<br>"
             "• <b>Phishing</b>: engana o usuário por e-mail ou link falso<br>"
             "• <b>Ransomware</b>: sequestra arquivos e exige resgate<br>"
             "• <b>DDoS</b>: derruba servidores com excesso de tráfego<br>"
             "• <b>Malware</b>: software malicioso instalado na máquina")
        tipo_data = filt[tipo_col].value_counts().reset_index()
        tipo_data.columns = ["Tipo", "Qtd"]
        fig_pie = px.pie(tipo_data, names="Tipo", values="Qtd", hole=0.5,
                         color_discrete_sequence=COLORS)
        fig_pie.update_layout(**THEME, legend=dict(orientation="v", font=dict(size=10)))
        fig_pie.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# Row 2: Ataques por País + Setor Alvo
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("### 🌍 Top 15 Países — Ataques")
    card("Países no topo da lista são os <b>mais afetados ou os que mais registram incidentes</b>. "
         "Isso pode refletir tanto maior exposição digital quanto melhor capacidade de detecção e registro dos ataques.")
    pais_data = filt[pais_col].value_counts().head(15).reset_index()
    pais_data.columns = ["País", "Ataques"]
    fig_pais = px.bar(pais_data, x="Ataques", y="País", orientation="h",
                      color="Ataques", color_continuous_scale=SCALE)
    fig_pais.update_layout(**THEME, yaxis=dict(autorange="reversed", gridcolor=GRID),
                           xaxis=dict(gridcolor=GRID), coloraxis_showscale=False)
    st.plotly_chart(fig_pais, use_container_width=True)

with col_d:
    if setor_col:
        st.markdown("### 🏢 Setores Mais Atacados")
        card("Mostra quais <b>áreas da economia</b> são os alvos favoritos dos hackers. "
             "Saúde, finanças e governo costumam liderar por terem <b>dados sensíveis e sistemas críticos</b> — "
             "um ataque bem-sucedido nesses setores causa o maior impacto.")
        setor_data = filt[setor_col].value_counts().head(10).reset_index()
        setor_data.columns = ["Setor", "Ataques"]
        fig_setor = px.bar(setor_data, x="Ataques", y="Setor", orientation="h",
                           color="Ataques", color_continuous_scale=[[0,"#7b2fff"],[1,"#ff006e"]])
        fig_setor.update_layout(**THEME, yaxis=dict(autorange="reversed", gridcolor=GRID),
                                xaxis=dict(gridcolor=GRID), coloraxis_showscale=False)
        st.plotly_chart(fig_setor, use_container_width=True)

st.divider()

# Row 3: Prejuízo por País + Vulnerabilidades
col_e, col_f = st.columns(2)

with col_e:
    if dano_col:
        st.markdown("### 💸 Prejuízo Financeiro por País (M$)")
        card("Valor total estimado em <b>milhões de dólares</b> perdidos por cada país. "
             "Inclui custos de remediação, multas regulatórias, perda de dados e interrupção de serviços. "
             "Um país pode ter poucos ataques, mas prejuízos enormes se os alvos forem críticos.")
        dano_pais = filt.groupby(pais_col)[dano_col].sum().sort_values(ascending=False).head(12).reset_index()
        dano_pais.columns = ["País", "Prejuízo (M$)"]
        fig_dano = px.bar(dano_pais, x="País", y="Prejuízo (M$)",
                          color="Prejuízo (M$)", color_continuous_scale=SCALE)
        fig_dano.update_layout(**THEME, xaxis=dict(gridcolor=GRID, tickangle=-35),
                               yaxis=dict(gridcolor=GRID), coloraxis_showscale=False)
        st.plotly_chart(fig_dano, use_container_width=True)

with col_f:
    if vuln_col:
        st.markdown("### 🔓 Vulnerabilidades Mais Exploradas")
        card("Mostra as <b>brechas de segurança</b> que os atacantes mais utilizaram.<br>"
             "• <b>Software desatualizado</b>: sistemas sem patches de segurança<br>"
             "• <b>Senha fraca</b>: credenciais fáceis de adivinhar ou roubar<br>"
             "• <b>Configuração incorreta</b>: servidores ou serviços mal configurados<br>"
             "Corrigir essas brechas elimina a maioria dos vetores de ataque.")
        vuln_data = filt[vuln_col].value_counts().reset_index()
        vuln_data.columns = ["Vulnerabilidade", "Qtd"]
        fig_vuln = px.pie(vuln_data, names="Vulnerabilidade", values="Qtd", hole=0.45,
                          color_discrete_sequence=["#ff006e","#ffaa00","#7b2fff","#00d4ff","#00ff88"])
        fig_vuln.update_layout(**THEME, legend=dict(orientation="v", font=dict(size=10)))
        fig_vuln.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(fig_vuln, use_container_width=True)

st.divider()

# Row 4: Fonte do Ataque + Mecanismo de Defesa
col_g, col_h = st.columns(2)

with col_g:
    if source_col:
        st.markdown("### 👾 Fontes dos Ataques")
        card("Identifica <b>quem está por trás dos ataques</b>.<br>"
             "• <b>Hackers independentes</b>: agem por motivação financeira ou desafio<br>"
             "• <b>Grupos organizados</b>: operações criminosas com estrutura profissional<br>"
             "• <b>Estados-nação</b>: ataques patrocinados por governos para espionagem ou sabotagem<br>"
             "• <b>Insider</b>: funcionários ou ex-funcionários da própria organização")
        source_data = filt[source_col].value_counts().reset_index()
        source_data.columns = ["Fonte", "Qtd"]
        fig_src = px.bar(source_data, x="Fonte", y="Qtd",
                         color="Qtd", color_continuous_scale=[[0,"#7b2fff"],[1,"#00d4ff"]])
        fig_src.update_layout(**THEME, xaxis=dict(gridcolor=GRID, tickangle=-20),
                              yaxis=dict(gridcolor=GRID), coloraxis_showscale=False)
        st.plotly_chart(fig_src, use_container_width=True)

with col_h:
    if defesa_col:
        st.markdown("### 🛡️ Mecanismos de Defesa Utilizados")
        card("Ferramentas e estratégias que as organizações usaram para <b>detectar ou conter os ataques</b>.<br>"
             "• <b>Firewall</b>: bloqueia tráfego malicioso na entrada da rede<br>"
             "• <b>Antivírus</b>: detecta e remove softwares maliciosos<br>"
             "• <b>VPN</b>: criptografa a comunicação e oculta a identidade<br>"
             "• <b>MFA</b>: exige segunda confirmação além da senha<br>"
             "Nenhum mecanismo isolado é suficiente — a defesa em camadas é o padrão.", "#00ff88")
        def_data = filt[defesa_col].value_counts().reset_index()
        def_data.columns = ["Defesa", "Qtd"]
        fig_def = px.bar(def_data, x="Defesa", y="Qtd",
                         color="Qtd", color_continuous_scale=[[0,"#00ff88"],[1,"#00d4ff"]])
        fig_def.update_layout(**THEME, xaxis=dict(gridcolor=GRID, tickangle=-20),
                              yaxis=dict(gridcolor=GRID), coloraxis_showscale=False)
        st.plotly_chart(fig_def, use_container_width=True)

st.divider()

# Mapa mundial
st.markdown("### 🗺️ Mapa Mundial de Ataques")
card("Visualização geográfica global — países com cores mais <b>vermelhas/quentes</b> concentram mais ataques registrados. "
     "Passe o mouse sobre cada país para ver o número exato de incidentes. "
     "Use os filtros da sidebar para comparar períodos ou tipos de ataque específicos.")
mapa = filt[pais_col].value_counts().reset_index()
mapa.columns = ["País", "Ataques"]
fig_map = px.choropleth(mapa, locations="País", locationmode="country names",
                        color="Ataques", color_continuous_scale=SCALE)
fig_map.update_layout(
    **{k: v for k, v in THEME.items() if k != "margin"},
    margin=dict(l=0, r=0, t=10, b=0),
    geo=dict(bgcolor="#050510", showframe=False, showcoastlines=True,
             coastlinecolor="rgba(0,212,255,0.2)", landcolor="#0a0520",
             showocean=True, oceancolor="#05051a"),
)
st.plotly_chart(fig_map, use_container_width=True)

st.divider()
st.markdown("### 📋 Dados Brutos")
card("Tabela completa com todos os registros filtrados. Clique em qualquer coluna para <b>ordenar</b>. "
     "Use os filtros da sidebar para reduzir os dados e focar na análise que desejar.")
st.dataframe(filt, use_container_width=True, height=300)
