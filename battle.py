"""
Battle logic (battle.py)
0. Disable keyboard inputs 
1. Fetch expression (state)  @antonio
2. Link expression to actions (action)  Rupali Bhati Antonio Pio Ricciardi
3. Execute action (step function)  Rupali Bhati
4. Average face expression over last frames (tbd, e.g. 10 frames) Wafa
5. Hit points (reward) (decrease player s health points) - attribute of class Player  Rupali Bhati
6. Cooldown (5 seconds)  Rupali Bhati
7. Check empty health points Wafa
8. If both still alive, go to step 1, else terminate encounter	Rupali Bhati
9. Increase winning player s score Rupali Bhati
10. Terminate battle Wafa
"""

import numpy as np
import statistics
from actions import get_action
from configs import configs

class BattleLogic:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.num_actions = len(configs.expressions)

        self.list_face_expression1 = []
        self.list_face_expression2 = []

    # def _add_expressions(self, expression1, expression2):
    #     # TODO: check
    #     self.list_face_expression1.append(expression1)
    #     self.list_face_expression2.append(expression2)
    #     if len(self.list_face_expression1) > self.context_len:
    #         self.list_face_expression1.pop(0)
    #         self.list_face_expression2.pop(0)
    
    def _count_expressions(self):
        # count the number of occurences of each expression for each player
        pass

    def fetch_face_expression(self):
        pass

    # def _expression_to_idx(self, expression: str) -> int:
    #     pass

    # def expression_to_action(self):
    #     pass

    def avg_face_expression(self, list_face_expression):
        # outputs mode for the one player having its list given as input
        mode = statistics.mode(list_face_expression)
        return mode

    # TODO: (ANTONIO) I think that battle only has to know about actions. Expr->action should go in another file
    def step(self, action_player_1, action_player_2):
        
        expected_action_player_1 = np.random.choice(self.num_actions)  # club expressions (if you want to remove 'disgust' etc.)
        expected_action_player_2 = np.random.choice(self.num_actions)

        # If number of frames that player 1 had expected action, player 1 shoots player 2
        # Elif number of frames that player 2 had expected action, player 2 shoots player 1

        if action_player_1 == expected_action_player_1: # change this to mode of player 1's actions
            self.player2.health_points -= 1
        if action_player_2 == expected_action_player_2: # change this to mode of player 2's actions
            self.player1.health_points -= 1
            
        # implement 
        # check if cooldown is over
        # check the attack of each player


        # check empty health points:
        if self.player1.health_points <= 0:
            self.winner = self.player2.id
            return self.player2.id
        if self.player2.health_points <= 0:
            self.winner = self.player1.id
            return self.player1.id

        

        


