from actions import Actions

class Player:
    def __init__(self, id, hitpoints: int = 5):
        self.id = id
        self.health_points = hitpoints
        self.actions = Actions(actions_window=5)


    def get_health_points(self):
        return self.health_points
    
    def perform_action(self, action):

    def __str__(self):
        return f"Player {self.id} with {self.health_points} health points"
