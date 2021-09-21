# Resize iamges to 100x100 pixels. We also convert them to PNG otherwise we can loose information if we save them as JPG.
# https://stackoverflow.com/questions/47361966/scikit-image-write-a-ndarray-to-image-with-imsave-read-back-with-imread-data

import numpy as np
import pandas as pd
import os

from pathlib import Path
from skimage.io import imsave, imread
from skimage import img_as_ubyte
from skimage.transform import resize

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


def prepare_train_images(train_csv_path):
    df = pd.read_csv(train_csv_path)
    file_path_list = load_column(data_frame=df, column_name="filename")

    for image_path in file_path_list:
        image_file = os.path.basename(image_path)
        p = Path(image_file)
        image_file_name = p.stem
        ext = 'png'

        object_folder = parse_object_type_from_image_path(image_path)
        train_or_val = parse_object_purpose_from_image_path(image_path)

        print()
        print('Processing image: {image_path}'.format(image_path=image_path))

        print('Reading    image: {image_path}'.format(image_path=image_path))
        image = imread(image_path)

        print('Resizing   image: {image_file}'.format(image_file=image_file))
        resized = resize(image, (100, 100, 3))
        resized_image_dir = get_resized_image_dir(train_or_val, object_folder)
        os.makedirs(resized_image_dir, exist_ok=True)
        resized_image_path = f'{resized_image_dir}/{image_file_name}.{ext}'
        imsave(resized_image_path, img_as_ubyte(resized))
        print(f'Resized    image: {resized_image_path}')


def main(repo_path):
    train_csv_path = repo_path / "data/prepared/train.csv"
    prepare_train_images(train_csv_path)


def load_column(data_frame, column_name):
    list = data_frame[column_name].to_list()
    return list


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
