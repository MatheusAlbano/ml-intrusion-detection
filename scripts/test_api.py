import requests
import pandas as pd

from src.config import TRAIN_FILE

# Load original dataset (raw)
df = pd.read_parquet(TRAIN_FILE)

# Drop target column
df = df.drop(columns=["label"], errors="ignore")

# Get one sample
sample = df.iloc[0].to_dict()

# Send request to API
url = "http://127.0.0.1:8000/predict"

response = requests.post(url, json={"features": sample})

print("Status:", response.status_code)
print("Response:", response.json())