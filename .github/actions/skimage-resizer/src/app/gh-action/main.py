import os
import sys

from shared.resize_image_handler import resize_image_handler


def parse_output_shape():
    rows = int(os.environ["INPUT_ROWS"])
    cols = int(os.environ["INPUT_COLS"])
    dim = int(os.environ["INPUT_DIM"])
    return (rows, cols, dim)


def main():
    source_image_path = os.environ["INPUT_SOURCE_IMAGE_PATH"]
    resized_image_path = os.environ["INPUT_RESIZED_IMAGE_PATH"]
    output_shape = parse_output_shape()

    resize_image_handler(source_image_path, resized_image_path, output_shape)

    output = f"Resized image {resized_image_path}"
    print(output)


if __name__ == "__main__":
    main()
