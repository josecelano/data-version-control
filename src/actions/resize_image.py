import argparse
import os
import sys

from skimage import img_as_ubyte
from skimage.io import imread, imsave
from skimage.transform import resize

# sample usage:
# python src/actions/resize_image.py -i src/scripts/data/bridge.jpeg -o bridge2.jpeg -r 200 -c 200 -d 3


def create_dest_folder(resized_image_path):
    resized_image_dir = os.path.dirname(resized_image_path)
    os.makedirs(resized_image_dir, exist_ok=True)


def resize_image(source_image_path, resized_image_path, output_shape):
    image = imread(source_image_path)

    resized = resize(image, output_shape)

    create_dest_folder(resized_image_path)

    imsave(resized_image_path, img_as_ubyte(resized))


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help="source image path")
    parser.add_argument('-o', '--output', required=True,
                        help="resized image path")
    parser.add_argument('-r', '--rows', required=True,
                        type=int, help="resized image width")
    parser.add_argument('-c', '--cols', required=True,
                        type=int, help="resized image heigth")
    parser.add_argument('-d', '--dim', required=True, type=int)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    resize_image(args.input, args.output, (args.rows, args.cols, args.dim))


if __name__ == "__main__":
    main()
