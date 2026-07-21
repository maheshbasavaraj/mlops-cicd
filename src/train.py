from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


ARTIFACT_DIR = Path("artifacts")
MODEL_PATH = ARTIFACT_DIR / "model.joblib"
MIN_ACCURACY = 0.85
RANDOM_STATE = 42


def train_model():
    iris = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=iris.target,
    )

    model = RandomForestClassifier(
        n_estimators=80,
        max_depth=4,
        random_state=RANDOM_STATE,
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    metadata = {
        "accuracy": accuracy,
        "target_names": list(iris.target_names),
        "feature_names": list(iris.feature_names),
        "min_accuracy": MIN_ACCURACY,
    }
    return model, metadata


def save_model(model, metadata):
    ARTIFACT_DIR.mkdir(exist_ok=True)
    joblib.dump({"model": model, "metadata": metadata}, MODEL_PATH)


def main():
    model, metadata = train_model()
    accuracy = metadata["accuracy"]
    print(f"Model accuracy: {accuracy:.3f}")

    if accuracy < MIN_ACCURACY:
        raise SystemExit(
            f"Model quality gate failed: {accuracy:.3f} < {MIN_ACCURACY:.3f}"
        )

    save_model(model, metadata)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
