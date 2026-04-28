import pandas as pd
from pathlib import Path


class ReportExporter:

    def __init__(self, alerts_folder="alerts"):
        self.alerts_folder = Path(alerts_folder)

    def load_alerts(self):
        files = list(
            self.alerts_folder.glob("*.json")
        )

        alerts = []

        for file in files:
            df = pd.read_json(file)
            alerts.append(df)

        if not alerts:
            return pd.DataFrame()

        return pd.concat(
            alerts,
            ignore_index=True
        )

    def export_csv(
        self,
        output_path="reports/alerts_report.csv"
    ):
        df = self.load_alerts()

        if df.empty:
            return None

        output = Path(output_path)
        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_csv(
            output,
            index=False
        )

        return output