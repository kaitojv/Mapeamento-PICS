"""
Mapeamento de PICS – UNICAMP
Salva os dados em mapeamento_pics.csv (append por envio).
Execute com:  streamlit run app.py
"""

import csv
import os
from datetime import date

import pandas as pd
import streamlit as st

# ──────────────────────────────────────────────
# CONSTANTES
# ──────────────────────────────────────────────

CSV_FILE = "mapeamento_pics.csv"

CARGOS = [
    "Coordenador", "Enfermeiro", "TO", "Técnico de Enf", "Auxiliar de Enf",
    "Médico", "Fisioterapeuta", "Dentista", "Nutricionista", "Psicólogo",
    "ACS", "Agente de Apoio", "Farmacêutico", "Auxiliar de Farmácia", "Outros",
]

PICS_LIST = [
    "Acupuntura", "Auriculoterapia", "Homeopatia",
    "Plantas Medicinais / Fitoterapia", "Meditação", "Yoga",
    "Tai Chi Chuan", "Lian Gong", "Arteterapia", "Musicoterapia",
    "Biodança", "Dança Circular", "Terapia Comunitária Integrativa",
    "Reflexologia", "Reiki", "Shantala", "Apiterapia", "Aromaterapia",
    "Cromoterapia", "Geoterapia", "Hidroterapia", "Outra",
]

FREQUENCIA_OPT = [
    "Mais de uma vez ao dia", "Diariamente", "Semanalmente",
    "Quinzenalmente", "Mensalmente", "Eventualmente",
    "Não há frequência definida",
]
DURACAO_OPT   = ["Até 30 minutos", "30 min a 1 hora", "2 horas", "Mais de duas horas", "Variável"]
PERIODO_OPT   = ["Manhã", "Tarde", "Mais de um período", "Outro"]
LOCAL_OPT     = [
    "Sala de grupos", "Consultório", "Sala específica da unidade",
    "Área externa da unidade", "Espaço comunitário", "Parceria externa",
    "Domicílios do usuário", "Direcionados a outra unidade", "Outros",
]
PUBLICO_OPT   = [
    "Público geral", "Público de grupos", "Adultos", "Crianças",
    "Idosos", "Pessoas com doenças crônicas", "Gestantes",
    "Profissionais da unidade",
]
N_USUARIOS_OPT = ["Até 5", "6 a 10", "11 a 20", "Mais de 20", "Variável"]
FREQ_PART_OPT  = ["Esporádica", "Regular", "Irregular", "Alta adesão na unidade"]

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────

def save_to_csv(data: dict):
    """Acrescenta uma linha ao CSV, criando o arquivo/cabeçalho se necessário."""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


def slug(text: str) -> str:
    """Gera prefixo seguro para colunas CSV."""
    return (
        text.replace(" ", "_")
            .replace("/", "_")
            .replace("–", "_")
            .replace(".", "")
            .lower()
    )

# ──────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Mapeamento PICS – UNICAMP",
    page_icon="🌿",
    layout="centered",
)

