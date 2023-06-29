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

        ratio_h, ratio_w = 768 / self.h, 768 / self.w
        for face_position in self.faces_positions:
            

        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (0, 0))
        self.update_screen([])
    
    def update_screen(self,
                      faces):
        # self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (self.h, self.w))
        # self.screen = pygame.display.set_mode((self.w, self.h))
        for face, face_position in zip(faces, self.faces_positions):
            # convert face to pygame surface
            face = pygame.surfarray.make_surface(face)
            self.screen.blit(face, face_position)
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
        np.random.rand(512, 512)
    ]

    gui.render(faces)