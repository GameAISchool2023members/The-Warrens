import numpy as np

# class Ability:
#     def __init__(self, name, damage, mana_cost):
#         self.name = name
#         self.damage = damage
#         self.mana_cost = mana_cost

#     def __str__(self):
#         return f"{self.name} with {self.damage} damage and {self.mana_cost} mana cost"

#     def __repr__(self):
#         return f"{self.name} with {self.damage} damage and {self.mana_cost} mana cost"



# class Ability:
#     def __init__(self, name, damage):
#         self.name = name
#         self.damage = damage
#         self.cooldown = 0

#     def __str__(self):
#         return f"{self.name} with {self.damage} damage and {self.cooldown} cooldown"

#     def __repr__(self):
#         return f"{self.name} with {self.damage} damage and {self.cooldown} cooldown"
    

class Abilities:
    def __init__(self):
        self.names = ['attack', 'heal', 'shield', 'fireball', 'lightning']
        self.types = ['damage', 'heal', 'shield', 'damage', 'damage']
        self.damages = [1, 2, 0, 5, 10]
        self.max_mana_pools = np.array([50, 50, 50, 50, 50])
        self.mana_costs = np.array([3, 10, 50, 25, 50])
        self.regen_speeds = np.array([2, 2, 2, 3, 2])
        self.current_mana_pools = np.array([50, 50, 50, 50, 50])

    def get_name(self, index):
        return self.names[index]
    
    def get_type(self, index):
        return self.types[index]
    
    def get_damage(self, index):
        return self.damages[index]
    
    def decrease_cooldowns(self):
        # decrease the cooldown of all abilities
        self.current_mana_pools += self.regen_speeds
    
    def is_ability_ready(self, index):
        return self.current_mana_pools[index] >= self.mana_costs[index]

    def select_ability(self, index):
        if self.current_mana_pools[index] >= self.mana_costs[index]:
            self.current_mana_pools[index] -= self.mana_costs[index]
            # # increase the cooldown of all other abilities
            # for i in range(len(self.current_mana_pools)):
            #     if i != index:
            #         self.current_mana_pools[i] += self.regen_speeds[i]
            return self.damages[index]
        else:
            return 0
        
    def get_current_mana_pools(self):
        return self.current_mana_pools
    
    def get_max_mana_pools(self):
        return self.max_mana_pools

    def __str__(self):
        return f"{self.name} with {self.damage} damage and {self.mana_cost} mana cost"

    def __repr__(self):
        return f"{self.name} with {self.damage} damage and {self.mana_cost} mana cost"