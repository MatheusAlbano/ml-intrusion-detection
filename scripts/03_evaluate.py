import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_auc_score
)

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

    print(f"Dataset de teste: {X_test.shape}")

    print("\n Carregando modelo treinado...")
    model = joblib.load(MODEL_PATH)

    # Make predictions
    print("\nRealizando previsões...")
    y_pred = model.predict(X_test)

    # Classification Report
    print("\n Gerando relatório de classificação...")
    report = classification_report(y_test, y_pred, output_dict=True)

    PATHS.reports.mkdir(exist_ok=True)

    report_path = PATHS.reports / "classification_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print("Relatório salvo em:", report_path)

    # ROC-AUC
    auc = None
    if hasattr(model, "predict_proba"):
        print("\nCalculando ROC-AUC...")
        proba = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, proba)

        auc_path = PATHS.reports / "roc_auc.json"
        with open(auc_path, "w") as f:
            json.dump({"roc_auc": float(auc)}, f, indent=4)

        print(f"ROC-AUC: {auc:.4f}")
        print("ROC salvo em:", auc_path)

    # Confusion Matrix
    print("\n Gerando matriz de confusão...")

    PATHS.figures.mkdir(parents=True, exist_ok=True)

    cm = confusion_matrix(y_test, y_pred)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(values_format="d")

    fig_path = PATHS.figures / "confusion_matrix.png"
    plt.title("Matriz de Confusão")
    plt.savefig(fig_path, dpi=200, bbox_inches="tight")
    plt.close()

    print("Matriz salva em:", fig_path)

    print("\n Avaliação concluída com sucesso!")


if __name__ == "__main__":
    main()