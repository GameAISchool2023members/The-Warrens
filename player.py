from actions import Actions

class Player:
    def __init__(self, id, hitpoints: int = 5):
        self.id = id
        self.health_points = hitpoints
        self.actions = Actions(actions_window=5)


    def get_health_points(self):
        return self.health_points
    
    def add_action(self, action):
        self.actions.add_action(action)

    def get_action(self):
        return self.actions.get_most_used_action()
    
    def is_actions_buffer_full(self):
        return self.actions.is_buffer_full()

    def __str__(self):
        return f"Player {self.id} with {self.health_points} health points"
