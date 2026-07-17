import cv2
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import QTimer

from core.vision import VisionProcessor
from core.model import LibrasModel
from core.translator import TranslatorEngine
from core.data_manager import DataManager
from core.obs_server import OBSServerThread

from ui.sidebar import SidebarWidget
from ui.views import StudioWidget, TrainingWidget, LibraryWidget, SettingsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LIBRAS to Speech")
        self.resize(1400, 750)
        self.setMinimumSize(1100, 600)
        
        theme_path = os.path.join(os.path.dirname(__file__), 'theme.qss')
        if os.path.exists(theme_path):
            with open(theme_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        
        self.vision = VisionProcessor()
        self.model = LibrasModel()
        self.translator = TranslatorEngine()
        self.data_manager = DataManager()
        
        self.obs_server = OBSServerThread()
        self.obs_server.start()
        self.translator.history_updated.connect(self.obs_server.update_state)
        
        self.init_ui()
        
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.sidebar = SidebarWidget()
        self.sidebar.view_changed.connect(self.switch_view)
        
        self.stacked_widget = QStackedWidget()
        
        self.view_studio = StudioWidget(self)
        self.view_training = TrainingWidget(self)
        self.view_library = LibraryWidget(self)
        self.view_settings = SettingsWidget(self)
        
        self.stacked_widget.addWidget(self.view_studio)    # Index 0
        self.stacked_widget.addWidget(self.view_training)  # Index 1
        self.stacked_widget.addWidget(self.view_library)   # Index 2
        self.stacked_widget.addWidget(self.view_settings)  # Index 3
        
        self.view_map = {
            "studio": self.view_studio,
            "training": self.view_training,
            "library": self.view_library,
            "settings": self.view_settings
        }
        
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget, stretch=1)

    def switch_view(self, view_name):
        if view_name in self.view_map:
            self.stacked_widget.setCurrentWidget(self.view_map[view_name])

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
            
        frame = cv2.flip(frame, 1)
        
        annotated_frame, landmarks = self.vision.process_frame(frame)
        
        current_view = self.stacked_widget.currentWidget()
        if hasattr(current_view, "update_frame"):
            current_view.update_frame(annotated_frame, landmarks)

    def closeEvent(self, event):
        self.cap.release()
        self.vision.close()
        self.obs_server.stop()
        event.accept()
