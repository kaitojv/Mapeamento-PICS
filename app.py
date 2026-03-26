"""
Mapeamento de PICS – UNICAMP
Salva os dados em mapeamento_pics.csv (append por envio).
Execute com:  streamlit run app.py
"""

import csv
import os
import uuid
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
DURACAO_OPT  = ["Até 30 minutos", "30 min a 1 hora", "2 horas", "Mais de duas horas", "Variável"]
PERIODO_OPT  = ["Manhã", "Tarde", "Mais de um período", "Outro"]
LOCAL_OPT    = [
    "Sala de grupos", "Consultório", "Sala específica da unidade",
    "Área externa da unidade", "Espaço comunitário", "Parceria externa",
    "Domicílios do usuário", "Direcionados a outra unidade", "Outros",
]
PUBLICO_OPT  = [
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
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def slug(text: str) -> str:
    return (
        text.replace(" ", "_").replace("/", "_")
            .replace("–", "_").replace(".", "").lower()
    )

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────

if "pics_instancias" not in st.session_state:
    st.session_state.pics_instancias = []   # lista de {"id": uuid_str, "pic": nome}

if "envio_ok" not in st.session_state:
    st.session_state.envio_ok = False

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
        .block-container { padding: 1rem 1rem 3rem; max-width: 780px; margin: auto; }
        h1  { color: #1B5E20; }
        h2  { color: #2E7D32; border-bottom: 2px solid #A5D6A7; padding-bottom: 4px; margin-top:1.5rem; }
        h3  { color: #388E3C; }
        .pic-card {
            background: #F1F8E9; border-left: 4px solid #66BB6A;
            border-radius: 6px; padding: .6rem 1rem; margin-bottom: .5rem;
        }
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #2E7D32; border: none;
            font-size: 1.1rem; padding: .6rem 1.2rem;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover { background-color: #1B5E20; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌿 Mapeamento de PICS")
st.markdown("**Pesquisa sobre Práticas Integrativas e Complementares em Saúde · UNICAMP**")
st.caption("Campos marcados com * são obrigatórios.")

# ──────────────────────────────────────────────
# ABAS PRINCIPAIS
# ──────────────────────────────────────────────

tab_form, tab_dados = st.tabs(["📝 Questionário", "📊 Dados Coletados"])

# ══════════════════════════════════════════════
# ABA 1 – QUESTIONÁRIO
# ══════════════════════════════════════════════

with tab_form:

    # ── PARTE 1 ───────────────────────────────
    st.header("📋 Parte 1 · Identificação do Profissional")

    c1, c2 = st.columns(2)
    with c1:
        iniciais     = st.text_input("Iniciais do entrevistado *")
        unidade_trab = st.text_input("Unidade de Trabalho *")
        distrito     = st.text_input("Distrito da Unidade")
        formacao     = st.text_input("Formação Acadêmica")
        cargo        = st.selectbox("Cargo na Prefeitura *", ["— selecione —"] + CARGOS)
    with c2:
        tempo_unidade = st.text_input("Tempo de Trabalho na Unidade")
        tempo_pref    = st.text_input("Tempo de Trabalho na Prefeitura")
        ano_formacao  = st.number_input("Ano de Formação", min_value=1950,
                                        max_value=2030, value=2000, step=1, format="%d")
        data_nasc     = st.date_input("Data de Nascimento",
                                      value=date(1985, 1, 1),
                                      min_value=date(1940, 1, 1),
                                      max_value=date(2005, 12, 31))
        nome_unidade  = st.text_input("Nome da Unidade")

    st.divider()

    # ── PARTE 2 ───────────────────────────────
    st.header("🌱 Parte 2 · Mapeamento de PICS")
    st.markdown(
        "Adicione cada PIC ofertada na unidade. "
        "**A mesma PIC pode ser adicionada mais de uma vez** (ex.: Acupuntura individual e em grupo)."
    )

    # Seletor + botão adicionar
    add_col, btn_col = st.columns([3, 1])
    with add_col:
        pic_escolhida = st.selectbox("Selecione uma PIC para adicionar",
                                     PICS_LIST, key="pic_add_select", label_visibility="collapsed")
    with btn_col:
        if st.button("➕ Adicionar", use_container_width=True):
            st.session_state.pics_instancias.append(
                {"id": str(uuid.uuid4())[:8], "pic": pic_escolhida}
            )
            st.rerun()

    # Lista de instâncias adicionadas
    pics_data: dict[str, dict] = {}

    if not st.session_state.pics_instancias:
        st.info("Nenhuma PIC adicionada ainda. Use o seletor acima.")
    else:
        for idx, inst in enumerate(st.session_state.pics_instancias):
            iid  = inst["id"]
            pic  = inst["pic"]
            num  = sum(1 for x in st.session_state.pics_instancias[:idx+1] if x["pic"] == pic)
            label = f"📌 {pic}" + (f" (modalidade {num})" if num > 1 else "")

            with st.expander(label, expanded=True):
                rem_col, _ = st.columns([1, 4])
                with rem_col:
                    if st.button("🗑️ Remover", key=f"rem_{iid}"):
                        st.session_state.pics_instancias = [
                            x for x in st.session_state.pics_instancias if x["id"] != iid
                        ]
                        st.rerun()

                prof = st.multiselect("Profissional(is) que ofertam",
                                      options=CARGOS, key=f"prof_{iid}")
                freq = st.selectbox("Frequência de oferta",
                                    ["— selecione —"] + FREQUENCIA_OPT, key=f"freq_{iid}")
                dur  = st.selectbox("Duração da prática",
                                    ["— selecione —"] + DURACAO_OPT,    key=f"dur_{iid}")
                per  = st.selectbox("Período",
                                    ["— selecione —"] + PERIODO_OPT,    key=f"per_{iid}")
                loc  = st.multiselect("Local de oferecimento",
                                      options=LOCAL_OPT,                 key=f"loc_{iid}")
                pub  = st.multiselect("Público-alvo",
                                      options=PUBLICO_OPT,               key=f"pub_{iid}")
                nu   = st.selectbox("Número de usuários por sessão",
                                    ["— selecione —"] + N_USUARIOS_OPT,  key=f"nu_{iid}")
                fp   = st.selectbox("Frequência de participação dos usuários",
                                    ["— selecione —"] + FREQ_PART_OPT,   key=f"fp_{iid}")

                pics_data[iid] = dict(
                    pic=pic, profissionais=prof, frequencia=freq,
                    duracao=dur, periodo=per, local=loc,
                    publico=pub, n_usuarios=nu, freq_participacao=fp,
                )

    st.divider()

    # ── PARTE 3 ───────────────────────────────
    st.header("✅ Parte 3 · Finalização")
    referencia  = st.text_input("Profissional de referência para a 2ª fase do projeto")
    observacoes = st.text_area("Observações gerais", height=130)

    st.divider()

    # ── ENVIO ─────────────────────────────────
    if st.button("📤 Enviar Questionário", use_container_width=True, type="primary"):
        erros = []
        if not iniciais.strip():     erros.append("Iniciais do entrevistado")
        if not unidade_trab.strip(): erros.append("Unidade de Trabalho")
        if cargo == "— selecione —": erros.append("Cargo na Prefeitura")

        if erros:
            st.error(f"⚠️ Preencha os campos obrigatórios: {', '.join(erros)}.")
        elif not st.session_state.pics_instancias:
            st.warning("⚠️ Adicione pelo menos uma PIC antes de enviar.")
        else:
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
                "pics_ofertadas":   "; ".join(
                    inst["pic"] for inst in st.session_state.pics_instancias
                ),
            }

            # Colunas dinâmicas: prefixo = slug(pic)__N__ para suportar múltiplas instâncias
            pic_count: dict[str, int] = {}
            for iid, d in pics_data.items():
                pname = d["pic"]
                pic_count[pname] = pic_count.get(pname, 0) + 1
                p = f"{slug(pname)}__{pic_count[pname]}"
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

            # Limpa instâncias após envio
            st.session_state.pics_instancias = []
            st.session_state.envio_ok = True
            st.rerun()

    if st.session_state.envio_ok:
        st.success("🎉 Questionário enviado com sucesso! Obrigado pela participação.")
        st.balloons()
        st.session_state.envio_ok = False

# ══════════════════════════════════════════════
# ABA 2 – DADOS COLETADOS
# ══════════════════════════════════════════════

with tab_dados:
    st.header("📊 Dados Coletados")

    if not os.path.isfile(CSV_FILE):
        st.info("Nenhum dado coletado ainda. Os envios aparecerão aqui automaticamente.")
    else:
        df = pd.read_csv(CSV_FILE, encoding="utf-8-sig")
        st.metric("Total de respostas", len(df))

        st.markdown("##### Filtrar por Unidade de Trabalho")
        unidades = ["Todas"] + sorted(df["unidade_trabalho"].dropna().unique().tolist())
        filtro   = st.selectbox("Unidade", unidades, label_visibility="collapsed")

        df_view = df if filtro == "Todas" else df[df["unidade_trabalho"] == filtro]

        st.dataframe(df_view, use_container_width=True, hide_index=True)

        with open(CSV_FILE, "rb") as f:
            st.download_button(
                label="⬇️ Baixar CSV completo",
                data=f,
                file_name="mapeamento_pics.csv",
                mime="text/csv",
                use_container_width=True,
            )