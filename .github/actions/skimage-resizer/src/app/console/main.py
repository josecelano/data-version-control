import argparse

from shared.resize_image_handler import resize_image_handler


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

    resize_image_handler(args.input, args.output,
                         (args.rows, args.cols, args.dim))


if __name__ == "__main__":
    main()
