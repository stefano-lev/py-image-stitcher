import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QWidget, QRadioButton, QButtonGroup, QHBoxLayout, QScrollArea, QGridLayout
)
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt, QDateTime
from PIL import Image


class ImageCollageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("py-image-stitcher")
        self.resize(1200, 800)
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
        self.add_images_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        self.main_layout.addWidget(self.add_images_button)

        self.export_button = QPushButton("Export Collage")
        self.export_button.clicked.connect(self.export_collage)
        self.export_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        self.main_layout.addWidget(self.export_button)

        # Stitch direction toggles
        self.stitch_direction = "horizontal"  # Default direction

        self.horizontal_button = QRadioButton("Horizontal")
        self.horizontal_button.setChecked(True)
        self.vertical_button = QRadioButton("Vertical")

        self.horizontal_button.setStyleSheet("color: white;")
        self.vertical_button.setStyleSheet("color: white;")

        self.direction_group = QButtonGroup()
        self.direction_group.addButton(self.horizontal_button)
        self.direction_group.addButton(self.vertical_button)

        self.horizontal_button.toggled.connect(lambda: self.set_stitch_direction("horizontal"))
        self.vertical_button.toggled.connect(lambda: self.set_stitch_direction("vertical"))

        self.direction_layout = QHBoxLayout()
        self.direction_layout.addWidget(self.horizontal_button)
        self.direction_layout.addWidget(self.vertical_button)
        self.main_layout.addLayout(self.direction_layout)

        # Image paths
        self.image_paths = []

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)

        QApplication.setPalette(dark_palette)

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
            self.image_paths = file_dialog.selectedFiles()
            if self.image_paths:
                # Clear previous previews
                for i in reversed(range(self.scroll_layout.count())):
                    widget = self.scroll_layout.itemAt(i).widget()
                    if widget:
                        widget.deleteLater()

                # Add new previews
                for idx, img_path in enumerate(self.image_paths):
                    pixmap = QPixmap(img_path)
                    label = QLabel()

                    # Dynamically scale previews to occupy more space
                    max_width = self.scroll_area.width() // 2
                    max_height = self.scroll_area.height() // 3
                    label.setPixmap(pixmap.scaled(
                        max_width,
                        max_height,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    ))
                    self.scroll_layout.addWidget(label, idx // 3, idx % 3)

    def set_stitch_direction(self, direction):
        self.stitch_direction = direction
        print(f"Stitch direction set to: {self.stitch_direction}")

    def export_collage(self):
        if not self.image_paths:
            print("No images to stitch!")
            return

        try:
            # Open images
            images = [Image.open(img_path) for img_path in self.image_paths]

            # Find the smallest width and height among all images
            min_width = min(img.size[0] for img in images)
            min_height = min(img.size[1] for img in images)

            # Resize all images to match the smallest dimensions
            resized_images = [img.resize((min_width, min_height), Image.Resampling.LANCZOS) for img in images]

            # Create collage based on stitch direction
            if self.stitch_direction == "horizontal":
                total_width = sum(img.size[0] for img in resized_images)
                max_height = min_height
                collage = Image.new("RGB", (total_width, max_height), color=(255, 255, 255))
                x_offset = 0
                for img in resized_images:
                    collage.paste(img, (x_offset, 0))
                    x_offset += img.size[0]
            else:
                max_width = min_width
                total_height = sum(img.size[1] for img in resized_images)
                collage = Image.new("RGB", (max_width, total_height), color=(255, 255, 255))
                y_offset = 0
                for img in resized_images:
                    collage.paste(img, (0, y_offset))
                    y_offset += img.size[1]

            # Automatically generate filename with timestamp
            timestamp = QDateTime.currentDateTime().toString("yyyyMMdd-HHmmss")
            save_path = f"collage-{timestamp}.jpg"
            collage.save(save_path)
            print(f"Collage saved at {save_path}")

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCollageApp()
    window.show()
    sys.exit(app.exec_())
