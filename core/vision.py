import cv2
import mediapipe as mp
import numpy as np

class VisionProcessor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process_frame(self, frame):
        """
        Processes a BGR frame from OpenCV.
        Returns the annotated frame and a list of normalized landmarks if a hand is detected.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = self.hands.process(rgb_frame)
        
        annotated_frame = frame.copy()
        landmarks_list = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                landmarks_list = []
                wrist = hand_landmarks.landmark[0]
                
                for lm in hand_landmarks.landmark:
                    landmarks_list.append(lm.x - wrist.x)
                    landmarks_list.append(lm.y - wrist.y)
                    landmarks_list.append(lm.z - wrist.z)
                    
            return annotated_frame, landmarks_list
            
        return annotated_frame, None

    def close(self):
        self.hands.close()
