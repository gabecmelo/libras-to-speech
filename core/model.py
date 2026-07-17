import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class LibrasModel:
    def __init__(self, model_filename="libras_model.pkl"):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, model_filename)
        self.model = None
        self.load_model()
        
    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
                
    def save_model(self):
        if self.model is not None:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
                
    def train(self, X, y):
        """
        X: list of landmark lists (features)
        y: list of string labels
        """
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self.save_model()
        
    def predict(self, landmarks):
        if self.model is None:
            return None
            
        X_infer = np.array(landmarks).reshape(1, -1)
        
        prediction = self.model.predict(X_infer)[0]
        
        probs = self.model.predict_proba(X_infer)[0]
        max_prob = np.max(probs)
        
        if max_prob > 0.5:
            return prediction
        return None
