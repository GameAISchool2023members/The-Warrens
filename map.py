import numpy as np

from configs import configs
from utils import in_nested_list

import pygame

pygame.init()
# change pygame window size

""" given a numpy array, draw the map on the screen.
0s are white, 1s are black. 1s are walls and cannot be passed through. 0s are open space and can be passed through."""


class MapGenerator:
    def __init__(self,
                 map_size = configs.map_size,
                 n_rooms = configs.n_rooms,
                 room_size = configs.room_size):
        self.map_size = map_size
        self.n_rooms = n_rooms
        self.room_size = room_size
    
    
    def generate_level(self):
        level = np.ones(shape=self.map_size, dtype=np.uint8) * configs.empty_tile
        # generate rooms centers and sizes
        rooms_center = np.uint8(np.random.rand(self.n_rooms, 2) * np.asarray(self.map_size))
        rooms_dimensions = np.uint8(np.random.rand(self.n_rooms, 2) * np.asarray(self.room_size[1])) + (np.asarray(self.room_size[1]) - np.asarray(self.room_size[0]))
        # add rooms to level
        rooms = [(i, min(i + di, self.map_size[0]), j, min(j + dj, self.map_size[1])) for (i, j), (di, dj) in zip(rooms_center, rooms_dimensions)]
        for (i, k, j, m) in rooms:
            level[i:k, j:m] = configs.ground_tile
        # get actual rooms
        all_rooms = []
        for i in range(len(rooms)):
            room1 = rooms[i]
            if not in_nested_list(room1, all_rooms):
                current_room = [room1]
                for j in range(i + 1, len(rooms)):
                    room2 = rooms[j]
                    m1x, M1x, m1y, M1y = room1
                    m2x, M2x, m2y, M2y = room2
                    if (m1x <= m2x <= M1x or m2x <= m1x <= M2x) and (m1y <= m2y <= M1y or m2y <= m1y <= M2y):
                        current_room.append(room2)
                all_rooms.append(current_room)
        # draw corridors
        for i in range(len(all_rooms)):
            for j in range(i + 1, len(all_rooms)):
                if np.random.rand() <= configs.connection_prob:
                    room_start = all_rooms[i][np.random.choice(range(len(all_rooms[i])))]
                    room_end = all_rooms[j][np.random.choice(range(len(all_rooms[j])))]
                    start_point = (room_start[0] + np.uint8(np.random.rand() * (room_start[1] - room_start[0])),
                                   room_start[2] + np.uint8(np.random.rand() * (room_start[3] - room_start[2])))
                    end_point = (room_end[0] + np.uint8(np.random.rand() * (room_end[1] - room_end[0])),
                                 room_end[2] + np.uint8(np.random.rand() * (room_end[3] - room_end[2])))
                    # ensure we're not on edge of map
                    start_point = (min(start_point[0], self.map_size[0] - 1),
                                   min(start_point[1], self.map_size[1] - 1))
                    end_point = (min(end_point[0], self.map_size[0] - 1),
                                 min(end_point[1], self.map_size[1] - 1))
                    # add the corridors to the level
                    a, b = (start_point, end_point) if start_point[0] <= end_point[0] else (end_point, start_point)
                    level[a[0]:b[0] + 1, a[1]] = configs.ground_tile
                    level[b[0], min(a[1], b[1]):max(a[1], b[1])] = configs.ground_tile
        # clear edges around the level
        level[0, :] = configs.empty_tile
        level[-1, :] = configs.empty_tile
        level[:, 0] = configs.empty_tile
        level[:, -1] = configs.empty_tile
        # add walls around the rooms
        ground_tiles = np.nonzero(level == configs.ground_tile)
        directions = [[1, 0, 0, -1], [0, 1, -1, 0]]
        for (i, j) in zip(*ground_tiles):
            for di, dj in zip(*directions):
                if level[i + di, j + dj] == configs.empty_tile:
                    level[i + di, j + dj] = configs.wall_tile
        # add random walls in rooms
        for i in range(len(all_rooms)):
            if np.random.rand() <= configs.wall_prob:
                room_start = all_rooms[i][np.random.choice(range(len(all_rooms[i])))]
                start_point = (room_start[0] + np.uint8(np.random.rand() * (room_start[1] - room_start[0])),
                               room_start[2] + np.uint8(np.random.rand() * (room_start[3] - room_start[2])))
                lengths = (np.uint8(np.random.rand() * self.room_size[0][0]),
                           np.uint8(np.random.rand() * self.room_size[1][0]))
                level[start_point[0]:min(start_point[0] + lengths[0], self.map_size[0] - 1), start_point[1]] = configs.wall_tile
                level[min(start_point[0] + lengths[0], self.map_size[0] - 1), start_point[1]:min(start_point[1] + lengths[1], self.map_size[1] - 1)] = configs.wall_tile
        
        return level

class Map:
    def __init__(self, map_arr, tile_size: int = 8) -> None:
        self.map_arr = map_arr
        self.tile_size: int = tile_size
        self.screen = pygame.display.set_mode((len(map_arr[0])*tile_size, len(map_arr)*tile_size), 0, 32)
        print(self.screen.get_size())

    def draw_map(self):
        # draw the map taking into account the tile size
        for i in range(len(self.map_arr)):
            for j in range(len(self.map_arr[0])):
                if self.map_arr[i][j] == configs.empty_tile:
                    pygame.draw.rect(self.screen, (0, 0, 0), (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_arr[i][j] == configs.ground_tile:
                    pygame.draw.rect(self.screen, (0, 128, 0), (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))
                elif self.map_arr[i][j] == configs.wall_tile:
                    pygame.draw.rect(self.screen, (128, 128, 128), (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.screen, (255, 0, 0), (j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size))

    def render(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.draw_map()
            pygame.display.flip()

if __name__ == "__main__":
    map_array = MapGenerator().generate_level()
    
    map = Map(map_array)
    map.render()
