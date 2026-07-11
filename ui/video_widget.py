import cv2
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt

class VideoWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("background-color: black;")
        
    def update_frame(self, cv_img):
        """Updates the image_label with a new opencv image"""
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        # Convert from BGR to RGB
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        
        qt_img = QImage(cv_img_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_img)
        
        # Scale pixmap to fit the label, keeping aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.width(), self.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setPixmap(scaled_pixmap)
