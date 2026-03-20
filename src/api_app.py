import joblib
import pandas as pd

from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.config import PIPELINE_PATH, MODEL_PATH


app = FastAPI(
    title="ML Intrusion Detection API",
    version="1.0.0",
    description="API for intrusion detection using machine learning and UNSW-NB15"
)


class PredictionRequest(BaseModel):
    features: Dict[str, Any]


def load_artifacts():
    # Load preprocessing pipeline and trained model
    if not PIPELINE_PATH.exists():
        raise FileNotFoundError(f"Pipeline not found: {PIPELINE_PATH}")

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    pipeline = joblib.load(PIPELINE_PATH)
    model = joblib.load(MODEL_PATH)
    return pipeline, model


pipeline, model = load_artifacts()


@app.get("/health")
def health():
    # Return API health status
    return {"status": "ok"}


@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([request.features])

        # Apply preprocessing pipeline
        transformed_data = pipeline.transform(input_df)

        # Generate prediction
        prediction = int(model.predict(transformed_data)[0])

        result = {
            "prediction": prediction,
            "label": "attack" if prediction == 1 else "normal"
        }

        # Add probability if the model supports it
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(transformed_data)[0][1])
            result["attack_probability"] = probability

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))