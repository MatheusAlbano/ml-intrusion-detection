import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


class AlertAnalytics:

    def __init__(self, alerts_folder="alerts", reports_folder="reports"):
        self.alerts_folder = Path(alerts_folder)
        self.reports_folder = Path(reports_folder)

        # Create reports folder if it does not exist
        self.reports_folder.mkdir(exist_ok=True)

    def load_alerts(self):
        alerts = []

        for file in self.alerts_folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                alert = json.load(f)
                alerts.append(alert)

        return alerts

    def generate_report(self):
        alerts = self.load_alerts()

        if not alerts:
            return None

        df = pd.DataFrame(alerts)

        report = {
            "total_alerts": len(df),
            "critical": len(df[df["severity"] == "critical"]),
            "high": len(df[df["severity"] == "high"]),
            "medium": len(df[df["severity"] == "medium"]),
            "average_probability": round(
                df["probability"].mean(), 4
            )
        }

        return report

    def export_csv(self):
        alerts = self.load_alerts()

        if not alerts:
            return None

        df = pd.DataFrame(alerts)

        output_path = self.reports_folder / "alerts_report.csv"
        df.to_csv(output_path, index=False)

        return output_path

    def generate_severity_chart(self):
        alerts = self.load_alerts()

        if not alerts:
            return None

        df = pd.DataFrame(alerts)

        severity_counts = df["severity"].value_counts()

        plt.figure(figsize=(8, 6))
        severity_counts.plot(kind="bar")

        plt.title("Alert Severity Distribution")
        plt.xlabel("Severity")
        plt.ylabel("Count")

        output_path = self.reports_folder / "severity_chart.png"
        plt.savefig(output_path)
        plt.close()

        return output_path