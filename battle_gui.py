import pygame
import numpy as np
import cv2
import os
from face_prediction import VideoCamera

from utils import add_outline_to_image
from configs import configs

from battle import BattleLogic
from player import Player

pygame.init()
pygame.display.set_caption('Face2Face')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

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
        
        ratio_h, ratio_w = self.h / 768, self.w / 768
        for i, face_position in enumerate(self.faces_positions):
            self.faces_positions[i] = (face_position[0] * ratio_w,
                                       face_position[1] * ratio_h)

        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (0, 0))
        self.create_circles()
        self.make_title()
        self.update_screen()

        self.p1 = Player(id=1, hitpoints=5)
        self.p2 = Player(id=2, hitpoints=5)
        self.battlelogic = BattleLogic(self.p1, self.p2)
    
    def make_title(self):
        # text at the bottom
        font_size = self.h // 20
        font = pygame.font.Font(None, font_size)
        text_surface = font.render("Two AI researchers arguing in Cambribdge, brought by stable diffusion", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.bottom = self.screen.get_rect().bottom - font_size
        self.screen.blit(text_surface, text_rect)
        
    # Draw players life (circles)
    def create_circles(self):
        # TODO: these values should be resized based on window size and amount
        circle_radius = min(self.h // 20, self.w // (5 * (self.total_life * 2 + 1)))
        circle_spacing = circle_radius // 4
        circle_top_left = (circle_radius, circle_radius)
        for i in range(self.total_life):
            circle_center = (circle_top_left[0] + i * (circle_radius * 2 + circle_spacing), circle_top_left[1])
            self.circles_left.append((circle_center, circle_radius))
            pygame.draw.circle(self.screen, (255, 0, 0), circle_center, circle_radius)

        circle_top_right = (self.w - circle_radius, circle_radius)
        for i in range(self.total_life):
            circle_center = (circle_top_right[0] - i * (circle_radius * 2 + circle_spacing), circle_top_right[1])
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