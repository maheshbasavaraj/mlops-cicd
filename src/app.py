from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.train import MODEL_PATH, train_model


app = FastAPI(title="Iris ML API", version="1.0.0")


class IrisFeatures(BaseModel):
    sepal_length: float = Field(..., gt=0, lt=10)
    sepal_width: float = Field(..., gt=0, lt=10)
    petal_length: float = Field(..., gt=0, lt=10)
    petal_width: float = Field(..., gt=0, lt=10)


def load_model_bundle():
    if Path(MODEL_PATH).exists():
        return joblib.load(MODEL_PATH)

    model, metadata = train_model()
    return {"model": model, "metadata": metadata}


MODEL_BUNDLE = load_model_bundle()
MODEL = MODEL_BUNDLE["model"]
METADATA = MODEL_BUNDLE["metadata"]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_accuracy": round(float(METADATA["accuracy"]), 3),
    }


@app.post("/predict")
def predict(features: IrisFeatures):
    row = np.array(
        [
            [
                features.sepal_length,
                features.sepal_width,
                features.petal_length,
                features.petal_width,
            ]
        ]
    )
    prediction = int(MODEL.predict(row)[0])
    species = METADATA["target_names"][prediction]
    return {"species": species}
