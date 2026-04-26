# Alert system module

from pathlib import Path
from datetime import datetime
import json


class AlertManager:
    def __init__(self, alert_dir="alerts"):
        """
        Initialize alert manager
        """
        self.alert_dir = Path(alert_dir)
        self.alert_dir.mkdir(exist_ok=True)

        print("Sistema de alertas inicializado!")

    def create_alert(self, prediction_result):
        """
        Create an alert if intrusion is detected
        """

        if prediction_result["label"] != "attack":
            return None

        attack_probability = prediction_result["attack_probability"]

        severity = self.define_severity(attack_probability)

        alert_data = {
            "timestamp": datetime.now().isoformat(),
            "type": "intrusion_detected",
            "severity": severity,
            "probability": attack_probability,
            "prediction": prediction_result["prediction"],
            "label": prediction_result["label"]
        }

        file_name = (
            f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        )

        alert_path = self.alert_dir / file_name

        with open(alert_path, "w", encoding="utf-8") as file:
            json.dump(alert_data, file, indent=4)

        print(f"🚨 ALERTA GERADO! Severidade: {severity}")
        print(f"Arquivo salvo em: {alert_path}")

        return alert_data

    def define_severity(self, probability):
        """
        Define alert severity level
        """

        if probability >= 0.95:
            return "critical"
        elif probability >= 0.80:
            return "high"
        elif probability >= 0.60:
            return "medium"
        else:
            return "low"