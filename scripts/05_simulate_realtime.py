import time
import pandas as pd

from src.config import TRAIN_FILE
from src.detector import IntrusionDetector
from src.logger import IntrusionLogger


def main():
    print(" Carregando dataset para simulação...")

    # Load original dataset
    df = pd.read_parquet(TRAIN_FILE)

    # Remove target column
    df = df.drop(columns=["label"], errors="ignore")

    # Initialize detector and logger
    detector = IntrusionDetector()
    logger = IntrusionLogger()

    print("\n Iniciando simulação de tráfego em tempo real...\n")

    # Simulate first 20 traffic samples
    for index, row in df.head(20).iterrows():
        sample = row.to_dict()

        # Predict traffic type
        result = detector.predict(sample)

        print(
            f"[{index}] "
            f"Classe: {result['label']} | "
            f"Probabilidade de ataque: {result['attack_probability']:.4f}"
        )

        # Save event to log
        logger.save_event(result)

        # Simulate interval between packets
        time.sleep(1)

    print("\n Simulação concluída com sucesso!")


if __name__ == "__main__":
    main()