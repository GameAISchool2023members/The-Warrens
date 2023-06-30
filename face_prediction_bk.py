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
        self.video = cv2.VideoCapture(0) if sys.platform == 'darwin' else cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        # show the frame
        # cv2.imshow('frame', fr)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     return

        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)
        
        assert faces is not None, 'No faces at all?'
        cropped_faces = []
        predicted_emotions = []

        for i, (x, y, w, h) in enumerate(faces):
            fc = gray_fr[y:y+h, x:x+w]
            
            cropped_faces.append(cv2.resize(fc, (512, 512)))

            roi = cv2.resize(fc, (48, 48))
            predicted_emotions.append(configs.expressions.index(model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])))
        
        if len(cropped_faces) == 1:
            cropped_faces.append(np.zeros_like(cropped_faces[0]))
        
        return cropped_faces, predicted_emotions
