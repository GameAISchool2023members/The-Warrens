import cv2
from model import FacialExpressionModel
import numpy as np
import os
import sys

from configs import configs

facec = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        # Use correct camera index for Mac and PC ¯\_(ツ)_/¯
        self.video = cv2.VideoCapture(1 if sys.platform == 'darwin' else 0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()

        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)
        # keep faces ordered
        faces = sorted(faces, key=lambda x: -x[0])
        
        assert faces is not None, 'No faces at all?'
        cropped_faces = [np.zeros((512, 512)) for _ in range(2)]  # empty faces
        predicted_emotions = [-1, -1]  # no predictions

        # weird for-loop because camera can get either 0 or more faces, but we always want 2
        for i in range(len(cropped_faces)):
            if i < len(faces):
                x, y, w, h = faces[i]
                fc = gray_fr[y:y+h, x:x+w]
                roi = cv2.resize(fc, (48, 48))

                cropped_faces[i] = cv2.resize(fc, (512, 512))
                predicted_emotions[i] = configs.expressions.index(model.predict_emotion(roi[np.newaxis, :, :, np.newaxis]))
        
        return cropped_faces, predicted_emotions
