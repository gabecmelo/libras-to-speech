from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from ui.icons import Icons

class SidebarWidget(QFrame):
    view_changed = pyqtSignal(str) # Emits the name of the view to switch to

    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(200)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        brand_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_label.setPixmap(Icons.get_icon(Icons.SVG_LOGO, color="#4CC38A", size=QSize(20, 20)).pixmap(QSize(20, 20)))
        brand_text = QLabel("Libras-to-Speech")
        brand_text.setStyleSheet("font-weight: 600; color: #E7ECEE;")
        brand_layout.addWidget(logo_label)
        brand_layout.addWidget(brand_text)
        brand_layout.addStretch()
        self.layout.addLayout(brand_layout)
        
        self.layout.addSpacing(15)

        self.btn_studio = self.create_nav_button("Estúdio", Icons.SVG_STUDIO, "studio")
        self.btn_training = self.create_nav_button("Treinamento", Icons.SVG_TRAINING, "training")
        self.btn_library = self.create_nav_button("Biblioteca", Icons.SVG_LIBRARY, "library")
        self.btn_settings = self.create_nav_button("Configurações", Icons.SVG_SETTINGS, "settings")

        self.buttons = {
            "studio": self.btn_studio,
            "training": self.btn_training
        }

        self.layout.addWidget(self.btn_studio)
        self.layout.addWidget(self.btn_training)
        
        self.layout.addStretch()

        self.set_active("studio")

    def create_nav_button(self, text, icon_svg, view_name):
        btn = QPushButton(f"  {text}")
        btn.setObjectName("SidebarButton")
        btn.setIcon(Icons.get_icon(icon_svg, color="#8B959B", size=QSize(18, 18)))
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.on_button_clicked(view_name))
        return btn

    def on_button_clicked(self, view_name):
        self.set_active(view_name)
        self.view_changed.emit(view_name)

    def set_active(self, view_name):
        for name, btn in self.buttons.items():
            is_active = (name == view_name)
            btn.setChecked(is_active)
            if is_active:
                btn.setIcon(Icons.get_icon(getattr(Icons, f"SVG_{name.upper()}"), color="#4CC38A", size=QSize(18, 18)))
            else:
                btn.setIcon(Icons.get_icon(getattr(Icons, f"SVG_{name.upper()}"), color="#8B959B", size=QSize(18, 18)))