st.markdown(
    """
    <style>
        /* Centraliza e limita largura em mobile */
        .block-container { padding: 1rem 1rem 3rem; max-width: 780px; margin: auto; }
        h1  { color: #1B5E20; }
        h2  { color: #2E7D32; border-bottom: 2px solid #A5D6A7; padding-bottom: 4px; margin-top: 1.5rem; }
        h3  { color: #388E3C; }
        /* Botão principal */
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #2E7D32; border: none;
            font-size: 1.1rem; padding: .6rem 1.2rem;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #1B5E20;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌿 Mapeamento de PICS")
st.markdown("**Pesquisa sobre Práticas Integrativas e Complementares em Saúde · UNICAMP**")
st.caption("Campos marcados com * são obrigatórios.")
st.divider()

# ──────────────────────────────────────────────
# PARTE 1 – IDENTIFICAÇÃO
# ──────────────────────────────────────────────

st.header("📋 Parte 1 · Identificação do Profissional")

c1, c2 = st.columns(2)
with c1:
    iniciais        = st.text_input("Iniciais do entrevistado *")
    unidade_trab    = st.text_input("Unidade de Trabalho *")
    distrito        = st.text_input("Distrito da Unidade")
    formacao        = st.text_input("Formação Acadêmica")
    cargo           = st.selectbox("Cargo na Prefeitura *", ["— selecione —"] + CARGOS)
with c2:
    tempo_unidade   = st.text_input("Tempo de Trabalho na Unidade")
    tempo_pref      = st.text_input("Tempo de Trabalho na Prefeitura")
    ano_formacao    = st.number_input("Ano de Formação", min_value=1950, max_value=2030,
                                      value=2000, step=1, format="%d")
    data_nasc       = st.date_input("Data de Nascimento",
                                    value=date(1985, 1, 1),
                                    min_value=date(1940, 1, 1),
                                    max_value=date(2005, 12, 31))
    nome_unidade    = st.text_input("Nome da Unidade")

st.divider()

# ──────────────────────────────────────────────
# PARTE 2 – MAPEAMENTO DE PICS
# ──────────────────────────────────────────────

st.header("🌱 Parte 2 · Mapeamento de PICS")
st.markdown("Selecione todas as PICS ofertadas na unidade:")

# Grade de checkboxes (2 colunas)
pics_selecionadas = []
cb_cols = st.columns(2)
for i, pic in enumerate(PICS_LIST):
    with cb_cols[i % 2]:
        if st.checkbox(pic, key=f"chk_{i}"):
            pics_selecionadas.append(pic)

pics_data: dict[str, dict] = {}

if pics_selecionadas:
    st.markdown("---")
    st.subheader("🔍 Detalhamento por PIC selecionada")
    st.caption("Preencha as informações de cada prática marcada acima.")

    for pic in pics_selecionadas:
        with st.expander(f"📌 {pic}", expanded=False):
            prof_pic = st.multiselect(
                "Profissional(is) que ofertam",
                options=CARGOS, key=f"prof_{pic}")
            freq = st.selectbox(
                "Frequência de oferta",
                ["— selecione —"] + FREQUENCIA_OPT, key=f"freq_{pic}")
            dur  = st.selectbox(
                "Duração da prática",
                ["— selecione —"] + DURACAO_OPT,   key=f"dur_{pic}")
            per  = st.selectbox(
                "Período",
                ["— selecione —"] + PERIODO_OPT,   key=f"per_{pic}")
            loc  = st.multiselect(
                "Local de oferecimento",
                options=LOCAL_OPT,                  key=f"loc_{pic}")
            pub  = st.multiselect(
                "Público-alvo",
                options=PUBLICO_OPT,                key=f"pub_{pic}")
            nu   = st.selectbox(
                "Número de usuários por sessão",
                ["— selecione —"] + N_USUARIOS_OPT, key=f"nu_{pic}")
            fp   = st.selectbox(
                "Frequência de participação dos usuários",
                ["— selecione —"] + FREQ_PART_OPT,  key=f"fp_{pic}")

            pics_data[pic] = dict(
                profissionais=prof_pic, frequencia=freq,
                duracao=dur,           periodo=per,
                local=loc,             publico=pub,
                n_usuarios=nu,         freq_participacao=fp,
            )

st.divider()

# ──────────────────────────────────────────────
# PARTE 3 – FINALIZAÇÃO
# ──────────────────────────────────────────────

st.header("✅ Parte 3 · Finalização")
referencia   = st.text_input(
    "Profissional de referência para a 2ª fase do projeto")
observacoes  = st.text_area("Observações gerais", height=130)

st.divider()

# ──────────────────────────────────────────────
# ENVIO
# ──────────────────────────────────────────────

if st.button("📤 Enviar Questionário", use_container_width=True, type="primary"):

    # Validação mínima
    erros = []
    if not iniciais.strip():
        erros.append("Iniciais do entrevistado")
    if not unidade_trab.strip():
        erros.append("Unidade de Trabalho")
    if cargo == "— selecione —":
        erros.append("Cargo na Prefeitura")

    if erros:
        st.error(f"⚠️ Preencha os campos obrigatórios: {', '.join(erros)}.")
    else:
        # Monta a linha base
        row = {
            "timestamp":        pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "iniciais":         iniciais.strip(),
            "unidade_trabalho": unidade_trab.strip(),
            "distrito":         distrito.strip(),
            "formacao":         formacao.strip(),
            "cargo":            cargo,
            "tempo_unidade":    tempo_unidade.strip(),
            "tempo_prefeitura": tempo_pref.strip(),
            "ano_formacao":     int(ano_formacao),
            "data_nascimento":  str(data_nasc),
            "nome_unidade":     nome_unidade.strip(),
            "pics_ofertadas":   "; ".join(pics_selecionadas),
        }

        # Colunas dinâmicas para cada PIC
        for pic, d in pics_data.items():
            p = slug(pic)
            row[f"{p}__profissionais"]     = "; ".join(d["profissionais"])
            row[f"{p}__frequencia"]        = d["frequencia"]
            row[f"{p}__duracao"]           = d["duracao"]
            row[f"{p}__periodo"]           = d["periodo"]
            row[f"{p}__local"]             = "; ".join(d["local"])
            row[f"{p}__publico"]           = "; ".join(d["publico"])
            row[f"{p}__n_usuarios"]        = d["n_usuarios"]
            row[f"{p}__freq_participacao"] = d["freq_participacao"]

        row["referencia_2a_fase"] = referencia.strip()
        row["observacoes"]        = observacoes.strip()

        save_to_csv(row)

        st.success("🎉 Questionário enviado com sucesso! Obrigado pela participação.")
        st.balloons()

        # Botão para baixar o CSV atualizado
        with open(CSV_FILE, "rb") as f:
            st.download_button(
                label="⬇️ Baixar mapeamento_pics.csv",
                data=f,
                file_name="mapeamento_pics.csv",
                mime="text/csv",
            )