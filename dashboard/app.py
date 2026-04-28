import sys
from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

from src.analytics import AlertAnalytics
from src.report_exporter import ReportExporter
from src.pdf_report import PDFReportGenerator
from dashboard.feature_importance import render_feature_importance


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

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df


def main():
    # Auto-refresh dashboard every 5 seconds
    st_autorefresh(
        interval=5000,
        key="dashboard_refresh"
    )

    st.title(
        "Intrusion Detection Monitoring Dashboard"
    )

    # Sidebar controls
    st.sidebar.header("Monitoring Controls")

    monitoring = st.sidebar.checkbox(
        "Enable live monitoring",
        value=True
    )

    if monitoring:
        st.sidebar.success(
            "Live monitoring enabled"
        )
    else:
        st.sidebar.warning(
            "Live monitoring disabled"
        )

    analytics = AlertAnalytics()
    report = analytics.generate_report()

    # Main metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Alerts",
        report["total_alerts"]
    )

    col2.metric(
        "Critical Alerts",
        report["critical"]
    )

    col3.metric(
        "High Alerts",
        report["high"]
    )

    col4.metric(
        "Average Probability",
        report["average_probability"]
    )

    df = load_alerts()

    if df.empty:
        st.warning("No alerts found.")
        return

    # Filters
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

    # Export buttons
    st.subheader("Export Reports")

    col_export1, col_export2 = st.columns(2)

    with col_export1:
        if st.button("Export CSV Report"):
            exporter = ReportExporter()
            file_path = exporter.export_csv()

            if file_path:
                st.success(
                    f"CSV report exported: {file_path}"
                )
            else:
                st.warning(
                    "No alerts available for export."
                )

    with col_export2:
        if st.button("Export PDF Report"):
            pdf_generator = PDFReportGenerator()
            file_path = pdf_generator.generate()

            st.success(
                f"PDF report exported: {file_path}"
            )

    # Alerts table
    st.subheader("Recent Alerts")

    st.dataframe(
        filtered_df.sort_values(
            by="timestamp",
            ascending=False
        ),
        use_container_width=True
    )

    # Severity distribution
    st.subheader("Severity Distribution")

    severity_chart = px.histogram(
        filtered_df,
        x="severity"
    )

    st.plotly_chart(
        severity_chart,
        use_container_width=True
    )

    # Probability distribution
    st.subheader(
        "Attack Probability Distribution"
    )

    probability_chart = px.histogram(
        filtered_df,
        x="probability"
    )

    st.plotly_chart(
        probability_chart,
        use_container_width=True
    )

    # Attack timeline
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

    # Feature importance
    render_feature_importance()


if __name__ == "__main__":
    main()