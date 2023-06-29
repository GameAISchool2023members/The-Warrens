import random
from actions import Actions
from player import Player
from battle import BattleLogic
random.seed(10)


player1 = Player(id=1, hitpoints=5)
player2 = Player(id=2, hitpoints=5)

battle = BattleLogic(player1, player2)

# JSUT A PLACEHOLDER FOR PYGAME LOOP:
while True:

    # fetch expressions as integers
    expression_player_1 = random.randint(0, 5)
    expression_player_2 = random.randint(0, 5)

    player1.add_actions(expression_player_1)
    player2.add_actions(expression_player_2)

    battle.step(player1.get_most_used_action(), player2.get_most_used_action())