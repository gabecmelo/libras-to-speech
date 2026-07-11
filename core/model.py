import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class LibrasModel:
    def __init__(self, model_path="libras_model.pkl"):
        self.model_path = model_path
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
            
        # Reshape for a single sample
        X_infer = np.array(landmarks).reshape(1, -1)
        
        # Predict class
        prediction = self.model.predict(X_infer)[0]
        
        # Get probability
        probs = self.model.predict_proba(X_infer)[0]
        max_prob = np.max(probs)
        
        # Return prediction if confidence is reasonable
        if max_prob > 0.5:
            return prediction
        return None
