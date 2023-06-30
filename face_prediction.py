import cv2
from model import FacialExpressionModel
import numpy as np
import os
import sys
import pygame

from configs import configs

facec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self, n_players=2):
        # Use correct camera index for Mac and PC ¯\_(ツ)_/¯
        self.video = cv2.VideoCapture(1 if sys.platform == 'darwin' else 0)
        self.no_face = pygame.image.load('assets/noface.png')
        self.processed_faces = [self.no_face for _ in range(n_players)]
        self.predicted_emotions = [-1 for _ in range(n_players)]
        self.patience = [30 for _ in range(n_players)]
        self.bboxes_at = [-1 for _ in range(n_players)]
        
    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()

        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)
        # keep faces ordered
        faces = sorted(faces, key=lambda x: -x[0])
        
        for i in range(len(self.patience)):
            self.patience[i] -= 1
        
        for i, (x, y, w, h) in enumerate(faces):
            if i < len(self.processed_faces):
                fc = gray_fr[y:y+h, x:x+w]
                roi = cv2.resize(fc, (48, 48))
                
                cropped_face = cv2.resize(fc, (512, 512))
                predicted_emotion = configs.expressions.index(model.predict_emotion(roi[np.newaxis, :, :, np.newaxis]))
                
                if self.bboxes_at[i] == -1:
                    at = i
                else:
                    at = np.argmin([abs(x - y) for y in self.bboxes_at])
    
                self.processed_faces[at] = cropped_face
                self.predicted_emotions[at] = predicted_emotion
                self.patience[at] = 50
                self.bboxes_at[at] = x
                
        for i in range(len(self.patience)):
            if 0 < self.patience[i] < 30:
                self.predicted_emotions[i] = -1
            elif self.patience[i] <= 0:
                self.predicted_emotions[i] = -1
                self.processed_faces[i] = self.no_face
                self.bboxes_at[i] = -1
        
        return self.processed_faces, self.predicted_emotions
