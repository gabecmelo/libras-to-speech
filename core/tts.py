import pyttsx3
from PyQt6.QtCore import QThread, pyqtSignal

class TTSWorker(QThread):
    finished = pyqtSignal()
    
    def __init__(self, text):
        super().__init__()
        self.text = text
        
    def run(self):
        engine = pyttsx3.init()
        # Set to Portuguese voice if available
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'brazil' in voice.name.lower() or 'pt-br' in voice.id.lower() or 'portuguese' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.say(self.text)
        engine.runAndWait()
        self.finished.emit()

class TTSEngine:
    def __init__(self):
        self.worker = None

    def speak(self, text):
        if self.worker is not None and self.worker.isRunning():
            # If already speaking, maybe we skip or queue. For now, skip to avoid overlap chaos.
            pass
        self.worker = TTSWorker(text)
        self.worker.start()
