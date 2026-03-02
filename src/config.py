from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    """
    Centraliza todos os caminhos do projeto.
    """
    root: Path = Path(__file__).resolve().parents[1]
    data: Path = root / "data"
    data_raw: Path = data / "raw"
    data_processed: Path = data / "processed"
    artifacts: Path = root / "artifacts"
    reports: Path = root / "reports"
    figures: Path = reports / "figures"

PATHS = Paths()

# Dataset
TRAIN_FILE = PATHS.data_raw / "UNSW_NB15_training-set.parquet"
TEST_FILE = PATHS.data_raw / "UNSW_NB15_testing-set.parquet"

# Processed outputs
PROCESSED_TRAIN = PATHS.data_processed / "train_processed.csv"
PROCESSED_TEST = PATHS.data_processed / "test_processed.csv"

# Artifacts
PIPELINE_PATH = PATHS.artifacts / "preprocessing_pipeline.joblib"
MODEL_PATH = PATHS.artifacts / "best_model.joblib"

# Reports
METRICS_PATH = PATHS.reports / "metrics.json"
CONFUSION_MATRIX_PATH = PATHS.figures / "confusion_matrix.png"