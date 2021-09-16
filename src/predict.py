from joblib import load
import json
from pathlib import Path
import numpy as np

from train import load_data, preprocess
from skimage.io import imread

import sys
import getopt


def main(repo_path, argv):

    inputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('How to use: predict.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg.strip()

        model = load(repo_path / "model/model.joblib")

        image_path = repo_path / inputfile

        print('Predicting for image: "', image_path, '"')

        raw_image = imread(image_path)  
    
        processed_image = [preprocess(raw_image)]
        data = np.concatenate(processed_image, axis=0)

        predictions = model.predict(data)

        print(predictions)


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path, sys.argv[1:])
