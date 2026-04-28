import time
import pandas as pd

from src.detector import IntrusionDetector
from src.alert_manager import AlertManager


class LiveMonitor:
    def __init__(self, dataset_path):
        """
        Initialize live monitoring system
        """
        print("Loading dataset...")
        self.dataset = pd.read_parquet(dataset_path)

        self.detector = IntrusionDetector()
        self.alert_manager = AlertManager()

    def start(self, interval=2):
        """
        Start real-time monitoring simulation
        """

        print("Starting live monitoring...")

        for _, row in self.dataset.iterrows():
            input_data = row.drop(
                ["label", "attack_cat"],
                errors="ignore"
            ).to_dict()

            result = self.detector.predict(input_data)

            print(
                f"Class: {result['label']} | "
                f"Probability: "
                f"{result['attack_probability']:.4f}"
            )

            self.alert_manager.create_alert(result)

            time.sleep(interval)