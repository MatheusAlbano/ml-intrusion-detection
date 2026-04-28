import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from src.config import MODEL_PATH


def load_model():
    model = joblib.load(MODEL_PATH)
    return model


def get_feature_importance():
    model = load_model()

    if not hasattr(model, "feature_importances_"):
        return None

    feature_names = model.feature_names_in_
    importances = model.feature_importances_

    df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    })

    df = df.sort_values(
        by="importance",
        ascending=False
    )

    return df


def render_feature_importance():
    st.subheader("Feature Importance")

    importance_df = get_feature_importance()

    if importance_df is None:
        st.warning(
            "Model does not support feature importance."
        )
        return

    top_features = importance_df.head(15)

    fig = px.bar(
        top_features,
        x="importance",
        y="feature",
        orientation="h",
        title="Top 15 Most Important Features"
    )

    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )