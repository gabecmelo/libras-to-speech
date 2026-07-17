from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QListWidget, QListWidgetItem, 
                               QStackedWidget, QLineEdit, QComboBox, QTableWidget,
                               QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox)
from PyQt6.QtCore import Qt
import cv2
import datetime
from ui.video_widget import VideoWidget

class StudioWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.is_deaf_mode = True
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        left_panel = QVBoxLayout()
        
        header_layout = QHBoxLayout()
        title = QLabel("Estúdio (Modo Surdo)")
        title.setObjectName("Title")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        left_panel.addLayout(header_layout)
        
        self.video_widget = VideoWidget()
        self.video_widget.setStyleSheet("background-color: #101417; border: 1px solid #21272B; border-radius: 12px;")
        left_panel.addWidget(self.video_widget, stretch=1)
        
        right_panel = QVBoxLayout()
        
        log_card = QFrame()
        log_card.setObjectName("Card")
        log_layout = QVBoxLayout(log_card)
        
        log_title = QLabel("Log de tradução")
        log_title.setStyleSheet("font-weight: 600; font-size: 14px;")
        log_layout.addWidget(log_title)
        
        self.log_list = QListWidget()
        self.log_list.setStyleSheet("border: none; background: transparent; outline: none;")
        log_layout.addWidget(self.log_list)
        
        typing_layout = QHBoxLayout()
        typing_layout.addWidget(QLabel("⏳"))
        self.typing_label = QLabel("")
        self.typing_label.setStyleSheet("font-size: 14px; color: #E7ECEE; padding: 4px;")
        typing_layout.addWidget(self.typing_label, stretch=1)
        log_layout.addLayout(typing_layout)
        
        right_panel.addWidget(log_card, stretch=1)
        
        obs_card = QFrame()
        obs_card.setObjectName("Card")
        obs_layout = QVBoxLayout(obs_card)
        
        obs_title = QLabel("Overlay para OBS")
        obs_title.setStyleSheet("font-weight: 600; font-size: 14px;")
        obs_layout.addWidget(obs_title)
        
        obs_link_layout = QHBoxLayout()
        obs_link = QLineEdit("http://localhost:8080/overlay")
        obs_link.setReadOnly(True)
        btn_copy = QPushButton("Copiar")
        obs_link_layout.addWidget(obs_link)
        obs_link_layout.addWidget(btn_copy)
        obs_layout.addLayout(obs_link_layout)
        
        obs_desc = QLabel("Adicione como Browser Source no OBS.")
        obs_desc.setStyleSheet("color: #5E686E; font-size: 12px;")
        obs_layout.addWidget(obs_desc)
        
        right_panel.addWidget(obs_card)
        
        main_layout.addLayout(left_panel, stretch=7)
        main_layout.addLayout(right_panel, stretch=3)
        
        self.current_word = ""
        self.main_window.translator.history_updated.connect(self.on_history_updated)
        self.main_window.translator.word_updated.connect(self.on_word_updated)
        
    def on_word_updated(self, word):
        self.current_word = word
        if word:
            self.typing_label.setText(f"{word}_")
        else:
            self.typing_label.setText("")
        
    def on_history_updated(self, history_list):
        self.log_list.clear()
        for text in history_list:
            time_str = datetime.datetime.now().strftime("%H:%M:%S")
            self.add_log(text, time_str, "Você")
        
    def update_frame(self, cv_img, landmarks):
        current_pred = ""
        prediction = None
        if landmarks:
            prediction = self.main_window.model.predict(landmarks)
            if prediction:
                current_pred = prediction
        
        self.main_window.translator.process_prediction(prediction)
        
        if current_pred:
            cv2.putText(cv_img, f"Caractere atual: {current_pred}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            
        if self.current_word:
            h, w = cv_img.shape[:2]
            cv2.putText(cv_img, self.current_word, (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            
        self.video_widget.update_frame(cv_img)
            
    def add_log(self, text, time_str, conf_str):
        item = QListWidgetItem(f"🟢 {text}\n   {time_str} • {conf_str}")
        self.log_list.addItem(item)
        self.log_list.scrollToBottom()


class TrainingWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Treinamento de sinais")
        title.setObjectName("Title")
        desc = QLabel("Selecione a letra/gesto para coletar dados.")
        desc.setObjectName("Subtitle")
        
        layout.addWidget(title)
        layout.addWidget(desc)
        
        content_layout = QHBoxLayout()
        
        video_layout = QVBoxLayout()
        self.video_widget = VideoWidget()
        self.video_widget.setStyleSheet("background-color: #101417; border: 1px solid #21272B; border-radius: 12px;")
        video_layout.addWidget(self.video_widget, stretch=1)
        
        self.btn_record = QPushButton("Gravar Amostra")
        self.btn_record.setObjectName("PrimaryButton")
        video_layout.addWidget(self.btn_record)
        
        self.lbl_status = QLabel("Pronto para gravar.")
        self.lbl_status.setStyleSheet("color: #4CC38A; font-weight: bold;")
        video_layout.addWidget(self.lbl_status)
        
        content_layout.addLayout(video_layout, stretch=7)
        
        form_layout = QVBoxLayout()
        
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        
        card_layout.addWidget(QLabel("Selecione o Gesto"))
        self.sign_combo = QComboBox()
        gestures = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["ESPAÇO", "ENTER", "APAGAR"]
        self.sign_combo.addItems(gestures)
        card_layout.addWidget(self.sign_combo)
        
        card_layout.addWidget(QLabel("Histórico de Sessões:"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Gesto", "Frames", "Data"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("background-color: transparent; border: 1px solid #2A3136;")
        card_layout.addWidget(self.table)
        
        self.btn_save = QPushButton("Treinar e Salvar Modelo")
        self.btn_save.setObjectName("PrimaryButton")
        card_layout.addWidget(self.btn_save)
        
        form_layout.addWidget(card)
        form_layout.addStretch()
        content_layout.addLayout(form_layout, stretch=3)
        
        layout.addLayout(content_layout)
        
        self.is_collecting = False
        self.current_session_landmarks = []
        self.btn_record.clicked.connect(self.toggle_recording)
        self.btn_save.clicked.connect(self.save_sign)
        
        self._refresh_table()
        
    def _refresh_table(self):
        sessions = self.main_window.data_manager.get_all_sessions()
        self.table.setRowCount(len(sessions))
        for i, s in enumerate(sessions):
            self.table.setItem(i, 0, QTableWidgetItem(s.session_id))
            self.table.setItem(i, 1, QTableWidgetItem(s.label))
            self.table.setItem(i, 2, QTableWidgetItem(str(s.frame_count)))
            self.table.setItem(i, 3, QTableWidgetItem(s.timestamp))
        
    def toggle_recording(self):
        self.is_collecting = not self.is_collecting
        if self.is_collecting:
            self.current_session_landmarks = []
            self.btn_record.setText("Parar Gravação")
            self.btn_record.setStyleSheet("background-color: #E5484D; border: none; color: white;")
            self.lbl_status.setText("Capturando frames: 0")
        else:
            self.btn_record.setText("Gravar Amostra")
            self.btn_record.setStyleSheet("")
            sign_name = self.sign_combo.currentText()
            if self.current_session_landmarks:
                self.main_window.data_manager.add_session(sign_name, self.current_session_landmarks)
                self._refresh_table()
                self.lbl_status.setText(f"Sessão salva com {len(self.current_session_landmarks)} frames.")
                
    def save_sign(self):
        self.lbl_status.setText("Treinando modelo, aguarde...")
        self.main_window.repaint() # Force UI update before blocking training
        X, y = self.main_window.data_manager.get_aggregated_data()
        if len(X) > 0:
            self.main_window.model.train(X, y)
            self.lbl_status.setText("Modelo treinado com sucesso!")
        else:
            self.lbl_status.setText("Erro: Nenhum dado coletado para treinar.")
        
    def update_frame(self, cv_img, landmarks):
        if self.is_collecting and landmarks:
            self.current_session_landmarks.append(landmarks)
            self.lbl_status.setText(f"Capturando frames: {len(self.current_session_landmarks)}")
        self.video_widget.update_frame(cv_img)


class LibraryWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Biblioteca de sinais")
        title.setObjectName("Title")
        desc = QLabel("Sinais do modelo universal e os que você treinou.")
        desc.setObjectName("Subtitle")
        
        layout.addWidget(title)
        layout.addWidget(desc)
        
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(QLabel("Universal Model: Ativo (1.240 sinais)"))
        layout.addWidget(card)
        
        layout.addWidget(QLabel("Sinais personalizados (0)"))
        self.signs_list = QListWidget()
        layout.addWidget(self.signs_list)
        
        layout.addStretch()


class SettingsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Configurações")
        title.setObjectName("Title")
        layout.addWidget(title)
        
        card = QFrame()
        card.setObjectName("Card")
        card_layout = QVBoxLayout(card)
        
        card_layout.addWidget(QLabel("Câmera e captura"))
        
        cam_layout = QHBoxLayout()
        cam_layout.addWidget(QLabel("Dispositivo"))
        self.cam_combo = QComboBox()
        self.cam_combo.addItems(["Câmera Padrão"])
        cam_layout.addWidget(self.cam_combo)
        card_layout.addLayout(cam_layout)
        
        layout.addWidget(card)
        layout.addStretch()
