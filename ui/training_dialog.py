from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QMessageBox)
from PyQt6.QtCore import pyqtSignal

class TrainingDialog(QDialog):
    # Signals: letter to collect, boolean indicating to start/stop
    collect_data_signal = pyqtSignal(str, bool)
    train_model_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Treinar Modelo de LIBRAS")
        self.resize(300, 200)
        
        layout = QVBoxLayout()
        
        info_label = QLabel("Selecione a letra/gesto para coletar dados.\nSegure a pose da mão em frente à câmera.")
        layout.addWidget(info_label)
        
        self.combo = QComboBox()
        # Add A-Z, ESPAÇO, ENTER, APAGAR
        gestures = [chr(i) for i in range(ord('A'), ord('Z')+1)] + ["ESPAÇO", "ENTER", "APAGAR"]
        self.combo.addItems(gestures)
        layout.addWidget(self.combo)
        
        self.btn_collect = QPushButton("Iniciar Coleta")
        self.btn_collect.setCheckable(True)
        self.btn_collect.clicked.connect(self.toggle_collect)
        layout.addWidget(self.btn_collect)
        
        self.lbl_status = QLabel("Aguardando...")
        layout.addWidget(self.lbl_status)
        
        self.btn_train = QPushButton("Treinar e Salvar Modelo")
        self.btn_train.clicked.connect(self.train_model)
        layout.addWidget(self.btn_train)
        
        self.setLayout(layout)
        
    def toggle_collect(self):
        is_collecting = self.btn_collect.isChecked()
        letter = self.combo.currentText()
        if is_collecting:
            self.btn_collect.setText("Parar Coleta")
            self.lbl_status.setText(f"Coletando dados para: {letter}")
        else:
            self.btn_collect.setText("Iniciar Coleta")
            self.lbl_status.setText("Coleta pausada.")
            
        self.collect_data_signal.emit(letter, is_collecting)
        
    def update_count(self, count):
        self.lbl_status.setText(f"Coletando: {self.combo.currentText()} - Frames: {count}")
        
    def train_model(self):
        # Stop collecting if we were
        if self.btn_collect.isChecked():
            self.btn_collect.click()
            
        self.lbl_status.setText("Treinando modelo... Aguarde.")
        self.train_model_signal.emit()
        
    def show_training_success(self):
        self.lbl_status.setText("Modelo treinado com sucesso!")
        QMessageBox.information(self, "Sucesso", "O modelo foi treinado e salvo com sucesso!")
