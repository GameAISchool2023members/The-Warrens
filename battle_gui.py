import pygame
import numpy as np
import cv2
import os
from face_prediction import VideoCamera

from configs import configs

pygame.init()

class EncounterGUI:
    def __init__(self) -> None:
        self.background = pygame.image.load('assets/encounter.jpg')
        self.faces_positions = [(210, 392), (436, 392)]
        self.h, self.w = configs.window_height, configs.window_width
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.camera = VideoCamera()
        
        self.total_life = configs.total_lives # Total_lifes to be defined
        self.circles_left = []
        self.life_tobe_consumed_left = self.total_life -1
        
        self.circles_right = []
        self.life_tobe_consumed_right = self.total_life -1
        
        self.create_circles() 
        
        # text at the bottom
        font = pygame.font.Font(None, self.h // 20)
        text_surface = font.render("Two AI researchers arguing in Cambribdge, brought by stable diffusion", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.bottom = self.screen.get_rect().bottom# - 10
        self.screen.blit(text_surface, text_rect)
        
        ratio_h, ratio_w = self.h / 768, self.w / 768
        for i, face_position in enumerate(self.faces_positions):
            self.faces_positions[i] = (face_position[0] * ratio_w,
                                       face_position[1] * ratio_h)

        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (0, 0))
        self.update_screen()
        
        
    # Draw players life (circles)
    def create_circles(self):
        # TODO: these values should be resized based on window size and amount
        circle_radius = 10
        circle_spacing = 10
        circle_top_left = (20, 20)
        for i in range(self.total_life):
            circle_center = (circle_top_left[0] + i * (circle_radius * 2 + circle_spacing), circle_top_left[1])
            self.circles_left.append((circle_center, circle_radius))
            pygame.draw.circle(self.screen, (255, 0, 0), circle_center, circle_radius)

        circle_top_right = (self.w - circle_top_left[0] - (circle_radius * 2 + circle_spacing) * 5, circle_top_left[1])
        for i in range(self.total_life):
            circle_center = (circle_top_right[0] + i * (circle_radius * 2 + circle_spacing), circle_top_right[1])
            self.circles_right.append((circle_center, circle_radius))
            pygame.draw.circle(self.screen, (255, 0, 0), circle_center, circle_radius)
        

    # Consuming player life (test for now with happy and angry face)
    def modify_circles(self, prediction):
        if prediction == 0: # happy (player left lose point, okay i know it's counter intuitive, fix it)
            if self.life_tobe_consumed_left >= 0:
                circle = self.circles_left[self.life_tobe_consumed_left]
                pygame.draw.circle(self.screen, (255, 255, 255), circle[0], circle[1])
                pygame.draw.circle(self.screen, (255, 0, 0), circle[0], circle[1], 1)
                self.life_tobe_consumed_left -=1
        elif prediction == 5: #angry (player right lose point)
            if self.life_tobe_consumed_right >= 0:
                circle = self.circles_right[self.life_tobe_consumed_right]
                pygame.draw.circle(self.screen, (255, 255, 255), circle[0], circle[1])
                pygame.draw.circle(self.screen, (255, 0, 0), circle[0], circle[1], 1)
                self.life_tobe_consumed_right -=1
    
    def update_screen(self):
        cropped_faces, predicted_emotions = self.camera.get_frame()  

        for face, face_position, predicted_emotion in zip(cropped_faces, self.faces_positions, predicted_emotions):
            if predicted_emotion != -1:
                fixed_face = cv2.cvtColor(face.T, cv2.COLOR_GRAY2RGB)
                self.screen.blit(pygame.transform.scale(pygame.surfarray.make_surface(fixed_face), (250, 250)), (face_position[0], face_position[1] - 250))
                # Beat the shit out of him
                self.modify_circles(predicted_emotion)
            
        pygame.display.flip()

        
    def render(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.update_screen()
            pygame.display.flip()


if __name__ == "__main__":
    gui = EncounterGUI()

    gui.render()
    # cooldown period