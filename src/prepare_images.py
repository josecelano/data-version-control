import numpy as np
import pandas as pd
import os

from pathlib import Path
from actions.resize_image.resize_image import resize_image

# From /home/josecelano/Documents/github/josecelano/data-version-control/data/raw/train/n03445777/n03445777_14165.JPEG
# It returns: n03445777
# The folder containing the image
def parse_object_type_from_image_path(image_path):
    return os.path.basename(os.path.dirname(image_path))  # Object type folder


# From /home/josecelano/Documents/github/josecelano/data-version-control/data/raw/train/n03445777/n03445777_14165.JPEG
# It returns: train
# From /home/josecelano/Documents/github/josecelano/data-version-control/data/raw/val/n03445777/n03445777_14165.JPEG
# It returns: val
def parse_object_purpose_from_image_path(image_path):
    # train or val
    return os.path.basename(os.path.dirname(os.path.dirname(image_path)))


def get_resized_image_dir(train_or_val, object_folder):
    return 'data/prepared/{train_or_val}/resized/{object_folder}'.format(train_or_val=train_or_val, object_folder=object_folder)


def get_reshaped_image_dir(train_or_val, object_folder):
    return 'data/prepared/{train_or_val}/reshaped/{object_folder}'.format(train_or_val=train_or_val, object_folder=object_folder)


def get_resized_image_path(resized_image_dir, image_file):
    return f'{resized_image_dir}/{image_file}'


def get_reshaped_image_path(reshaped_image_dir, image_file):
    return f'{reshaped_image_dir}/{image_file}'


def prepare_images(csv_path):
    df = pd.read_csv(csv_path)
    file_path_list = load_column(data_frame=df, column_name="filename")

    for image_path in file_path_list:
        image_file = os.path.basename(image_path)
        p = Path(image_file)
        image_file_name = p.stem
        ext = 'png'

        object_folder = parse_object_type_from_image_path(image_path)
        train_or_val = parse_object_purpose_from_image_path(image_path)

        resized_image_dir = get_resized_image_dir(train_or_val, object_folder)
        resized_image_path = f'{resized_image_dir}/{image_file_name}.{ext}'

        resize_image(image_path, resized_image_path, (100, 100, 3))


def main(repo_path):
    # prepare train images
    train_csv_path = repo_path / "data/prepared/train.csv"
    prepare_images(train_csv_path)

    # prepare test images
    test_csv_path = repo_path / "data/prepared/test.csv"
    prepare_images(test_csv_path)


def load_column(data_frame, column_name):
    list = data_frame[column_name].to_list()
    return list


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
