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

class BattleLogic:
    def __init__(self, player1, player2, context_len):
        self.player1 = player1
        self.player2 = player2
        self.winner = None

        self.context_len = context_len
        self.list_face_expression1 = []
        self.list_face_expression2 = []

    # def start(self):

    def _add_expressions(self, expression1, expression2):
        # TODO: check
        self.list_face_expression1.append(expression1)
        self.list_face_expression2.append(expression2)
        if len(self.list_face_expression1) > self.context_len:
            self.list_face_expression1.pop(0)
            self.list_face_expression2.pop(0)
    
    def _count_expressions(self):
        # count the number of occurences of each expression for each player
        pass

    def fetch_face_expression(self):
        pass

    def _expression_to_idx(self, expression: str) -> int:
        pass

    def expression_to_action(self):
        pass

    def step(self):
        # check if cooldown is over
            # check the attack of each player

        # decrease hit points

        # if self.player1.health_points <= 0:
        #     self.winner = self.player2.id
        #     return
        # if self.player2.health_points <= 0:
        #     self.winner = self.player1.id
        #     return

        
        pass


