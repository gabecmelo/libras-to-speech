import os
import json
import uuid
from datetime import datetime

DATA_DIR = "training_data"
SESSIONS_FILE = os.path.join(DATA_DIR, "sessions.json")

class TrainingSession:
    """Represents a single data collection session."""
    def __init__(self, session_id, label, timestamp, frame_count, landmarks):
        self.session_id = session_id
        self.label = label
        self.timestamp = timestamp
        self.frame_count = frame_count
        self.landmarks = landmarks  # list of landmark lists

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "label": self.label,
            "timestamp": self.timestamp,
            "frame_count": self.frame_count,
            "landmarks": self.landmarks,
        }

    @staticmethod
    def from_dict(data):
        return TrainingSession(
            session_id=data["session_id"],
            label=data["label"],
            timestamp=data["timestamp"],
            frame_count=data["frame_count"],
            landmarks=data["landmarks"],
        )


class DataManager:
    """Manages training data sessions with full history and per-session deletion."""

    def __init__(self):
        self.sessions = []
        os.makedirs(DATA_DIR, exist_ok=True)
        self._load_sessions()

    def _load_sessions(self):
        if os.path.exists(SESSIONS_FILE):
            try:
                with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.sessions = [TrainingSession.from_dict(s) for s in data]
            except (json.JSONDecodeError, KeyError):
                self.sessions = []
        else:
            self.sessions = []

    def _save_sessions(self):
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump([s.to_dict() for s in self.sessions], f, ensure_ascii=False)

    def add_session(self, label, landmarks):
        """Creates and persists a new training session."""
        session = TrainingSession(
            session_id=str(uuid.uuid4())[:8],
            label=label,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            frame_count=len(landmarks),
            landmarks=landmarks,
        )
        self.sessions.append(session)
        self._save_sessions()
        return session

    def delete_session(self, session_id):
        """Deletes a single session by its ID."""
        self.sessions = [s for s in self.sessions if s.session_id != session_id]
        self._save_sessions()

    def get_all_sessions(self):
        """Returns a list of all sessions (metadata only, no heavy data)."""
        return self.sessions

    def get_aggregated_data(self):
        """Aggregates all sessions into X, y arrays for training."""
        X = []
        y = []
        for session in self.sessions:
            for lm in session.landmarks:
                X.append(lm)
                y.append(session.label)
        return X, y

    def get_summary(self):
        """Returns a dict of label -> total frame count across all sessions."""
        summary = {}
        for s in self.sessions:
            summary[s.label] = summary.get(s.label, 0) + s.frame_count
        return summary
