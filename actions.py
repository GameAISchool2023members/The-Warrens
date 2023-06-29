class Actions:
    """ class for managing the actions """
    def __init__(self, actions_window: int = 1):
        self.actions = []
        self.actions_window = actions_window

    def add_action(self, action):
        self.actions.append(action)
        if len(self.actions) > self.actions_window:
            self.actions.pop(0)

    def get_actions(self):
        return self.actions
    
    def get_most_used_action(self):
        # return the most used action in the last actions_window actions
        return max(set(self.actions), key=self.actions.count)

    def is_buffer_full(self):
        return len(self.actions) == self.actions_window

    def __str__(self):
        return str(self.actions)

    def __repr__(self):
        return str(self.actions)