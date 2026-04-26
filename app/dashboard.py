# Dashboard for IDS monitoring
import pandas as pd
import streamlit as st
from pathlib import Path

LOG_FILE = Path("reports/intrusion_logs.csv")

st.set_page_config(
    page_title="IDS Dashboard",
    layout="wide"
)

st.title("Intrusion Detection Dashboard")

# Check if log file exists
if not LOG_FILE.exists():
    st.warning("Arquivo de logs não encontrado.")
    st.stop()

# Load logs
df = pd.read_csv(LOG_FILE)

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Metrics
total_events = len(df)
total_attacks = len(df[df["label"] == "attack"])
total_normal = len(df[df["label"] == "normal"])

attack_rate = (
    (total_attacks / total_events) * 100
    if total_events > 0 else 0
)

# Top metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Eventos Totais", total_events)
col2.metric("Ataques Detectados", total_attacks)
col3.metric("Tráfego Normal", total_normal)
col4.metric("Taxa de Ataque (%)", f"{attack_rate:.2f}")

st.divider()

# Timeline chart
st.subheader("Eventos ao longo do tempo")

events_over_time = (
    df.groupby(df["timestamp"].dt.floor("min"))
    .size()
)

st.line_chart(events_over_time)

st.divider()

# Attack probability chart
st.subheader("Probabilidade de ataque")

st.line_chart(df["attack_probability"])

st.divider()

# Latest logs
st.subheader("Últimos eventos registrados")

st.dataframe(
    df.tail(20),
    use_container_width=True
)