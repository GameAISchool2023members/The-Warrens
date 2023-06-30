import pygame
import numpy as np
import cv2
import os
from face_prediction import VideoCamera
import time

# from utils import add_outline_to_image
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
        # self.update_screen()

        self.p1 = Player(id=1, hitpoints=5)
        self.p2 = Player(id=2, hitpoints=5)
        self.battlelogic = BattleLogic(self.p1, self.p2)

        self.font = pygame.font.Font(None, 30)
        
        # text1 = self.font.render("Emotion_left", True, (255, 255, 255))
        # text2 = self.font.render("Emotion_right", True, (255, 255, 255))

        # text_rect1 = text1.get_rect(center=(self.faces_positions[0][0] + 100, self.faces_positions[0][1] + 20))
        # text_rect2 = text2.get_rect(center=(self.faces_positions[1][0] + 100, self.faces_positions[1][1] + 20))

        # self.screen.blit(text1, text_rect1)
        # self.screen.blit(text2, text_rect2)

    def make_title(self):
        # text at the bottom
        font_size = self.h // 20
        font = pygame.font.Font(None, font_size)
        text_surface = font.render("Two AI researchers arguing in Cambribdge, brought by stable diffusion", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.bottom = self.screen.get_rect().bottom - font_size
        self.screen.blit(text_surface, text_rect)

    def show_winner(self, winner):
        font_size = self.h // 10
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(f'Winner is YOU (Player {winner})!', True, (255, 255, 255)) if winner != 0 else font.render("It's a DRAW!", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx
        text_rect.centery = self.screen.get_rect().centery
        self.screen.blit(text_surface, text_rect)

    def modify_emoji(self, expected_image, face_position):
        image_path = 'assets/emojis/'+str(expected_image)+'.png'  # Replace with the path to your image
        image = pygame.image.load(image_path)
        image_size = (250 // 3, 250 // 3)
        image_position = (face_position[0] + (250 // 2 - image_size[0]), face_position[1] + 20)
        self.screen.blit(pygame.transform.scale(image, image_size), image_position)

    def show_predicted_emotion(self, predicted_emotion, face_position):
        image_path = 'assets/emojis/'+str(predicted_emotion)+'.png'  # Replace with the path to your image
        image = pygame.image.load(image_path)
        image_size = (250 // 6, 250 // 6)
        image_position = (face_position[0] + 100, face_position[1] - (250 + image_size[1] + 10))
        self.screen.blit(pygame.transform.scale(image, image_size), image_position) 

    def loop_stuff(self):
        winner = None
        print()
        print('##############################################')
        cropped_faces, predicted_emotions = self.camera.get_frame()
        print(predicted_emotions)
        print(f"Predicted emotions: {predicted_emotions}")
        # club expressions (if you want to remove 'disgust' etc.)

        expected_action_p1, expected_action_p2 = self.battlelogic.get_required_action()
        # expected_action_p2 = self.battlelogic.get_required_action()
        self.modify_emoji(expected_action_p1,self.faces_positions[0]) #TODO (just example) to call when expected_face changes
        self.modify_emoji(expected_action_p2,self.faces_positions[1]) #TODO (just example) to call when expected_face changes
    
        # TODO: display expected actions on screen
        
        # print(f"Player 1 expected action: {expected_action_player_1}")
        # print(f"Player 2 expected action: {expected_action_player_2}")


        # fetch expressions as integers
        # expression_player_1 = random.randint(0, number_actions)
        # expression_player_2 = random.randint(0, number_actions)
        expression_player_1 = predicted_emotions[0] # expected_action_player_1
        expression_player_2 = predicted_emotions[1] # expected_action_player_2
        
        if expression_player_1 != -1:
            self.show_predicted_emotion(expression_player_1, self.faces_positions[0])
        if expression_player_2 != -1:
            self.show_predicted_emotion(expression_player_2, self.faces_positions[1])
        
        self.p1.add_action(expression_player_1)
        self.p2.add_action(expression_player_2)

        # print(f"Player 1 actions: {player1.get_action()}")
        # print(f"Player 2 actions: {player2.get_action()}")

        # print(f"Player 1 window: {player1.actions.actions}")
        # print(f"Player 2 window: {player2.actions.actions}")

        # if player1's list of expressions > 10 and player2's list of expressions > 10 then run step
        if self.p1.is_actions_buffer_full() and self.p2.is_actions_buffer_full():
            # player.get_action() returns the most used action in the actions window
            winner = self.battlelogic.step(expected_action_p1, expected_action_p2, self.p1.get_action(), self.p2.get_action())

        # print(f"Player 1: {player1.get_health_points()} health points")
        # print(f"Player 2: {player2.get_health_points()} health points")
        
        self.battlelogic.clock()
        print("")

        if (expression_player_1 != -1) or (expression_player_2 != -1):
            self.modify_circles(expected_action_p1, expected_action_p2, expression_player_1, expression_player_2)
        self.update_screen(cropped_faces=cropped_faces, predicted_emotions=predicted_emotions)
        return winner


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
    def modify_circles(self, required_p1, required_p2, prediction_p1, prediction_p2):
        if required_p1 == prediction_p1:
            if (self.total_life - self.p1.health_points) >= 0:
                circle = self.circles_right[self.total_life - self.p2.health_points]
                pygame.draw.circle(self.screen, (255, 255, 255), circle[0], circle[1])
                pygame.draw.circle(self.screen, (255, 0, 0), circle[0], circle[1], 1)
                # self.life_tobe_consumed_left -=1
        elif required_p2 == prediction_p2:
            if (self.total_life - self.p2.health_points)  >= 0:
                circle = self.circles_left[self.total_life - self.p1.health_points]
                pygame.draw.circle(self.screen, (255, 255, 255), circle[0], circle[1])
                pygame.draw.circle(self.screen, (255, 0, 0), circle[0], circle[1], 1)
                # self.life_tobe_consumed_right -=1


    # def modify_circles_bk(self, prediction):
    #     if prediction == 0: # happy (player left lose point, okay i know it's counter intuitive, fix it)
    #         if self.life_tobe_consumed_left >= 0:
    #             circle = self.circles_left[self.life_tobe_consumed_left]
    #             pygame.draw.circle(self.screen, (255, 255, 255), circle[0], circle[1])
    #             pygame.draw.circle(self.screen, (255, 0, 0), circle[0], circle[1], 1)
    #             self.life_tobe_consumed_left -=1
    #     elif prediction == 5: #angry (player right lose point)
    #         if self.life_tobe_consumed_right >= 0:
    #             circle = self.circles_right[self.life_tobe_consumed_right]
    #             pygame.draw.circle(self.screen, (255, 255, 255), circle[0], circle[1])
    #             pygame.draw.circle(self.screen, (255, 0, 0), circle[0], circle[1], 1)
    #             self.life_tobe_consumed_right -=1
    
    def update_screen(self, cropped_faces, predicted_emotions):  
        for face, face_position, predicted_emotion in zip(cropped_faces, self.faces_positions, predicted_emotions):
            fixed_face = pygame.surfarray.make_surface(cv2.cvtColor(face.T, cv2.COLOR_GRAY2RGB)) if isinstance(face, np.ndarray) else face
            self.screen.blit(pygame.transform.scale(fixed_face, (250, 250)), (face_position[0], face_position[1] - 250))
            # Beat the shit out of him
            
        pygame.display.flip()

    def make_countdown(self):
        font_size = self.h // 5
        font = pygame.font.Font(None, font_size)
        for i in range(3, 0, -1):
            self.screen.fill((0, 0, 0))
            self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (0, 0))
            text_surface = font.render(str(i), True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.screen.get_rect().centerx
            text_rect.centery = self.screen.get_rect().centery
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(1)
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.background, (self.w, self.h)), (0, 0))
        self.create_circles()
        pygame.display.flip()
        time.sleep(1)


    def render(self):
        cd_shown = False
        while True: # battle loop
            # sleep for 1 second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if not cd_shown:
                self.make_countdown()
                cd_shown = True
            winner = self.loop_stuff()   # 1 step  # TODO: return battle ending condition
            # self.update_screen()     # TODO: we might need to move this to loop_stuff   NO, this is a render
            pygame.display.flip()
            if winner is not None:
                self.show_winner(winner)
                if winner == 0:
                    print("Draw!")
                else:
                    print(f"Player {winner} wins!")
            
            if self.p1.health_points == 0 or self.p2.health_points == 0:
                pygame.quit()
                exit(0)
            
            # TODO: End game when someone dies
            # TODO: Check why people are dying so fast


if __name__ == "__main__":
    gui = EncounterGUI()

    gui.render()
    # cooldown period