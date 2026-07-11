import pyttsx3
from PyQt6.QtCore import QThread, pyqtSignal

def _find_portuguese_voice(engine):
    """Search for a Brazilian Portuguese voice across SAPI5 voice properties."""
    voices = engine.getProperty('voices')
    # Priority: pt-BR first, then any Portuguese
    for voice in voices:
        voice_id_lower = voice.id.lower()
        voice_name_lower = voice.name.lower()
        if 'brazil' in voice_name_lower or 'pt-br' in voice_id_lower or 'brazilian' in voice_name_lower:
            return voice.id
    for voice in voices:
        voice_id_lower = voice.id.lower()
        voice_name_lower = voice.name.lower()
        if 'portug' in voice_name_lower or 'pt' in voice_id_lower:
            return voice.id
    return None

class TTSWorker(QThread):
    finished = pyqtSignal()
    
    def __init__(self, text):
        super().__init__()
        self.text = text
        
    def run(self):
        engine = pyttsx3.init()
        voice_id = _find_portuguese_voice(engine)
        if voice_id:
            engine.setProperty('voice', voice_id)
        
        engine.say(self.text)
        engine.runAndWait()
        self.finished.emit()

class TTSEngine:
    def __init__(self):
        self.worker = None

    def speak(self, text):
        if self.worker is not None and self.worker.isRunning():
            # If already speaking, skip to avoid overlap
            pass
        self.worker = TTSWorker(text)
        self.worker.start()
