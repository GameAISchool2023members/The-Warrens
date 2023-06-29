# Face2Face

An AI Summer School 2023 game jam project.

## Game overview
...


## Team members:
 - Andrea Alfonso
 - Antonio Pio Ricciardi
 - Najada Kambo
 - Roberto Gallotta
 - Rupali Bhati
 - Sarra Graja
 - Wafa Aissa


# Files
    - player: `player.py` should contain a class `Player` with the following methods:
        - `__init__(self, name, hp, attack, speed, range)`
        - `attack(self, enemy)` produces an attack
        - `move(self, direction)` moves the player in the given direction
        - `get_position(self)` returns the position of the player
        - `get_stats(self)` returns the stats of the player
        - `get_name(self)` returns the name of the player
        - `get_hp(self)` returns the hp of the player
        - `get_attack(self)` returns the attack of the player
        - `get_defense(self)` returns the defense of the player
        - `get_speed(self)` returns the speed of the player
        - `get_range(self)` returns the view range of the player
        - `set_position(self, position)` sets the position of the player (used right after map creation)
        - `set_stats(self, hp, attack, defense, speed, range)` sets the stats of the player
        - `set_name(self, name)` sets the name of the player
        - `set_hp(self, hp)` sets the hp of the player
        - `decrease_hp(self, damage)` decreases the hp of the player by the given amount
        - `set_attack(self, attack)` 
        - `set_defense(self, defense)`
        - `set_speed(self, speed)`
        - `set_range(self, range)`

    - map: `map.py` should contain a class `Map` with following methods:
        - `__init__(self, size, player, enemies)` creates a map of the given size, with two players and random enemies
        - `get_size(self)` returns the size of the map
        - `get_player(self)` returns the player
        - `get_enemies(self)` returns the enemies
        - `get_tile(self, position)` returns the tile at the given position
        - `set_size(self, size)` sets the size of the map
        - `set_player(self, player)` sets the player
        - `set_enemies(self, enemies)` sets the enemies
        - `set_tile(self, position, tile)` sets the tile at the given position
        - `move_player(self, direction)` moves the player in the given direction
        - `move_enemy(self, enemy, direction)` moves the given enemy in the given direction
        - `get_tile(self, position)
    - game (core) (TBF)
    - enemy (TBD)