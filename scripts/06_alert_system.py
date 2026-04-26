# Alert simulation script

import pandas as pd
import random

from src.config import TRAIN_FILE
from src.detector import IntrusionDetector
from src.alert_manager import AlertManager


def main():
    """
    Simulate alert generation from network traffic
    """

    print("Carregando dataset...")

    df = pd.read_parquet(TRAIN_FILE)

    detector = IntrusionDetector()
    alert_manager = AlertManager()

    print("\nIniciando monitoramento com alertas...\n")

    samples = random.sample(range(len(df)), 20)

    for idx in samples:
        sample = df.iloc[idx].drop("label").to_dict()

        result = detector.predict(sample)

        print(
            f"[{idx}] Classe: {result['label']} | "
            f"Probabilidade: {result['attack_probability']:.4f}"
        )

        alert_manager.create_alert(result)

    print("\nSistema de alertas finalizado!")


if __name__ == "__main__":
    main()