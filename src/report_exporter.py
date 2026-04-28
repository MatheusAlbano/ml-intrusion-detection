import json
from pathlib import Path
import pandas as pd


class ReportExporter:

    def __init__(self, alerts_folder="alerts", output_folder="reports"):
        self.alerts_folder = Path(alerts_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)

    def load_alerts(self):
        alerts = []

        for file in self.alerts_folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                alert = json.load(f)
                alerts.append(alert)

        if not alerts:
            return pd.DataFrame()

        return pd.DataFrame(alerts)

    def export_csv(self):
        df = self.load_alerts()

        if df.empty:
            return None

        output_file = self.output_folder / "alerts_report.csv"
        df.to_csv(output_file, index=False)

        return output_file

    def export_excel(self):
        df = self.load_alerts()

        if df.empty:
            return None

        output_file = self.output_folder / "alerts_report.xlsx"
        df.to_excel(output_file, index=False)

        return output_file