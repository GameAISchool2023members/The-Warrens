import pygame
import numpy as np
import cv2
import os
from face_prediction import VideoCamera

pygame.init()

class EncounterGUI:
    def __init__(self) -> None:
        self.background = pygame.image.load('assets/encounter.jpg')
        self.faces_positions = [(168, 372), (436, 384)]
        self.h, self.w = 720, 1280
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.camera = VideoCamera()

        ratio_h, ratio_w = self.h / 768, self.w / 768
        for i, face_position in enumerate(self.faces_positions):
            self.faces_positions[i] = (face_position[0] * ratio_w,
                                       face_position[1] * ratio_h)
#         print(self.faces_positions)

        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (0, 0))
        self.update_screen([])
    
    def update_screen(self,
                      faces):
        cropped_faces, predicted_emotions = self.camera.get_frame()
        for face, face_position in zip(cropped_faces, self.faces_positions):
            print(face.shape)
#             fixed_face = np.expand_dims(face.T, axis=-1)
            fixed_face = face.T
            print(fixed_face.shape)
            
            self.screen.blit(pygame.transform.scale(pygame.surfarray.make_surface(fixed_face), (250, 250)), (face_position[0], face_position[1] - 250))
#               pygame.draw.circle(self.screen, (0, 0, 0), face_position, 20)
        pygame.display.flip()

    
    def render(self, faces):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.update_screen(faces)
            pygame.display.flip()


if __name__ == "__main__":
    gui = EncounterGUI()

    faces = [
        np.random.rand(512, 512),
        np.random.rand(512, 512)*255
    ]

    gui.render(faces)
    # cooldown period