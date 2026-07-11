import cv2
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QListWidget, QFrame,
                             QMessageBox)
from PyQt6.QtCore import QTimer, Qt

from core.vision import VisionProcessor
from core.model import LibrasModel
from core.translator import TranslatorEngine
from core.data_manager import DataManager
from ui.video_widget import VideoWidget
from ui.training_dialog import TrainingDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LIBRAS to Speech - Ao Vivo")
        self.resize(1024, 768)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e1e; color: #ffffff; }
            QLabel { color: #ffffff; font-size: 14px; }
            QPushButton { 
                background-color: #007acc; 
                color: white; 
                border: none; 
                padding: 10px; 
                border-radius: 5px; 
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #005999; }
            QListWidget { 
                background-color: #2d2d2d; 
                color: white; 
                border: 1px solid #3d3d3d; 
                font-size: 16px; 
                padding: 5px;
            }
        """)

        # Core Components
        self.vision = VisionProcessor()
        self.model = LibrasModel()
        self.translator = TranslatorEngine()
        self.data_manager = DataManager()
        
        # Connect Translator Signals
        self.translator.word_updated.connect(self.update_current_word)
        self.translator.history_updated.connect(self.update_history)
        
        # Training Data Collection State
        self.is_collecting = False
        self.collect_label = ""
        self.current_session_landmarks = []  # Buffer for the current collection session

        self.init_ui()
        
        # Camera Setup
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30) # ~33 fps

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left Panel - Video
        left_panel = QVBoxLayout()
        self.video_widget = VideoWidget()
        left_panel.addWidget(self.video_widget, stretch=1)
        
        # Current translation overlay/label
        self.lbl_current_word = QLabel("Palavra atual: ")
        self.lbl_current_word.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        left_panel.addWidget(self.lbl_current_word)
        
        # Right Panel - Controls & History
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(10, 0, 0, 0)
        
        lbl_history = QLabel("Histórico de Tradução:")
        lbl_history.setStyleSheet("font-weight: bold;")
        right_panel.addWidget(lbl_history)
        
        self.list_history = QListWidget()
        right_panel.addWidget(self.list_history)
        
        # Buttons
        self.btn_pause = QPushButton("Pausar Tradução")
        self.btn_pause.clicked.connect(self.toggle_pause)
        right_panel.addWidget(self.btn_pause)
        
        self.btn_clear = QPushButton("Limpar Histórico")
        self.btn_clear.clicked.connect(self.translator.clear_history)
        right_panel.addWidget(self.btn_clear)
        
        self.btn_replay = QPushButton("Ouvir Tradução Novamente")
        self.btn_replay.clicked.connect(self.translator.replay_last)
        right_panel.addWidget(self.btn_replay)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        right_panel.addWidget(line)
        
        self.btn_train = QPushButton("Modo de Treinamento")
        self.btn_train.setStyleSheet("background-color: #d84315; color: white;")
        self.btn_train.clicked.connect(self.open_training_dialog)
        right_panel.addWidget(self.btn_train)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, stretch=7)
        main_layout.addLayout(right_panel, stretch=3)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
            
        frame = cv2.flip(frame, 1) # Mirror
        
        annotated_frame, landmarks = self.vision.process_frame(frame)
        
        # Draw current prediction on screen
        current_pred = "Nenhum"
        
        prediction = None
        if landmarks:
            if self.is_collecting:
                # Buffer landmarks for the current session
                self.current_session_landmarks.append(landmarks)
                if hasattr(self, 'training_dialog') and self.training_dialog.isVisible():
                    self.training_dialog.update_count(len(self.current_session_landmarks))
            else:
                # Inference
                prediction = self.model.predict(landmarks)
                if prediction:
                    current_pred = prediction
        
        # Always feed prediction (could be None) to translator when not collecting data
        if not self.is_collecting:
            self.translator.process_prediction(prediction)
        
        # Draw info
        cv2.putText(annotated_frame, f"Sinal: {current_pred}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
        self.video_widget.update_frame(annotated_frame)

    def update_current_word(self, text):
        self.lbl_current_word.setText(f"Palavra atual: {text}")
        
    def update_history(self, history_list):
        self.list_history.clear()
        self.list_history.addItems(history_list)
        self.list_history.scrollToBottom()

    def toggle_pause(self):
        is_paused = self.translator.toggle_pause()
        self.btn_pause.setText("Retomar Tradução" if is_paused else "Pausar Tradução")
        self.btn_pause.setStyleSheet(
            "background-color: #ff9800; color: white;" if is_paused else 
            "background-color: #007acc; color: white;"
        )

    def open_training_dialog(self):
        self.training_dialog = TrainingDialog(self.data_manager, self)
        self.training_dialog.collect_data_signal.connect(self.set_collecting_state)
        self.training_dialog.train_model_signal.connect(self.train_model_from_data)
        self.training_dialog.delete_session_signal.connect(self.delete_session)
        self.training_dialog.exec()
        
    def set_collecting_state(self, label, is_collecting):
        if self.is_collecting and not is_collecting:
            # Stopping collection: save the session
            if self.current_session_landmarks:
                self.data_manager.add_session(label, self.current_session_landmarks)
                self.current_session_landmarks = []
                if hasattr(self, 'training_dialog') and self.training_dialog.isVisible():
                    self.training_dialog.on_session_saved()
        elif not self.is_collecting and is_collecting:
            # Starting a new collection: reset buffer
            self.current_session_landmarks = []
            
        self.collect_label = label
        self.is_collecting = is_collecting
        
    def train_model_from_data(self):
        X, y = self.data_manager.get_aggregated_data()
        if len(X) > 0:
            self.model.train(X, y)
            if hasattr(self, 'training_dialog') and self.training_dialog.isVisible():
                self.training_dialog.show_training_success()
        else:
            QMessageBox.warning(self, "Aviso", "Nenhum dado coletado! Colete dados primeiro.")

    def delete_session(self, session_id):
        self.data_manager.delete_session(session_id)
        if hasattr(self, 'training_dialog') and self.training_dialog.isVisible():
            self.training_dialog.on_session_saved()

    def closeEvent(self, event):
        self.cap.release()
        self.vision.close()
        event.accept()
