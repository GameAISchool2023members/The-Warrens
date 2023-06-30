import random
import numpy as np

from actions import Actions
from player import Player
from battle import BattleLogic
from face_prediction import VideoCamera

from configs import configs

random.seed(configs.seed)
np.random.seed(configs.seed)

number_actions = len(configs.expressions)

player1 = Player(id=1, hitpoints=5)
player2 = Player(id=2, hitpoints=5)

battle = BattleLogic(player1, player2)
camera_feed = VideoCamera()

winner = None
# JSUT A PLACEHOLDER FOR PYGAME LOOP:
while True:
    print()
    print('##############################################')
    cropped_faces, predicted_emotions = camera_feed.get_frame()
    print(f"Predicted emotions: {predicted_emotions}")
    exit(2)
    expected_action_player_1 = np.random.choice(number_actions)  # club expressions (if you want to remove 'disgust' etc.)
    expected_action_player_2 = np.random.choice(number_actions)
    print(f"Player 1 expected action: {expected_action_player_1}")
    print(f"Player 2 expected action: {expected_action_player_2}")


    # fetch expressions as integers
    # expression_player_1 = random.randint(0, number_actions)
    # expression_player_2 = random.randint(0, number_actions)
    expression_player_1 = expected_action_player_1
    expression_player_2 = expected_action_player_2

    player1.add_action(expression_player_1)
    player2.add_action(expression_player_2)

    print(f"Player 1 actions: {player1.get_action()}")
    print(f"Player 2 actions: {player2.get_action()}")

    print(f"Player 1 window: {player1.actions.actions}")
    print(f"Player 2 window: {player2.actions.actions}")

    # if player1's list of expressions > 10 and player2's list of expressions > 10 then run step
    if player1.is_actions_buffer_full() and player2.is_actions_buffer_full():
        # player.get_action() returns the most used action in the actions window
        winner = battle.step(expected_action_player_1, expected_action_player_2, player1.get_action(), player2.get_action())

    print(f"Player 1: {player1.get_health_points()} health points")
    print(f"Player 2: {player2.get_health_points()} health points")
    
    if winner is not None:
        if winner == 0:
            print("Draw!")
        else:
            print(f"Player {winner} wins!")
        break
    print("")
