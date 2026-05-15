# 🛡️ Semana 7 — Apps com Streamlit | Kensei AI Foundations 2026

Cinco aplicações web construídas com Python + Streamlit durante a Semana 7 do programa **Kensei AI Foundations 2026**.

---

## 🚀 Como rodar

### 1. Clone o repositório
```bash
git clone https://github.com/NaiaraRodrigues-naih/semana-7-apps-com-streamlit.git
cd semana-7-apps-com-streamlit
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com suas chaves de API
```

### 4. Rode o projeto desejado
```bash
streamlit run "Projeto 1 Calculadora IMC/app.py"
```

---

## 📁 Projetos

### 🏆 Projeto 1 — Calculadora de IMC
**Arquivo:** `Projeto 1 Calculadora IMC/app.py`

Calcula o IMC (Índice de Massa Corporal) do usuário com visualização interativa.

**Funcionalidades:**
- Entrada de peso e altura com `st.number_input`
- Cálculo e exibição do IMC com `st.metric`
- Classificação colorida (abaixo do peso, normal, sobrepeso, obeso)
- Barra de progresso visual por faixa de IMC

**Conceitos:** `st.number_input`, `st.metric`, `st.progress`, `st.button`

---

### 🛡️ Projeto 2 — Dashboard de Cyber Attacks
**Arquivo:** `Projeto 2 Dashboard de Cyber Attacks/app.py`

Dashboard interativo com dados reais de ameaças cibernéticas globais (2015–2024).

**Dataset:** [Kaggle - Global Cybersecurity Threats](https://www.kaggle.com/datasets/atharvasoundankar/global-cybersecurity-threats-2015-2024)
> Baixe o CSV e salve como `cyber_attacks.csv` na pasta do projeto.

**Funcionalidades:**
- Sidebar com filtros por país, ano e tipo de ataque
- 3 KPIs no topo (total de ataques, países, prejuízo)
- Gráfico de barras por país
- Gráfico de pizza por tipo de ataque
- Mapa mundi coroplético interativo
- Tabela de dados filtrados

**Conceitos:** `st.sidebar`, `st.columns`, `st.metric`, `plotly.express`, `pandas`

---

### 🤖 Projeto 3 — Chatbot Web com IA
**Arquivo:** `Projeto 3 Chatbot Web com IA/app.py`

Chatbot estilo ChatGPT integrado com Google Gemini.

**Requer:** `GEMINI_API_KEY` no `.env` ou na sidebar do app.
> Chave gratuita em: [aistudio.google.com](https://aistudio.google.com)

**Funcionalidades:**
- Bubbles de chat com `st.chat_message`
- Campo fixo na parte inferior com `st.chat_input`
- Histórico de mensagens via `st.session_state`
- Seletor de modelo (gemini-2.0-flash / gemini-2.0-flash-lite)
- Botão para limpar a conversa

**Conceitos:** `st.chat_message`, `st.chat_input`, `session_state`, walrus operator `:=`

---

### 📄 Projeto 4 — Analisador de PDF com IA
**Arquivo:** `Projeto 4 Analisador de PDF com IA/app.py`

Faz upload de PDFs, extrai o texto e usa IA para resumir e responder perguntas.

**Requer:** `GEMINI_API_KEY` no `.env` ou na sidebar do app.

**Funcionalidades:**
- Upload de PDF com `st.file_uploader`
- Extração de texto com `pypdf`
- Resumo automático: tipo do documento, 5 bullet points, pontos de atenção
- Chat para perguntas sobre o documento
- Histórico de PDFs analisados na sidebar (com data e resumo)

**Casos de uso:** contratos, laudos técnicos, políticas, petições, currículos

**Conceitos:** `st.file_uploader`, `pypdf`, `session_state`, Google Gemini API

---

### 🔗 Projeto 5 — SOC Investigator (Streamlit + n8n)
**Arquivo:** `Projeto 5 Streamlit + Agente n8n (Integração!)/app.py`

Interface web que integra com um agente de segurança no n8n via webhook.

**Requer:** URL do webhook do n8n (inserida na sidebar do app).

**Funcionalidades:**
- Campo para IP ou URL a investigar
- Envio via POST para o agente n8n
- Exibição do resultado JSON formatado
- Histórico de investigações na sidebar
- Exportação do relatório em PDF

**Arquitetura:** `Streamlit App → POST webhook → Agente n8n → JSON`

**Conceitos:** `requests.post`, `fpdf2`, integração com n8n, webhooks

---

## 🎨 Design

Tema **Cyberpunk** com as cores:
- Fundo: preto profundo `#050510`
- Destaque 1: rosa neon `#ff006e`
- Destaque 2: azul neon `#00d4ff`
- Fonte: Orbitron (títulos) + Rajdhani (texto)

---

## 🔐 Segurança

- Chaves de API ficam no `.env` (nunca no código)
- `.env` está no `.gitignore` — jamais será enviado ao GitHub
- Use `.env.example` como template

---

## 📦 Dependências

```
streamlit, pandas, plotly, google-genai, pypdf, fpdf2, requests, python-dotenv
```

---

*Kensei CyberSec Lab | AI Foundations 2026 | Semana 7*
