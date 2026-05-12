import argparse
from core import create_collage


def run_cli():

    parser = argparse.ArgumentParser(
        description="Python Image Stitcher"
    )

    parser.add_argument(
        "images",
        nargs="+",
        help="Image files to stitch"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output filename"
    )

    parser.add_argument(
        "--horizontal",
        action="store_true",
        help="Force horizontal stitching"
    )

    parser.add_argument(
        "--vertical",
        action="store_true",
        help="Force vertical stitching"
    )

    parser.add_argument(
        "--randomize",
        action="store_true",
        help="Randomize image order"
    )

    args = parser.parse_args()

    direction = "auto"

    if args.horizontal:
        direction = "horizontal"

    if args.vertical:
        direction = "vertical"

    try:

        output = create_collage(
            image_paths=args.images,
            direction=direction,
            randomize=args.randomize,
            output_path=args.output
        )

        print(f"Saved collage to: {output}")

    except Exception as e:
        print("ERROR:")
        print(e)