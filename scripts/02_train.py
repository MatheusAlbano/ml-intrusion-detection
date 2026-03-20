import json
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

from src.config import (
    PROCESSED_TRAIN,
    MODEL_PATH,
    METRICS_PATH,
    PATHS
)


def main():
    print("📥 Carregando dataset processado...")

    # Load processed dataset
    df = pd.read_csv(PROCESSED_TRAIN)

    # Separate features and target variable
    X = df.drop(columns=["y"])
    y = df["y"].astype(int)

    print(f"Dataset: {X.shape}")

    # Define stratified cross-validation (preserves class distribution)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Baseline Model
    print("\n🔹 Treinando Logistic Regression (baseline)...")

    lr = LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    )

    # Evaluate baseline model using cross-validation
    lr_scores = cross_val_score(lr, X, y, cv=cv, scoring="f1")
    lr_f1 = lr_scores.mean()

    print(f"F1 (LR): {lr_f1:.4f}")

    # Advanced Model
    print("\n🔹 Treinando Random Forest...")

    rf = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced_subsample",
        n_jobs=-1
    )

    # Evaluate Random Forest using cross-validation
    rf_scores = cross_val_score(rf, X, y, cv=cv, scoring="f1")
    rf_f1 = rf_scores.mean()

    print(f"F1 (RF): {rf_f1:.4f}")

    # Model Selection
    # Compare models and select the best one based on F1 score
    if rf_f1 >= lr_f1:
        best_model = rf
        best_name = "RandomForest"
        best_score = rf_f1
    else:
        best_model = lr
        best_name = "LogisticRegression"
        best_score = lr_f1

    print(f"\n🏆 Melhor modelo: {best_name} (F1={best_score:.4f})")

    # Final Training
    # Train the selected model on the full dataset
    print("\n⚙️ Treinando modelo final com todos os dados...")
    best_model.fit(X, y)

    # Save Model
    joblib.dump(best_model, MODEL_PATH)

    # Save Metrics
    metrics = {
        "model": best_name,
        "f1_score": float(best_score)
    }

    PATHS.reports.mkdir(exist_ok=True)

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

    print("\n💾 Modelo salvo em:", MODEL_PATH)
    print("📊 Métricas salvas em:", METRICS_PATH)

    print("\n✅ Treinamento concluído!")


if __name__ == "__main__":
    main()