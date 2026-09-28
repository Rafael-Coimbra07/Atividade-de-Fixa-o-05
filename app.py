import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Fintech Analytics",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
TRANSACOES = BASE_DIR / "transacoes.csv"

RISCO_DICT = {
    "C100": "Baixo",
    "C101": "Alto",
    "C102": "Médio",
    "C103": "Baixo",
    "C104": "Alto",
}


@st.cache_data
def carregar_e_tratar_dados():
    """Ingere e transforma os dados conforme os requisitos do exercício."""
    df = pd.read_csv(TRANSACOES, encoding="latin1")

    # Imputação da mediana do valor por estado.
    medianas_estado = df.groupby("estado_cliente")["valor"].transform("median")
    df["valor"] = df["valor"].fillna(medianas_estado)

    # Rastreabilidade.
    df["plataforma"] = "Mobile"

    # Data/hora e fuso de São Paulo.
    df["data_transacao"] = pd.to_datetime(df["data_transacao"], errors="coerce")
    df["data_transacao"] = df["data_transacao"].dt.tz_localize("America/Sao_Paulo")

    # Informações temporais usando .dt.
    df["dia_semana"] = df["data_transacao"].dt.day_name()
    df["mes"] = df["data_transacao"].dt.month

    # Remove duplicidades, mantendo a primeira ocorrência.
    df = df.drop_duplicates(keep="first").copy()

    # Cruzamento com categorias de risco usando .map().
    df["nivel_risco"] = df["id_cliente"].map(RISCO_DICT)

    # Z-Score vetorizado por estado, sem loops.
    media_estado = df.groupby("estado_cliente")["valor"].transform("mean")
    desvio_estado = df.groupby("estado_cliente")["valor"].transform("std")

    # Evita divisão problemática caso algum grupo tenha desvio zero.
    desvio_seguro = desvio_estado.replace(0, np.nan)
    df["z_score"] = (df["valor"] - media_estado) / desvio_seguro
    df["anomalia"] = df["z_score"] > 2.5

    return df


def gerar_pivot(df):
    """Tabela dinâmica mensal por nível de risco."""
    return pd.pivot_table(
        df,
        index="mes",
        columns="nivel_risco",
        values="valor",
        aggfunc="sum",
        margins=True,
        margins_name="Total"
    )


def formatar_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# -----------------------------
# Interface
# -----------------------------
st.title("📊 Fintech Analytics")
st.caption("Pipeline de dados, desempenho transacional e detecção de anomalias")

try:
    df = carregar_e_tratar_dados()
except FileNotFoundError:
    st.error(
        "O arquivo transacoes.csv não foi encontrado. "
        "Execute primeiro: python criar_dados.py"
    )
    st.stop()

# Filtro obrigatório do exercício:
# Setembro + (SP OU RJ) + valor > 5000, usando & e | vetorizados.
filtro_setembro_sp_rj = (
    (df["mes"] == 9)
    & ((df["estado_cliente"] == "SP") | (df["estado_cliente"] == "RJ"))
    & (df["valor"] > 5000)
)
df_filtrado = df[filtro_setembro_sp_rj].copy()

anomalias = df[df["z_score"] > 2.5].copy()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Transações processadas", f"{len(df):,}".replace(",", "."))
col2.metric("Faturamento total", formatar_reais(df["valor"].sum()))
col3.metric("Filtro Setembro / SP-RJ / > R$ 5 mil", f"{len(df_filtrado):,}".replace(",", "."))
col4.metric("Potenciais anomalias", f"{len(anomalias):,}".replace(",", "."))

st.divider()

# -----------------------------
# Gráfico OO Matplotlib
# -----------------------------
st.subheader("📈 Volume diário de transações")

diario = (
    df.assign(data=df["data_transacao"].dt.date)
      .groupby("data", as_index=True)["valor"]
      .sum()
      .sort_index()
)
media_movel = diario.rolling(7).mean()

fig, ax = plt.subplots(figsize=(12, 4.8))
ax.plot(diario.index, diario.values, label="Valor total diário")
ax.plot(media_movel.index, media_movel.values, label="Média móvel de 7 dias")
ax.set_ylim(bottom=0)
ax.set_title("Valor total de transações e média móvel de 7 dias")
ax.set_xlabel("Data")
ax.set_ylabel("Valor (R$)")
ax.legend()
ax.grid(alpha=0.25)
fig.autofmt_xdate()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# -----------------------------
# Filtro obrigatório
# -----------------------------
st.subheader("🔎 Transações filtradas")
st.write(
    "Setembro + estado SP ou RJ + valor superior a R$ 5.000,00 "
    "(filtro vetorizado com `&` e `|`)."
)

st.dataframe(
    df_filtrado[
        [
            "id_cliente", "data_transacao", "valor", "origem",
            "estado_cliente", "plataforma", "nivel_risco"
        ]
    ].sort_values("valor", ascending=False),
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Pivot table
# -----------------------------
st.subheader("📊 Tabela dinâmica por mês e nível de risco")

pivot = gerar_pivot(df)
pivot_display = pivot.copy()

st.dataframe(
    pivot_display.style.format(lambda x: formatar_reais(x) if pd.notna(x) else ""),
    use_container_width=True
)

# -----------------------------
# Anomalias
# -----------------------------
st.subheader("🚨 Potenciais anomalias / fraudes")
st.caption("Critério: Z-Score > 2,5 calculado vetorizadamente por estado.")

if anomalias.empty:
    st.success("Nenhuma transação ultrapassou o limite de Z-Score > 2,5.")
else:
    st.dataframe(
        anomalias[
            [
                "id_cliente", "data_transacao", "valor",
                "estado_cliente", "nivel_risco", "z_score"
            ]
        ].sort_values("z_score", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# Auditoria do pipeline
# -----------------------------
with st.expander("🧪 Detalhes do tratamento dos dados"):
    st.write(f"Registros finais após remoção de duplicidades: **{len(df)}**")
    st.write(f"Valores ausentes em `valor`: **{df['valor'].isna().sum()}**")
    st.write(f"Plataforma definida: **{df['plataforma'].unique()[0]}**")
    st.write(f"Fuso horário: **{df['data_transacao'].dt.tz}**")
    st.write(f"Clientes mapeados com risco: **{df['nivel_risco'].notna().sum()}**")

st.caption("Projeto acadêmico — pipeline desenvolvido com Pandas, NumPy, Matplotlib e Streamlit.")
