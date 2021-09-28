import numpy as np
import pandas as pd
import os

from joblib import dump
from pathlib import Path
from skimage.io import imread_collection, imsave, imread
from skimage import img_as_float64
from skimage.transform import resize
from sklearn.ensemble import RandomForestClassifier

from prepare_images import parse_object_type_from_image_path, parse_object_purpose_from_image_path, get_resized_image_dir, get_resized_image_path


def load_raw_images(data_frame, column_name):
    filelist = data_frame[column_name].to_list()
    image_list = imread_collection(filelist)
    return image_list


def load_resized_images(data_frame, column_name):
    # get the raw image list
    filelist = data_frame[column_name].to_list()

    # get the prepared image list
    filelist = [get_resized_image_path_from(
        raw_image_path) for raw_image_path in filelist]

    image_list = imread_collection(filelist)

    return image_list


def load_labels(data_frame, column_name):
    label_list = data_frame[column_name].to_list()
    return label_list


def resize_and_reshape(image):
    return im_reshape(im_resize(image))


def convert_to_float64_and_reshape(image):
    return im_reshape(img_as_float64(image))


def im_resize(image):
    # resize doc: https://scikit-image.org/docs/stable/api/skimage.transform.html?highlight=resize#resize
    return resize(image, (100, 100, 3))


def im_reshape(image):
    # reshaped doc: https://numpy.org/doc/stable/reference/generated/numpy.reshape.html#numpy-reshape
    return image.reshape((1, 30000))


def get_resized_image_path_from(raw_image_path):
    raw_image_file = os.path.basename(raw_image_path)
    p = Path(raw_image_file)
    image_file_name = p.stem
    ext = 'png'
    image_file = f'{image_file_name}.{ext}'
    object_type = parse_object_type_from_image_path(raw_image_path)
    object_purpose = parse_object_purpose_from_image_path(raw_image_path)
    resized_image_dir = get_resized_image_dir(object_purpose, object_type)
    resized_image_relative_path = get_resized_image_path(
        resized_image_dir, image_file)
    return resized_image_relative_path


def load_data_from_raw_images(data_path):
    df = pd.read_csv(data_path)

    labels = load_labels(data_frame=df, column_name="label")

    # load, resize and reshape images
    raw_images = load_raw_images(data_frame=df, column_name="filename")
    processed_images = [resize_and_reshape(image) for image in raw_images]

    data = np.concatenate(processed_images, axis=0)

    return data, labels


def load_data_from_resized_images(data_path):
    df = pd.read_csv(data_path)

    labels = load_labels(data_frame=df, column_name="label")

    # load resized images and only reshape them
    resized_images = load_resized_images(data_frame=df, column_name="filename")
    processed_images = [convert_to_float64_and_reshape(
        image) for image in resized_images]

    data = np.concatenate(processed_images, axis=0)

    return data, labels


def main(repo_path):
    train_csv_path = repo_path / "data/prepared/train.csv"

    # training using raw images
    #train_data, labels = load_data_from_raw_images(train_csv_path)

    # training using preprocessed images (resized images)
    # uncomment this line to use resized images
    train_data, labels = load_data_from_resized_images(train_csv_path)

    # RandomForestClassifier: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn-ensemble-randomforestclassifier
    rf = RandomForestClassifier()

    trained_model = rf.fit(train_data, labels)

    dump(trained_model, repo_path / "model/model.joblib")


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
