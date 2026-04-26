import joblib
import pandas as pd

from src.config import (
    MODEL_PATH,
    PIPELINE_PATH
)


class IntrusionDetector:

    def __init__(self):
        print("Loading trained model...")
        self.model = joblib.load(MODEL_PATH)

        print("Loading preprocessing pipeline...")
        self.preprocessor = joblib.load(PIPELINE_PATH)

        print("Detector initialized successfully!")

    def predict(self, input_data: dict):
        # Convert input data into DataFrame
        df = pd.DataFrame([input_data])

        # Apply preprocessing pipeline
        processed_data = self.preprocessor.transform(df)

        # Preserve feature names to avoid sklearn warnings
        if hasattr(self.model, "feature_names_in_"):
            processed_data = pd.DataFrame(
                processed_data,
                columns=self.model.feature_names_in_
            )

        # Predict class label
        prediction = self.model.predict(processed_data)[0]

        # Predict class probabilities
        probabilities = self.model.predict_proba(processed_data)[0]

        return {
            "prediction": int(prediction),
            "label": "attack" if prediction == 1 else "normal",
            "attack_probability": float(probabilities[1])
        }