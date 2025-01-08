import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QWidget, QRadioButton, QButtonGroup, QHBoxLayout, QScrollArea, QGridLayout, QCheckBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QDateTime
from PIL import Image
import random


class ImageCollageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("py-image-stitcher")
        self.resize(1200, 1000)
        self.center_window()
        self.apply_dark_theme()

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Scroll area for image previews
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("background-color: #2B2B2B; border: none;")
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        # Buttons
        self.add_images_button = QPushButton("Add Images")
        self.add_images_button.clicked.connect(self.add_images)
        self.add_images_button.setToolTip("Click to add images to the collage.")
        self.add_images_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        self.main_layout.addWidget(self.add_images_button)

        self.export_button = QPushButton("Export Collage")
        self.export_button.clicked.connect(self.export_collage)
        self.export_button.setToolTip("Export the created collage to a file.")
        self.export_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        self.main_layout.addWidget(self.export_button)

        # Stitch direction toggles
        self.stitch_direction = "horizontal"  # Default direction

        self.horizontal_button = QRadioButton("Horizontal")
        self.horizontal_button.setChecked(True)
        self.vertical_button = QRadioButton("Vertical")

        self.horizontal_button.setStyleSheet("color: white;")
        self.horizontal_button.setToolTip("Stitch images horizontally.")
        self.vertical_button.setStyleSheet("color: white;")
        self.vertical_button.setToolTip("Stitch images vertically.")

        self.direction_group = QButtonGroup()
        self.direction_group.addButton(self.horizontal_button)
        self.direction_group.addButton(self.vertical_button)

        self.horizontal_button.toggled.connect(lambda: self.set_stitch_direction("horizontal"))
        self.vertical_button.toggled.connect(lambda: self.set_stitch_direction("vertical"))

        self.direction_layout = QHBoxLayout()
        self.direction_layout.addWidget(self.horizontal_button)
        self.direction_layout.addWidget(self.vertical_button)
        self.main_layout.addLayout(self.direction_layout)

        # Randomize toggle
        self.randomize_checkbox = QCheckBox("Randomize Image Order")
        self.randomize_checkbox.setToolTip("Shuffle the order of images in the collage.")
        self.randomize_checkbox.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.randomize_checkbox)

        # Label for dimensions
        self.dimensions_label = QLabel("Calculated Dimensions: -")
        self.dimensions_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.dimensions_label)

        # Image paths
        self.image_paths = []

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(50, 50, 50))  # Tooltip background
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)  # Tooltip text
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)

        QApplication.setPalette(dark_palette)

        # Update the tooltips' style to have a dark background and white text
        self.setStyleSheet("""
            QToolTip {
                background-color: #2B2B2B;
                color: white;
                border: 1px solid #555555;
            }
        """)


    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def add_images(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()

            # Check for unsupported file types
            valid_files = []
            for file in selected_files:
                try:
                    Image.open(file)  # Attempt to open with PIL
                    valid_files.append(file)
                except Exception:
                    QMessageBox.warning(self, "Unsupported File", f"{file} is not a valid image.")
            
            self.image_paths.extend(valid_files)
            self.update_preview()

    def update_preview(self):
        if not self.image_paths:
            return

        # Clear previous previews
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Determine layout arrangement
        if self.stitch_direction == "horizontal":
            rows, cols = 1, len(self.image_paths)
        else:
            rows, cols = len(self.image_paths), 1

        # Add new previews with remove buttons
        for idx, img_path in enumerate(self.image_paths):
            pixmap = QPixmap(img_path)
            label = QLabel()
            label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            # Image container
            image_layout = QVBoxLayout()
            image_layout.addWidget(label)

            # Add swapping buttons
            if self.stitch_direction == "horizontal":
                swap_button_left = QPushButton("<")
                swap_button_right = QPushButton(">")
            else:
                swap_button_left = QPushButton("^")
                swap_button_right = QPushButton("v")

            swap_button_left.setStyleSheet("background-color:#676767; color: white;")
            swap_button_left.clicked.connect(lambda _, idx=idx: self.shift_image(idx, -1))  # Shift left
            image_layout.addWidget(swap_button_left)

            swap_button_right.setStyleSheet("background-color: #676767; color: white;")
            swap_button_right.clicked.connect(lambda _, idx=idx: self.shift_image(idx, 1))  # Shift right
            image_layout.addWidget(swap_button_right)
                

            # Add remove button
            remove_button = QPushButton("Remove")
            remove_button.setToolTip(f"Remove this image: {img_path}")
            remove_button.setStyleSheet("background-color: #E74C3C; color: white;")
            remove_button.clicked.connect(lambda _, path=img_path: self.remove_image(path))
            image_layout.addWidget(remove_button)

            # Add layout to grid
            container = QWidget()
            container.setLayout(image_layout)
            self.scroll_layout.addWidget(container, idx // cols, idx % cols, alignment=Qt.AlignCenter)

        self.scroll_widget.adjustSize()
        self.scroll_area.ensureVisible(0, 0)
        self.update_dimensions_label()

    def shift_image(self, idx, direction):
        # Swap the image path at idx with the one at idx + direction
        if 0 <= idx + direction < len(self.image_paths):
            self.image_paths[idx], self.image_paths[idx + direction] = self.image_paths[idx + direction], self.image_paths[idx]
            self.update_preview()  # Re-render the images in the new order

    def remove_image(self, img_path):
        if img_path in self.image_paths:
            self.image_paths.remove(img_path)
            self.update_preview()

    def set_stitch_direction(self, direction):
        self.stitch_direction = direction
        self.update_dimensions_label()
        self.update_preview()

    def update_dimensions_label(self):
        if not self.image_paths:
            self.dimensions_label.setText("Calculated Dimensions: -")
            return

        try:
            images = [Image.open(img) for img in self.image_paths]
            min_width = min(img.size[0] for img in images)  
            min_height = min(img.size[1] for img in images)

            if self.stitch_direction == "horizontal":
                total_width = sum(img.size[0] for img in images)
                dimensions = (total_width, min_height)
            else:
                total_height = sum(img.size[1] for img in images)
                dimensions = (min_width, total_height)

            self.dimensions_label.setText(f"Calculated Dimensions: {dimensions[0]} x {dimensions[1]}")
        except Exception as e:
            print(f"Error updating dimensions: {e}")

    def export_collage(self):
        if not self.image_paths:
            QMessageBox.warning(self, "No Images", "No images to stitch!")
            return

        try:
            # Check if randomization is enabled
            if self.randomize_checkbox.isChecked():
                random.shuffle(self.image_paths)

            images = [Image.open(img) for img in self.image_paths]

            # Resize images to smallest dimensions
            min_width = min(img.size[0] for img in images)
            min_height = min(img.size[1] for img in images)
            resized_images = [img.resize((min_width, min_height), Image.Resampling.LANCZOS) for img in images]

            if self.stitch_direction == "horizontal":
                total_width = sum(img.size[0] for img in resized_images)
                collage = Image.new("RGB", (total_width, min_height))
                x_offset = 0
                for img in resized_images:
                    collage.paste(img, (x_offset, 0))
                    x_offset += img.size[0]
            else:
                total_height = sum(img.size[1] for img in resized_images)
                collage = Image.new("RGB", (min_width, total_height))
                y_offset = 0
                for img in resized_images:
                    collage.paste(img, (0, y_offset))
                    y_offset += img.size[1]

            timestamp = QDateTime.currentDateTime().toString("yyyyMMdd-HHmmss")
            save_path = f"collage-{timestamp}.jpg"
            collage.save(save_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while exporting: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCollageApp()
    window.show()
    sys.exit(app.exec_())
