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

    player1.add_action(expression_player_1)
    player2.add_action(expression_player_2)

    print(f"Player 1 actions: {player1.get_action()}")
    print(f"Player 2 actions: {player2.get_action()}")

    # if player1's list of expressions > 10 and player2's list of expressions > 10 then run step
    if player1.is_actions_buffer_full() and player2.is_actions_buffer_full():
        # player.get_action() returns the most used action in the actions window
        winner = battle.step(player1.get_action(), player2.get_action())
    if winner is not None:
        print(f"Player {winner} wins!")
        break

    print(f"Player 1: {player1.get_health_points()} health points")
    print(f"Player 2: {player2.get_health_points()} health points")

    print("")
