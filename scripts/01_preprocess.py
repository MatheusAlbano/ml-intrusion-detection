import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import (
    PATHS,
    TRAIN_FILE,
    TEST_FILE,
    PROCESSED_TRAIN,
    PROCESSED_TEST,
    PIPELINE_PATH,
)

# Possible target columns in UNSW-NB15 (varies depending on the dataset version)
POSSIBLE_TARGETS = ["label", "Label", "attack_cat", "Attack_cat", "class"]


def find_target_column(df: pd.DataFrame) -> str:
    for c in POSSIBLE_TARGETS:
        if c in df.columns:
            return c
    raise ValueError(
        f"Nenhuma coluna de target encontrada. "
        f"Esperado uma destas: {POSSIBLE_TARGETS}. "
        f"Colunas encontradas (amostra): {list(df.columns)[:40]}"
    )


def ensure_dirs():
    PATHS.data_processed.mkdir(parents=True, exist_ok=True)
    PATHS.artifacts.mkdir(parents=True, exist_ok=True)
    PATHS.reports.mkdir(parents=True, exist_ok=True)
    PATHS.figures.mkdir(parents=True, exist_ok=True)


def main():
    ensure_dirs()

    if not TRAIN_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de treino não encontrado: {TRAIN_FILE}\n"
            "Coloque o parquet em data/raw/ com o nome: UNSW_NB15_training-set.parquet"
        )

    if not TEST_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de teste não encontrado: {TEST_FILE}\n"
            "Coloque o parquet em data/raw/ com o nome: UNSW_NB15_testing-set.parquet"
        )

    print("Lendo datasets parquet...")
    train_df = pd.read_parquet(TRAIN_FILE)
    test_df = pd.read_parquet(TEST_FILE)

    print(f"Treino: {train_df.shape} | Teste: {test_df.shape}")

    target_col = find_target_column(train_df)
    print(f"Coluna alvo encontrada: {target_col}")

    # Define BINARY task:
    # - If target is 'attack_cat': normal vs attack (1 = attack)
    # - If target is 'label': use as is
    # (If your dataset has a different format, we'll adjust it here later)
    if target_col.lower() == "attack_cat":
        y_train = (train_df[target_col].astype(str).str.lower() != "normal").astype(int)
        y_test = (test_df[target_col].astype(str).str.lower() != "normal").astype(int)
        target_used = "binary_from_attack_cat"
    else:
        # Try converting to int (label is usually 0/1)
        y_train = train_df[target_col].astype(int)
        y_test = test_df[target_col].astype(int)
        target_used = target_col

    # Columns that may cause data leakage
    leakage_cols = ["attack_cat", "Attack_cat"]

    X_train = train_df.drop(columns=[target_col] + leakage_cols, errors="ignore")
    X_test = test_df.drop(columns=[target_col] + leakage_cols, errors="ignore")

    # Remove clearly useless columns, if any exist
    # (some versions have 'id' or "Unnamed" columns)
    drop_candidates = [c for c in X_train.columns if c.lower() in ("id", "unnamed: 0")]
    if drop_candidates:
        X_train = X_train.drop(columns=drop_candidates, errors="ignore")
        X_test = X_test.drop(columns=drop_candidates, errors="ignore")
        print(f"Removidas colunas inúteis: {drop_candidates}")

    # If there are columns that are only in training or only in testing, align
    X_train, X_test = X_train.align(X_test, join="outer", axis=1, fill_value=None)

    # Detects numeric and categorical columns
    numeric_cols = X_train.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_cols = [c for c in X_train.columns if c not in numeric_cols]

    print(f"🔢 Numéricas: {len(numeric_cols)} | 🔤 Categóricas: {len(categorical_cols)}")

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    cat_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_cols),
            ("cat", cat_pipe, categorical_cols),
        ],
        remainder="drop",
    )

    print("⚙️ Ajustando pipeline (fit no treino)...")
    preprocessor.fit(X_train)

    print("➡️ Transformando treino e teste...")
    X_train_t = preprocessor.transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    # Assembles final feature names
    feature_names = []
    feature_names.extend(numeric_cols)

    if categorical_cols:
        ohe = preprocessor.named_transformers_["cat"].named_steps["onehot"]
        ohe_names = ohe.get_feature_names_out(categorical_cols).tolist()
        feature_names.extend(ohe_names)

    print(f"Total de features após encoding: {len(feature_names)}")

    # Save pipeline
    joblib.dump(preprocessor, PIPELINE_PATH)
    print(f"Pipeline salvo em: {PIPELINE_PATH}")

    # Save schema for traceability
    schema = {
        "target_original": target_col,
        "target_used": target_used,
        "n_features": len(feature_names),
        "feature_names": feature_names,
        "n_rows_train": int(X_train_t.shape[0]),
        "n_rows_test": int(X_test_t.shape[0]),
    }
    schema_path = PATHS.artifacts / "schema.json"
    schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"🧾 Schema salvo em: {schema_path}")

    # Save processed CSV
    train_out = pd.DataFrame(X_train_t, columns=feature_names)
    train_out["y"] = y_train.reset_index(drop=True)

    test_out = pd.DataFrame(X_test_t, columns=feature_names)
    test_out["y"] = y_test.reset_index(drop=True)

    train_out.to_csv(PROCESSED_TRAIN, index=False)
    test_out.to_csv(PROCESSED_TEST, index=False)

    print(f"📦 Train processed: {PROCESSED_TRAIN} -> {train_out.shape}")
    print(f"📦 Test processed:  {PROCESSED_TEST} -> {test_out.shape}")

    print("\n✅ Preprocessamento concluído com sucesso!")


if __name__ == "__main__":
    main()