from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QComboBox, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QAbstractItemView, QTabWidget, QWidget)
from PyQt6.QtCore import pyqtSignal, Qt


class TrainingDialog(QDialog):
    # Signals: letter to collect, boolean indicating to start/stop
    collect_data_signal = pyqtSignal(str, bool)
    train_model_signal = pyqtSignal()
    delete_session_signal = pyqtSignal(str)  # session_id

    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.setWindowTitle("Treinar Modelo de LIBRAS")
        self.resize(600, 500)
        self.setStyleSheet("""
            QDialog { background-color: #1e1e1e; color: #ffffff; }
            QLabel { color: #ffffff; font-size: 13px; }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #005999; }
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 6px;
                font-size: 13px;
            }
            QTableWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                gridline-color: #3d3d3d;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #333333;
                color: white;
                padding: 4px;
                border: 1px solid #3d3d3d;
                font-weight: bold;
            }
            QTabWidget::pane { border: 1px solid #3d3d3d; }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: white;
                padding: 8px 16px;
                border: 1px solid #3d3d3d;
            }
            QTabBar::tab:selected { background-color: #007acc; }
        """)

        main_layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()

        # --- Tab 1: Coleta ---
        collect_tab = QWidget()
        collect_layout = QVBoxLayout(collect_tab)

        info_label = QLabel(
            "Selecione a letra/gesto para coletar dados.\n"
            "Segure a pose da mão em frente à câmera."
        )
        collect_layout.addWidget(info_label)

        self.combo = QComboBox()
        gestures = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + ["ESPAÇO", "ENTER", "APAGAR"]
        self.combo.addItems(gestures)
        collect_layout.addWidget(self.combo)

        self.btn_collect = QPushButton("Iniciar Coleta")
        self.btn_collect.setCheckable(True)
        self.btn_collect.clicked.connect(self.toggle_collect)
        collect_layout.addWidget(self.btn_collect)

        self.lbl_status = QLabel("Aguardando...")
        collect_layout.addWidget(self.lbl_status)

        # Summary of total frames per label
        self.lbl_summary = QLabel("")
        collect_layout.addWidget(self.lbl_summary)
        self._refresh_summary()

        self.btn_train = QPushButton("Treinar e Salvar Modelo")
        self.btn_train.clicked.connect(self.train_model)
        collect_layout.addWidget(self.btn_train)

        self.tabs.addTab(collect_tab, "Coletar Dados")

        # --- Tab 2: Histórico ---
        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)

        history_layout.addWidget(QLabel("Sessões de treinamento registradas:"))

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Gesto", "Frames", "Data/Hora", "Ação"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        history_layout.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.btn_delete_selected = QPushButton("Apagar Sessão Selecionada")
        self.btn_delete_selected.setStyleSheet("background-color: #c62828;")
        self.btn_delete_selected.clicked.connect(self.delete_selected_session)
        btn_row.addWidget(self.btn_delete_selected)

        self.btn_retrain = QPushButton("Retreinar Modelo (sem sessões apagadas)")
        self.btn_retrain.setStyleSheet("background-color: #ef6c00;")
        self.btn_retrain.clicked.connect(self.train_model)
        btn_row.addWidget(self.btn_retrain)

        history_layout.addLayout(btn_row)

        self.tabs.addTab(history_tab, "Histórico de Sessões")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self._refresh_table()

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
        self._refresh_table()
        self._refresh_summary()
        QMessageBox.information(self, "Sucesso", "O modelo foi treinado e salvo com sucesso!")

    def on_session_saved(self):
        """Called by MainWindow after a collection session is saved to the DataManager."""
        self._refresh_table()
        self._refresh_summary()

    def delete_selected_session(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Aviso", "Selecione uma sessão na tabela para apagar.")
            return

        row = selected_rows[0].row()
        session_id = self.table.item(row, 0).text()
        label = self.table.item(row, 1).text()

        reply = QMessageBox.question(
            self, "Confirmar",
            f"Tem certeza que deseja apagar a sessão '{session_id}' (gesto: {label})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_session_signal.emit(session_id)
            self._refresh_table()
            self._refresh_summary()

    def _refresh_table(self):
        sessions = self.data_manager.get_all_sessions()
        self.table.setRowCount(len(sessions))
        for i, s in enumerate(sessions):
            self.table.setItem(i, 0, QTableWidgetItem(s.session_id))
            self.table.setItem(i, 1, QTableWidgetItem(s.label))
            self.table.setItem(i, 2, QTableWidgetItem(str(s.frame_count)))
            self.table.setItem(i, 3, QTableWidgetItem(s.timestamp))
            self.table.setItem(i, 4, QTableWidgetItem("Selecione e clique Apagar"))

    def _refresh_summary(self):
        summary = self.data_manager.get_summary()
        if not summary:
            self.lbl_summary.setText("Nenhum dado coletado ainda.")
            return
        lines = [f"  {label}: {count} frames" for label, count in sorted(summary.items())]
        self.lbl_summary.setText("Resumo dos dados:\n" + "\n".join(lines))
