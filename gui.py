import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image

from core import create_collage

class ImageCollageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("py-image-stitcher")
        self.resize(1200, 1000)
        self.center_window()
        self.apply_dark_theme()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("background-color: #2B2B2B; border: none;")
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area)

        self.add_images_button = QPushButton("Add Images")
        self.add_images_button.clicked.connect(self.add_images)
        self.add_images_button.setToolTip("Click to add images to the collage.")
        self.add_images_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        self.main_layout.addWidget(self.add_images_button)

        self.export_button = QPushButton("Export Stitched Image")
        self.export_button.clicked.connect(self.export_collage)
        self.export_button.setToolTip("Export the created collage to a file.")
        self.export_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        self.main_layout.addWidget(self.export_button)

        self.stitch_direction = "horizontal"

        self.horizontal_button = QRadioButton("Horizontal")
        self.horizontal_button.setChecked(True)
        self.vertical_button = QRadioButton("Vertical")
        self.collage_button = QRadioButton("Collage Mode")

        self.horizontal_button.setStyleSheet("color: white;")
        self.horizontal_button.setToolTip("Stitch images horizontally.")
        self.vertical_button.setStyleSheet("color: white;")
        self.vertical_button.setToolTip("Stitch images vertically.")
        self.collage_button.setStyleSheet("color: white;")
        self.collage_button.setToolTip("Stitch images dynamically.")

        self.direction_group = QButtonGroup()
        self.direction_group.addButton(self.horizontal_button)
        self.direction_group.addButton(self.vertical_button)
        self.direction_group.addButton(self.collage_button)

        self.horizontal_button.clicked.connect(
            lambda: self.set_stitch_direction("horizontal")
        )

        self.vertical_button.clicked.connect(
            lambda: self.set_stitch_direction("vertical")
        )

        self.collage_button.clicked.connect(
            lambda: self.set_stitch_direction("collage")
        )

        self.direction_layout = QHBoxLayout()
        self.direction_layout.addWidget(self.horizontal_button)
        self.direction_layout.addWidget(self.vertical_button)
        self.direction_layout.addWidget(self.collage_button)
        self.main_layout.addLayout(self.direction_layout)

        self.randomize_checkbox = QCheckBox("Randomize Image Order")
        self.randomize_checkbox.setToolTip("Shuffle the order of images in the collage.")
        self.randomize_checkbox.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.randomize_checkbox)

        self.dimensions_label = QLabel("Calculated Dimensions: -")
        self.dimensions_label.setStyleSheet("color: white;")
        self.main_layout.addWidget(self.dimensions_label)

        self.collage_dimensions = 1800
        self.collage_dimensions_field = QLineEdit()
        self.collage_dimensions_field.setStyleSheet("color: black;  background-color: white")
        self.collage_background_color = QColor()

        self.collage_dimensions_label = QLabel("Chosen Resolution for Collage: - ")
        self.collage_dimensions_label.setStyleSheet("color: white;")

        self.image_paths = []

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(50, 50, 50))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)

        QApplication.setPalette(dark_palette)

        self.setStyleSheet("""
            QToolTip {
                background-color: #2B2B2B;
                color: white;
                border: 1px solid #555555;
            }

            QMessageBox {
                background-color: #2B2B2B;
            }

            QMessageBox QLabel {
                color: white;
            }

            QMessageBox QPushButton {
                background-color: #3C3C3C;
                color: white;
                border: 1px solid #555555;
                padding: 5px;
                min-width: 80px;
            }

            QFileDialog {
                background-color: #2B2B2B;
                color: white;
            }

            QColorDialog {
                background-color: #2B2B2B;
                color: white;
            }
        """)


    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def add_images(self):
        print("Opening file dialog...")
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")

        if file_dialog.exec_():
            try:
                selected_files = file_dialog.selectedFiles()
                print(f"Files selected: {selected_files}")
                valid_files = []
                for file in selected_files:
                    try:
                        img = Image.open(file)
                        valid_files.append(file)
                    except Exception as e:
                        print(f"Invalid image: {file}, Error: {e}")
                        QMessageBox.warning(self, "Unsupported File", f"{file} is not a valid image.")
                
                self.image_paths.extend(valid_files)
                print(f"Valid image paths: {self.image_paths}")
                self.update_preview()
            except Exception as e:
                print(f"Error while selecting images: {e}")


    def init_collage_mode(self):
        if(self.stitch_direction == "collage"):
            self.main_layout.addWidget(self.collage_dimensions_label)
            self.main_layout.addWidget(self.collage_dimensions_field)


    def update_preview(self):
        if not self.image_paths:
            return

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        if self.stitch_direction == "collage":
            placeholder_label = QLabel("Collage mode preview coming soon!")
            placeholder_label.setStyleSheet("color: white; font-size: 16px;")
            self.scroll_layout.addWidget(placeholder_label)
            return

        rows, cols = (1, len(self.image_paths)) if self.stitch_direction == "horizontal" else (len(self.image_paths), 1)

        for idx, img_path in enumerate(self.image_paths):
            pixmap = QPixmap(img_path)
            label = QLabel()
            label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            image_layout = QVBoxLayout()
            image_layout.addWidget(label)

            if self.stitch_direction != "collage":
                self.add_swap_buttons(idx, image_layout)

            remove_button = QPushButton("Remove")
            remove_button.setStyleSheet("background-color: #E74C3C; color: white;")
            remove_button.clicked.connect(lambda _, path=img_path: self.remove_image(path))
            image_layout.addWidget(remove_button)

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

    def add_swap_buttons(self, idx, layout):
        # Up/Left
        up_button = QPushButton("↑" if self.stitch_direction == "vertical" else "←")
        up_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        up_button.setToolTip("Move image up" if self.stitch_direction == "vertical" else "Move image left")
        up_button.clicked.connect(lambda _, i=idx: self.shift_image(i, -1))
        layout.addWidget(up_button)

        # Down/Right
        down_button = QPushButton("↓" if self.stitch_direction == "vertical" else "→")
        down_button.setStyleSheet("background-color: #3C3C3C; color: white;")
        down_button.setToolTip("Move image down" if self.stitch_direction == "vertical" else "Move image right")
        down_button.clicked.connect(lambda _, i=idx: self.shift_image(i, 1))
        layout.addWidget(down_button)


    def remove_image(self, img_path):
        if img_path in self.image_paths:
            self.image_paths.remove(img_path)
            self.update_preview()

    def set_stitch_direction(self, direction):
        self.stitch_direction = direction

        if direction == "collage":
            self.enable_collage_mode()
        else:
            self.disable_collage_mode()

        self.update_dimensions_label()
        self.update_preview()

    def choose_background_color(self):
        try:
            print("Opening color picker dialog...")
            color = QColorDialog.getColor()

            if color.isValid():
                self.collage_background_color = color
                print(f"Selected color: {color.name()} (RGB: {color.red()}, {color.green()}, {color.blue()})")
                self.background_color_picker.setStyleSheet(f"background-color: {color.name()}; color: black;")
            else:
                print("No valid color selected.")
        except Exception as e:
            print(f"Error in choose_background_color: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def enable_collage_mode(self):
        try:
            if not hasattr(self, "collage_widgets_initialized"):
                print("Initializing collage mode widgets...")

                self.collage_dimensions_label = QLabel("Chosen Resolution for Collage: - ")
                self.collage_dimensions_label.setStyleSheet("color: white;")
                self.main_layout.addWidget(self.collage_dimensions_label)

                self.collage_dimensions_field = QLineEdit()
                self.collage_dimensions_field.setStyleSheet("color: black; background-color: white;")
                self.main_layout.addWidget(self.collage_dimensions_field)

                self.background_color_label = QLabel("Background Color:")
                self.background_color_label.setStyleSheet("color: white;")
                self.main_layout.addWidget(self.background_color_label)

                self.background_color_picker = QPushButton("Choose Color")
                self.background_color_picker.setStyleSheet("background-color: white; color: black;")
                self.background_color_picker.clicked.connect(self.choose_background_color)
                self.main_layout.addWidget(self.background_color_picker)

                self.collage_widgets_initialized = True
                print("Collage mode widgets initialized successfully.")
        except Exception as e:
            print(f"Error while enabling collage mode: {e}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def disable_collage_mode(self):
        self.collage_dimensions_label.setParent(None)
        self.collage_dimensions_field.setParent(None)

        if hasattr(self, 'background_color_label'):
            self.background_color_label.setParent(None)
            self.background_color_picker.setParent(None)
    

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
            QMessageBox.warning(
                self,
                "No Images",
                "No images to stitch!"
            )
            return

        try:

            output = create_collage(
                image_paths=self.image_paths,
                direction=self.stitch_direction,
                randomize=self.randomize_checkbox.isChecked()
            )

            QMessageBox.information(
                self,
                "Success",
                f"Saved collage to:\n{output}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

def launch_gui():

    app = QApplication(sys.argv)

    window = ImageCollageApp()

    window.show()

    sys.exit(app.exec_())