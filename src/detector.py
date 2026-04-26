import joblib
import pandas as pd

from src.config import (
    MODEL_PATH,
    PIPELINE_PATH
)


class IntrusionDetector:

    def __init__(self):
        print("Carregando modelo treinado...")
        self.model = joblib.load(MODEL_PATH)

        print("Carregando pipeline de preprocessamento...")
        self.preprocessor = joblib.load(PIPELINE_PATH)

        print("Detector inicializado com sucesso!")

    def predict(self, input_data: dict):
        # Convert input into DataFrame
        df = pd.DataFrame([input_data])

        # Transform data using fitted pipeline
        processed_data = self.preprocessor.transform(df)

        # Predict class
        prediction = self.model.predict(processed_data)[0]

        # Predict probabilities
        probabilities = self.model.predict_proba(processed_data)[0]

        return {
            "prediction": int(prediction),
            "label": "attack" if prediction == 1 else "normal",
            "attack_probability": float(probabilities[1])
        }