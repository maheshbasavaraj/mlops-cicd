from src.train import MIN_ACCURACY, train_model


def test_model_meets_accuracy_gate():
    _, metadata = train_model()
    assert metadata["accuracy"] >= MIN_ACCURACY
