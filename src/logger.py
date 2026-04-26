import csv
from datetime import datetime
from pathlib import Path


LOG_FILE = Path("reports/intrusion_logs.csv")


class IntrusionLogger:
    """
    Responsible for saving IDS events into a log file.
    """

    def __init__(self):
        # Create log file if it does not exist
        if not LOG_FILE.exists():
            with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "timestamp",
                    "prediction",
                    "label",
                    "attack_probability"
                ])

        print("✅ Logger inicializado com sucesso!")

    def save_event(self, result: dict):
        """
        Save intrusion detection result into CSV log.
        """

        with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow([
                datetime.now().isoformat(),
                result["prediction"],
                result["label"],
                result["attack_probability"]
            ])

        print("📝 Evento registrado no log!")