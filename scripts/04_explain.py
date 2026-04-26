import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import RocCurveDisplay

from src.config import (
    PROCESSED_TEST,
    MODEL_PATH,
    PATHS
)


def main():
    print("Carregando dados de teste...")

    # Load processed test dataset
    df = pd.read_csv(PROCESSED_TEST)

    # Separate features and target
    X_test = df.drop(columns=["y"])
    y_test = df["y"].astype(int)

    print("Carregando modelo treinado...")
    model = joblib.load(MODEL_PATH)

    PATHS.figures.mkdir(parents=True, exist_ok=True)

    # Feature Importance
    if hasattr(model, "feature_importances_"):
        print("\n Gerando feature importance...")

        importances = model.feature_importances_

        feature_importance_df = pd.DataFrame({
            "feature": X_test.columns,
            "importance": importances
        })

        feature_importance_df = feature_importance_df.sort_values(
            by="importance",
            ascending=False
        )

        top_features = feature_importance_df.head(15)

        plt.figure(figsize=(12, 8))
        plt.barh(
            top_features["feature"],
            top_features["importance"]
        )
        plt.gca().invert_yaxis()
        plt.title("Top 15 Most Important Features")

        feature_path = PATHS.figures / "feature_importance.png"
        plt.savefig(feature_path, dpi=200, bbox_inches="tight")
        plt.close()

        print("Feature importance salva em:", feature_path)

    # ROC Curve
    if hasattr(model, "predict_proba"):
        print("\n Gerando curva ROC...")

        probabilities = model.predict_proba(X_test)[:, 1]

        RocCurveDisplay.from_predictions(
            y_test,
            probabilities
        )

        roc_path = PATHS.figures / "roc_curve.png"
        plt.title("ROC Curve")
        plt.savefig(roc_path, dpi=200, bbox_inches="tight")
        plt.close()

        print("Curva ROC salva em:", roc_path)

    print("\n Explicação do modelo concluída!")


if __name__ == "__main__":
    main()