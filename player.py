from actions import Actions
from abilities import Abilities

class Player:
    def __init__(self, id, hitpoints: int = 5):
        self.id = id
        self.health_points = hitpoints
        self.shield = False
        self.shield_cool_down = 0

        self.actions = Actions(actions_window=5)
        self.abilities = Abilities()


    def get_health_points(self):
        return self.health_points
    
    def add_action(self, action):
        self.actions.add_action(action)

    def get_action(self):
        return self.actions.get_most_used_action()
    
    def is_actions_buffer_full(self):
        return self.actions.is_buffer_full()
    
    def activate_shield(self):
        self.shield = True
        self.shield_cool_down = 30

    def decrease_shield_remaining_time(self):
        self.shield_cool_down -= 1
        if self.shield_cool_down == 0:
            self.shield = False


    def clock(self):
        self.decrease_shield_remaining_time()
        self.abilities.regen_mana()
        

    def __str__(self):
        return f"Player {self.id} with {self.health_points} health points"
