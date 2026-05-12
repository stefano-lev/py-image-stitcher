import os
import random
from datetime import datetime
from PIL import Image

SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp")


def validate_images(image_paths):
    valid_images = []

    for path in image_paths:
        try:
            Image.open(path)
            valid_images.append(path)
        except Exception as e:
            print(f"Skipping invalid image: {path}")
            print(e)

    return valid_images


def detect_orientation(images):
    landscape_count = 0
    portrait_count = 0

    for img in images:
        width, height = img.size

        if width >= height:
            landscape_count += 1
        else:
            portrait_count += 1

    if landscape_count >= portrait_count:
        return "vertical"

    return "horizontal"


def resize_images(images, direction):
    resized = []

    if direction == "horizontal":
        target_height = min(img.height for img in images)

        for img in images:
            ratio = target_height / img.height
            new_width = int(img.width * ratio)

            resized.append(
                img.resize(
                    (new_width, target_height),
                    Image.Resampling.LANCZOS
                )
            )

    else:
        target_width = min(img.width for img in images)

        for img in images:
            ratio = target_width / img.width
            new_height = int(img.height * ratio)

            resized.append(
                img.resize(
                    (target_width, new_height),
                    Image.Resampling.LANCZOS
                )
            )

    return resized


def stitch_images(images, direction):
    if direction == "horizontal":

        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)

        canvas = Image.new("RGB", (total_width, max_height))

        x_offset = 0

        for img in images:
            canvas.paste(img, (x_offset, 0))
            x_offset += img.width

    else:

        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)

        canvas = Image.new("RGB", (max_width, total_height))

        y_offset = 0

        for img in images:
            canvas.paste(img, (0, y_offset))
            y_offset += img.height

    return canvas


def create_collage(
    image_paths,
    direction="auto",
    randomize=False,
    output_path=None
):
    if not image_paths:
        raise ValueError("No images provided.")

    image_paths = validate_images(image_paths)

    if not image_paths:
        raise ValueError("No valid images found.")

    if randomize:
        random.shuffle(image_paths)

    images = [Image.open(path).convert("RGB") for path in image_paths]

    if direction == "auto":
        direction = detect_orientation(images)

    resized_images = resize_images(images, direction)

    collage = stitch_images(resized_images, direction)

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = f"collage-{timestamp}.jpg"

    collage.save(output_path)

    return output_path