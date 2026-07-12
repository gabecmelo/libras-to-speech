from collections import deque
from PyQt6.QtCore import QObject, pyqtSignal
from spellchecker import SpellChecker
from core.tts import TTSEngine

class TranslatorEngine(QObject):
    word_updated = pyqtSignal(str)
    history_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.tts = TTSEngine()
        
        # Spell Checker initialization for Portuguese
        try:
            self.spell = SpellChecker(language='pt')
        except Exception:
            # Fallback if dictionary cannot be loaded offline
            self.spell = None
            
        self.current_word = ""  # This stores the active raw sentence/word builder
        self.history = []
        self.undo_stack = []    # Stack to keep previous states for APAGAR undo
        
        # Sliding Window for fast, robust voting
        self.window_size = 10
        self.prediction_window = deque(maxlen=self.window_size)
        self.last_confirmed = None
        
        # Hand presence tracking
        self.no_hand_counter = 0
        self.no_hand_threshold = 15  # Reset confirmed letter if hand is absent for ~0.5s
        
        self.repeat_counter = 0 # Counter for APAGAR auto-repeat
        self.is_paused = False
        
    def process_prediction(self, prediction):
        if self.is_paused:
            return
            
        if prediction is None:
            # Hand is absent
            self.no_hand_counter += 1
            if self.no_hand_counter >= self.no_hand_threshold:
                self.prediction_window.clear()
                self.last_confirmed = None
                self.repeat_counter = 0
            return
            
        # Hand is present
        self.no_hand_counter = 0
        self.prediction_window.append(prediction)
        
        # Perform majority voting when window is full
        if len(self.prediction_window) == self.window_size:
            # Find the most frequent prediction in the window
            counts = {}
            for item in self.prediction_window:
                counts[item] = counts.get(item, 0) + 1
            
            most_frequent = max(counts, key=counts.get)
            frequency = counts[most_frequent]
            
            # Require at least 70% confidence in the window to trigger
            if frequency >= 7:
                if most_frequent != self.last_confirmed:
                    self.last_confirmed = most_frequent
                    self.repeat_counter = 0
                    self._handle_confirmed_prediction(most_frequent)
                    # Clear window to avoid double triggers without a gesture change
                    self.prediction_window.clear()
                else:
                    # Auto-repeat for APAGAR
                    if most_frequent == "APAGAR":
                        self.repeat_counter += 1
                        if self.repeat_counter >= 10:  # Repeat roughly every 0.33s
                            self.repeat_counter = 0
                            self._handle_confirmed_prediction("APAGAR")

    def _autocorrect_word(self, word):
        """Fixes the spelling of a single Portuguese word using pyspellchecker."""
        if not self.spell or not word.isalpha():
            return word
            
        # Ignore very short words (like "oi", "vc", "eu") to prevent false positives
        if len(word) <= 3:
            return word
        
        # If it's already considered correct, keep it
        # Otherwise, find the best correction
        word_lower = word.lower()
        misspelled = self.spell.unknown([word_lower])
        if misspelled:
            correction = self.spell.correction(word_lower)
            if correction:
                # Match original capitalization case
                if word.isupper():
                    return correction.upper()
                elif word[0].isupper():
                    return correction.capitalize()
                return correction
        return word

    def _autocorrect_sentence(self, sentence):
        """Autocorrects all words in a sentence."""
        words = sentence.split(" ")
        corrected_words = [self._autocorrect_word(w) for w in words]
        return " ".join(corrected_words)

    def _handle_confirmed_prediction(self, letter):
        if letter == "ENTER":
            if self.current_word.strip():
                # Correct the entire sentence before final TTS and history append
                raw_sentence = self.current_word.strip()
                corrected_sentence = self._autocorrect_sentence(raw_sentence)
                
                self.history.append(corrected_sentence)
                self.history_updated.emit(self.history)
                self.tts.speak(corrected_sentence)
                
                self.current_word = ""
                self.undo_stack.clear()
                self.word_updated.emit(self.current_word)
                
        elif letter == "ESPAÇO":
            if self.current_word and not self.current_word.endswith(" "):
                self.undo_stack.append(self.current_word)
                # Autocorrect the last typed word when space is pressed
                words = self.current_word.split(" ")
                if words:
                    last_word = words[-1]
                    corrected = self._autocorrect_word(last_word)
                    words[-1] = corrected
                    self.current_word = " ".join(words)
                
                self.current_word += " "
                self.word_updated.emit(self.current_word)
                
        elif letter == "APAGAR":
            if self.undo_stack:
                self.current_word = self.undo_stack.pop()
                self.word_updated.emit(self.current_word)
            elif len(self.current_word) > 0:
                self.current_word = self.current_word[:-1]
                self.word_updated.emit(self.current_word)
                
        else:
            # Regular letter
            self.undo_stack.append(self.current_word)
            self.current_word += letter
            self.word_updated.emit(self.current_word)
            
    def clear_history(self):
        self.history.clear()
        self.current_word = ""
        self.undo_stack.clear()
        self.word_updated.emit(self.current_word)
        self.history_updated.emit(self.history)
        
    def replay_last(self):
        if self.history:
            self.tts.speak(self.history[-1])
            
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused
