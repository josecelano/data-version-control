import json
from pathlib import Path


def main(repo_path):
    accuracy_path = repo_path / "metrics/accuracy.json"

    with open(accuracy_path) as json_file:
        data = json.load(json_file)

        accuracy = data['accuracy']

        if abs(accuracy - .81) > 0.01:
            exit(1)


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
