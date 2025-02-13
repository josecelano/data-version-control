from joblib import load
import json
from pathlib import Path

from sklearn.metrics import accuracy_score

from train import load_data_from_raw_images, load_data_from_resized_images


def main(repo_path):
    test_csv_path = repo_path / "data/prepared/test.csv"

    # evaluate using raw images
    test_data, labels = load_data_from_raw_images(test_csv_path)

    # evaluate using pre-resized images
    #test_data, labels = load_data_from_resized_images(test_csv_path)

    model = load(repo_path / "model/model.joblib")
    predictions = model.predict(test_data)
    accuracy = accuracy_score(labels, predictions)
    metrics = {"accuracy": accuracy}
    accuracy_path = repo_path / "metrics/accuracy.json"
    accuracy_path.write_text(json.dumps(metrics))


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
