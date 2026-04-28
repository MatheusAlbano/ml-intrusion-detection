import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import pandas as pd
import streamlit as st
import plotly.express as px

from src.analytics import AlertAnalytics


st.set_page_config(
    page_title="Intrusion Detection Dashboard",
    layout="wide"
)


@st.cache_data(ttl=5)
def load_alerts():
    alerts_folder = Path("alerts")
    alerts = []

    for file in alerts_folder.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            alerts.append(json.load(f))

    if not alerts:
        return pd.DataFrame()

    df = pd.DataFrame(alerts)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def main():
    st.title("Intrusion Detection Monitoring Dashboard")

    analytics = AlertAnalytics()
    report = analytics.generate_report()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Alerts", report["total_alerts"])
    col2.metric("Critical Alerts", report["critical"])
    col3.metric("High Alerts", report["high"])
    col4.metric("Average Probability", report["average_probability"])

    df = load_alerts()

    if df.empty:
        st.warning("No alerts found.")
        return

    st.sidebar.header("Filters")

    severity_filter = st.sidebar.multiselect(
        "Select severity",
        options=df["severity"].unique(),
        default=df["severity"].unique()
    )

    probability_filter = st.sidebar.slider(
        "Minimum probability",
        min_value=0.0,
        max_value=1.0,
        value=0.0
    )

    filtered_df = df[
        (df["severity"].isin(severity_filter)) &
        (df["probability"] >= probability_filter)
    ]

    st.subheader("Recent Alerts")
    st.dataframe(
        filtered_df.sort_values(
            by="timestamp",
            ascending=False
        )
    )

    st.subheader("Severity Distribution")

    severity_chart = px.histogram(
        filtered_df,
        x="severity"
    )

    st.plotly_chart(
        severity_chart,
        use_container_width=True
    )

    st.subheader("Attack Probability Distribution")

    probability_chart = px.histogram(
        filtered_df,
        x="probability"
    )

    st.plotly_chart(
        probability_chart,
        use_container_width=True
    )

    st.subheader("Attack Timeline")

    timeline_chart = px.line(
        filtered_df.sort_values("timestamp"),
        x="timestamp",
        y="probability"
    )

    st.plotly_chart(
        timeline_chart,
        use_container_width=True
    )


if __name__ == "__main__":
    main()