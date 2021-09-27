import os
from skimage import img_as_ubyte
from skimage.io import imread, imsave
from skimage.transform import resize


def create_folder_for_file_path(file_path):
    resized_image_dir = os.path.dirname(file_path)
    os.makedirs(resized_image_dir, exist_ok=True)


def read_image(source_image_path):
    return imread(source_image_path)


def resize_image(image, output_shape):
    resized = resize(image, output_shape)
    return resized


def save_image(resized_image_path, resized):
    imsave(resized_image_path, img_as_ubyte(resized))


def resize_image_handler(source_image_path, resized_image_path, output_shape):
    create_folder_for_file_path(resized_image_path)

    image = read_image(source_image_path)
    resized = resize_image(image, output_shape)
    save_image(resized_image_path, resized)
