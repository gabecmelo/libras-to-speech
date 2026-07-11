from PyQt6.QtCore import QObject, pyqtSignal
from core.tts import TTSEngine

class TranslatorEngine(QObject):
    word_updated = pyqtSignal(str)
    history_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.tts = TTSEngine()
        
        self.current_word = ""
        self.history = []
        
        self.last_predicted = None
        self.consecutive_frames = 0
        self.debounce_threshold = 15 # Wait for 15 consecutive frames of the same prediction
        
        self.is_paused = False
        
    def process_prediction(self, prediction):
        if self.is_paused or prediction is None:
            return
            
        if prediction == self.last_predicted:
            self.consecutive_frames += 1
        else:
            self.last_predicted = prediction
            self.consecutive_frames = 1
            
        if self.consecutive_frames == self.debounce_threshold:
            self._handle_confirmed_prediction(prediction)

    def _handle_confirmed_prediction(self, letter):
        if letter == "ENTER":
            if self.current_word.strip():
                sentence = self.current_word.strip()
                self.history.append(sentence)
                self.history_updated.emit(self.history)
                self.tts.speak(sentence)
                self.current_word = ""
                self.word_updated.emit(self.current_word)
        elif letter == "ESPAÇO":
            if self.current_word and not self.current_word.endswith(" "):
                self.current_word += " "
                self.word_updated.emit(self.current_word)
        elif letter == "APAGAR":
            if len(self.current_word) > 0:
                self.current_word = self.current_word[:-1]
                self.word_updated.emit(self.current_word)
        else:
            # Regular letter
            self.current_word += letter
            self.word_updated.emit(self.current_word)
            
    def clear_history(self):
        self.history.clear()
        self.current_word = ""
        self.word_updated.emit(self.current_word)
        self.history_updated.emit(self.history)
        
    def replay_last(self):
        if self.history:
            self.tts.speak(self.history[-1])
            
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused
