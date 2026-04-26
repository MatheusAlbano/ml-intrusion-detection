import json
from pathlib import Path


class AlertAnalytics:

    def __init__(self, alerts_folder="alerts"):
        self.alerts_folder = Path(alerts_folder)

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
            return {
                "total_alerts": 0,
                "critical": 0,
                "high": 0,
                "medium": 0,
                "average_probability": 0
            }

        total_alerts = len(alerts)

        # Count alerts by severity safely
        critical = sum(
            1 for alert in alerts
            if alert.get("severity") == "critical"
        )

        high = sum(
            1 for alert in alerts
            if alert.get("severity") == "high"
        )

        medium = sum(
            1 for alert in alerts
            if alert.get("severity") == "medium"
        )

        # Collect probabilities safely
        valid_probabilities = [
            alert.get("probability", 0)
            for alert in alerts
        ]

        average_probability = (
            sum(valid_probabilities) / len(valid_probabilities)
            if valid_probabilities else 0
        )

        return {
            "total_alerts": total_alerts,
            "critical": critical,
            "high": high,
            "medium": medium,
            "average_probability": round(
                average_probability, 4
            )
        }