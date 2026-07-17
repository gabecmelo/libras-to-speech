from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QByteArray, QSize, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPainter

class Icons:
    SVG_STUDIO = """<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="2.5"></circle><path d="M7.8 7.8a6 6 0 0 0 0 8.4"></path><path d="M16.2 7.8a6 6 0 0 1 0 8.4"></path><path d="M4.9 4.9a10 10 0 0 0 0 14.2"></path><path d="M19.1 4.9a10 10 0 0 1 0 14.2"></path></svg>"""
    SVG_TRAINING = """<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"></circle><circle cx="12" cy="12" r="4.5"></circle><circle cx="12" cy="12" r="1"></circle></svg>"""
    SVG_LIBRARY = """<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="3" width="7.5" height="7.5" rx="1.5"></rect><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"></rect><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"></rect><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"></rect></svg>"""
    SVG_SETTINGS = """<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33h0a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51h0a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82v0a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>"""
    SVG_LOGO = """<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round"><path d="M7 11V7a5 5 0 0 1 10 0v4"></path><path d="M5 11h14v2a7 7 0 0 1-14 0v-2z"></path></svg>"""

    @classmethod
    def get_icon(cls, svg_template, color="#8B959B", size=QSize(24, 24)):
        svg_str = svg_template.format(color=color)
        renderer = QSvgRenderer(QByteArray(svg_str.encode('utf-8')))
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return QIcon(pixmap)
