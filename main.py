import random
import numpy as np

from actions import Actions
from player import Player
from battle import BattleLogic
from face_prediction import VideoCamera

from configs import configs

def change_expected_action(num_actions):
    # this should go in game_logic, should include a counter for the number of times
    # the same expected action is repeated
    # num_actions should be a class attribute
    return np.random.choice(num_actions)





random.seed(configs.seed)
np.random.seed(configs.seed)

number_actions = len(configs.expressions)

player1 = Player(id=1, hitpoints=5)
player2 = Player(id=2, hitpoints=5)

battle = BattleLogic(player1, player2)
camera_feed = VideoCamera()

winner = None

exp_act_cntr = 0

# JSUT A PLACEHOLDER FOR PYGAME LOOP:
while True:
    print()
    print('##############################################')
    cropped_faces, predicted_emotions = camera_feed.get_frame()
    print(predicted_emotions)
    print(f"Predicted emotions: {predicted_emotions}")
    # club expressions (if you want to remove 'disgust' etc.)

    if exp_act_cntr == 0:
        expected_action_player_1 = change_expected_action(number_actions)
    
    if exp_act_cntr == 0:
        expected_action_player_2 = change_expected_action(number_actions)

    exp_act_cntr += 1
    exp_act_cntr = exp_act_cntr % configs.expression_window
    # print(f"Player 1 expected action: {expected_action_player_1}")
    # print(f"Player 2 expected action: {expected_action_player_2}")


    # fetch expressions as integers
    # expression_player_1 = random.randint(0, number_actions)
    # expression_player_2 = random.randint(0, number_actions)
    expression_player_1 = predicted_emotions[0] # expected_action_player_1
    expression_player_2 = predicted_emotions[1] # expected_action_player_2

    player1.add_action(expression_player_1)
    player2.add_action(expression_player_2)

    # print(f"Player 1 actions: {player1.get_action()}")
    # print(f"Player 2 actions: {player2.get_action()}")

    # print(f"Player 1 window: {player1.actions.actions}")
    # print(f"Player 2 window: {player2.actions.actions}")

    # if player1's list of expressions > 10 and player2's list of expressions > 10 then run step
    if player1.is_actions_buffer_full() and player2.is_actions_buffer_full():
        # player.get_action() returns the most used action in the actions window
        winner = battle.step(expected_action_player_1, expected_action_player_2, player1.get_action(), player2.get_action())

    # print(f"Player 1: {player1.get_health_points()} health points")
    # print(f"Player 2: {player2.get_health_points()} health points")
    
    if winner is not None:
        if winner == 0:
            print("Draw!")
        else:
            print(f"Player {winner} wins!")
        break
    print("")
