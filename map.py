import numpy as np

import pygame

pygame.init()
# change pygame window size

""" given a numpy array, draw the map on the screen.
0s are white, 1s are black. 1s are walls and cannot be passed through. 0s are open space and can be passed through."""



class Map:
    def __init__(self, map_arr, tile_size: int = 32) -> None:
        self.map_arr = map_arr
        self.tile_size: int = tile_size
        self.screen = pygame.display.set_mode((len(map_arr[0])*tile_size, len(map_arr)*tile_size))
        print(self.screen.get_size())

    def draw_map(self):
        # draw the map taking into account the tile size
        for i in range(len(self.map_arr)):
            for j in range(len(self.map_arr[0])):
                if self.map_arr[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))

    def render(self):
        self.draw_map()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    map_array = np.array([
    [1, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    ])

    map = Map(map_array)
    map.render()
