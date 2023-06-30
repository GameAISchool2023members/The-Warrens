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
from configs import configs
from player import Player
from typing import List, Optional
from typing import Tuple

class BattleLogic:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        # None: game's not finished yet, 0: draw, 1: player 1, 2: player 2.
        self.winner: Optional[int] = None
        self.number_actions: int = len(configs.expressions)

        self.list_face_expression1 = []
        self.list_face_expression2 = []

        self.exp_act_cntr = 0

        self.required_actions_1 = self.change_required_action(self.number_actions)
        self.required_actions_2 = self.change_required_action(self.number_actions)


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

    def avg_face_expression(self, list_face_expression: List[str]):
        # outputs mode for the one player having its list given as input
        mode = statistics.mode(list_face_expression)
        return mode

    def change_required_action(self, number_actions):
        # this should go in game_logic, should include a counter for the number of times
        # the same required action is repeated
        # number_actions should be a class attribute
        return np.random.choice(number_actions)


    def init_required_action(self):
        self.required_actions_1 = self.change_required_action(self.number_actions)
        self.required_actions_2 = self.change_required_action(self.number_actions)
        self.exp_act_cntr = 0


    # TODO: (ANTONIO)
    def get_required_action(self) -> Tuple[int, int]:
        if self.exp_act_cntr == 0:
            self.required_actions_1 = self.change_required_action(self.number_actions)
            self.required_actions_2 = self.change_required_action(self.number_actions)

        print(f"Player 1: {self.required_actions_1}")
        print(f"Player 2: {self.required_actions_2}")
        return self.required_actions_1, self.required_actions_2

    def check_actions_and_update_hp(self, action_player_1: int, action_player_2: int,
                                    required_action_player_1: int, required_action_player_2: int) -> None:
        #TODO: Link these to GUI and to the actual expressions coming from the NN model (camera)
        if action_player_1 == required_action_player_1: # change this to mode of player 1's actions
            self.player2.health_points -= 1
            self.init_required_action()
        if action_player_2 == required_action_player_2: # change this to mode of player 2's actions
            self.player1.health_points -= 1
            self.init_required_action()

    def check_vitals(self) -> Optional[int]:
        if self.player1.health_points <= 0 and self.player2.health_points <= 0:
            return 0  # 0 means draw, 1 means player 1, 2 means player 2.
        # check empty health points:
        elif self.player1.health_points <= 0:
            self.winner = self.player2.id
            print("Player 2 shot Player 1")
            return self.player2.id
        elif self.player2.health_points <= 0:
            self.winner = self.player1.id
            print("Player 1 shot Player 2")
            return self.player1.id
        else:
            return self.winner  # will be None
        

    # TODO: (ANTONIO) I think that battle only has to know about actions. Expr->action should go in another file
    def step(self, required_action_player_1, required_action_player_2, action_player_1: int, action_player_2: int):

        # If number of frames that player 1 had required action, player 1 shoots player 2
        # Elif number of frames that player 2 had required action, player 2 shoots player 1

        #TODO: Link these to GUI and to the actual expressions coming from the NN model (camera)
        
        if action_player_1 != -1 or action_player_2 != -1:
            if action_player_1 == required_action_player_1: # change this to mode of player 1's actions
                print("Player 1 shot Player 2")
                self.player2.health_points -= 1
            if action_player_2 == required_action_player_2: # change this to mode of player 2's actions
                print("Player 2 shot Player 1")
                self.player1.health_points -= 1
                
        # implement 
        # check if cooldown is over
        # check the attack of each player

        if self.player1.health_points <= 0 and self.player2.health_points <= 0:
            return 0  # 0 means draw, 1 means player 1, 2 means player 2.
        # check empty health points:
        # TODO: after health lost, reset required expressions
        if self.player1.health_points <= 0:
            self.winner = self.player2.id
            return self.player2.id
        if self.player2.health_points <= 0:
            self.winner = self.player1.id
            return self.player1.id
        else: # Nobody won. Continue playing.
            return None

    def clock(self):
        self.exp_act_cntr += 1
        self.exp_act_cntr = self.exp_act_cntr % configs.expression_window + 1

        self.player1.clock()
        self.player2.clock()