# py-image-stitcher

A Python-based image collage utility that allows users to add multiple images, arrange them either horizontally or vertically, and export the final collage as a single image file. The application provides a simple, interactive interface built with PyQt5.

## Features
- **Add Images**: Select multiple images from your file system to add to the collage.
- **Arrange Images**: Choose between horizontal or vertical arrangement for the images.
- **Randomize Order**: Optionally shuffle the order of the images before stitching.
- **Remove Images**: Easily remove images from the collage preview.
- **Export Collage**: Export the collage to a `.jpg` file with a timestamped filename.
- **Dark Theme**

## Screenshots
![Screenshot 1](images/screenshot1.jpg)
*Demonstration of the basic functionality.*

![Screenshot 2](images/screenshot2.jpg)
*Configurable orientation and toggles.*

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your-username/py-image-stitcher.git
    ```

2. Navigate into the project directory:

    ```bash
    cd py-image-stitcher
    ```

3. Install the required dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should include the necessary libraries:

    ```txt
    PyQt5
    Pillow
    ```

4. Launch the application:

    ```bash
    python main.py
    ```

## Usage

1. **Add Images**: Click the "Add Images" button to open a file dialog and select images from your computer.
2. **Arrange Images**: Choose whether to stitch images **horizontally** or **vertically** using the radio buttons.
3. **Randomize**: Optionally, check the box to randomize the order of the images in the collage.
4. **Preview**: Images will be displayed in the selected layout, and you can remove any unwanted images using the "Remove" button next to each preview.
5. **Export Collage**: When you're satisfied with the arrangement, click "Export Collage" to generate a final image and save it to your computer.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
