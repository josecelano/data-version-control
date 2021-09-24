import os
import sys

from skimage import img_as_ubyte
from skimage.io import imread, imsave
from skimage.transform import resize


def create_dest_folder(resized_image_path):
    resized_image_dir = os.path.dirname(resized_image_path)
    os.makedirs(resized_image_dir, exist_ok=True)


def resize_image(source_image_path, resized_image_path, output_shape):
    image = imread(source_image_path)

    resized = resize(image, output_shape)

    create_dest_folder(resized_image_path)

    imsave(resized_image_path, img_as_ubyte(resized))


def main():
    source_image_path = os.environ["INPUT_SOURCE_IMAGE_PATH"]
    resized_image_path = os.environ["INPUT_RESIZED_IMAGE_PATH"]
    rows = int(os.environ["INPUT_ROWS"])
    cols = int(os.environ["INPUT_COLS"])
    dim = int(os.environ["INPUT_DIM"])

    resize_image(source_image_path, resized_image_path, (rows, cols, dim))

    output = f"Resized image {resized_image_path}"
    print(output)

if __name__ == "__main__":
    main()
