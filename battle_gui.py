import pygame
import numpy as np
import cv2
import os

pygame.init()

class EncounterGUI:
    def __init__(self) -> None:
        self.background = pygame.image.load('assets/encounter.jpg')
        self.faces_positions = [(168, 372), (436, 384)]
        self.h, self.w = 720, 1280
        self.screen = pygame.display.set_mode((self.w, self.h))

        ratio_h, ratio_w = self.h / 768, self.w / 768
        for i, face_position in enumerate(self.faces_positions):
            self.faces_positions[i] = (face_position[1] * ratio_w,
                                       face_position[0] * ratio_h)

        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (0, 0))
        self.update_screen([])
    
    def update_screen(self,
                      faces):
        for face, face_position in zip(faces, self.faces_positions):
            self.screen.blit(pygame.transform.scale(pygame.surfarray.make_surface(face), (250, 250)), (face_position[1], face_position[0]))
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