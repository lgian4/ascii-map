from typing import List
from terrain import TerrainType, TerrainData, Terrain
from random import randint
import sys
sys.setrecursionlimit(1500)


class FullMap():
    def __init__(self, width, height, map_data: List[List[str]], terrains: TerrainData):
        self.width = width
        self.height = height
        self.map_data = map_data
        self.terrains = terrains

    def set_full_map(self, map_data):
        self.map_data = map_data

    def get_map_value(self, r: int, c: int):
        return self.map_data[r][c]

    def set_map_value(self, r: int, c: int, terrain: Terrain):
        self.map_data[r][c] = terrain.key

    def has_row(self, r: int):
        return r >= 0 and r <= self.height

    def has_column(self, c: int):
        return c >= 0 and c <= self.width

    def is_surround_by_any(self, terrain: Terrain,  r: int, c: int):
        ops = [(-1, 0), (-1, 1), (0, 1), (1, 1),
               (1, 0), (1, -1,), (0, -1), (-1, -1)]
        for op in ops:
            if self.get_map_value(r + op[0], c + op[1]) == terrain.key:
                return True
        return False

    def count_connected_terrain_size(self, terrain: Terrain, visited, r=0, c=0):
        stack = [(r, c)]
        count = 0

        while stack:
            r, c = stack.pop()
            if not self.has_row(r) or not self.has_column(c) or visited[r][c]:
                continue

            visited[r][c] = True
            if self.get_map_value(r, c) == terrain.key:
                count += 1
                stack.extend([(r, c+1), (r, c-1), (r+1, c), (r-1, c)])

        return count

    def replace_connected_same_terrain(self, terrain: Terrain,  r, c, oldTerrain: Terrain):
        if (oldTerrain == None):
            oldTerrain = self.get_map_value(r, c)
        if (not self.has_row(r) or not self.has_column(c)):
            return 0
        if (self.get_map_value(r, c) == terrain.key):
            return
        self.set_map_value(r, c, terrain)
        self.replace_connected_same_terrain(terrain, r, c+1, oldTerrain)
        self.replace_connected_same_terrain(terrain, r, c-1, oldTerrain)
        self.replace_connected_same_terrain(terrain, r+1, c, oldTerrain)
        self.replace_connected_same_terrain(terrain, r-1, c, oldTerrain)


class FullMapBuilder():
    def __init__(self, terrain_data: TerrainData):
        self.height = 100
        self.width = 100
        self.min_island_size = 16
        self.terrain_data = terrain_data

    def set_size(self, height: int, width: int):
        self.height = height
        self.width = width

    def set_min_island_size(self, size: int):
        self.min_island_size = size

    def build(self, ):
        self.map = FullMap(self.width, self.height, None, self.terrain_data)
        self.generate_empty_map().generate_sea(
        ).sink_small_island().add_sand_to_all_sea().add_mountain()
        return self.map

    def generate_empty_map(self):
        self.map.set_full_map([[self.terrain_data.grass.key
                                for _ in range(self.width)] for _ in range(self.height)])
        return self

    def generate_sea(self):
        for r in range(self.height):
            for c in range(self.width):
                r_is_edge = r == 0 or r == self.height - 1
                c_is_edge = c == 0 or c == self.width - 1

                if r_is_edge or c_is_edge:
                    self.map.set_map_value(r, c, self.terrain_data.sea)
                elif self.map.is_surround_by_any(self.terrain_data.sea,  r, c) and randint(0, 100) > 60:
                    self.map.set_map_value(r, c, self.terrain_data.sea)
        return self

    def sink_small_island(self):

        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]
        for r in range(self.height):
            for c in range(self.width):
                if (visited[r][c]):
                    continue
                size = self.map.count_connected_terrain_size(
                    self.terrain_data.grass, visited, r, c)
                if size > 0 and size < self.min_island_size:
                    self.map.replace_connected_same_terrain(
                        self.terrain_data.sea, r, c, self.terrain_data.grass)
        return self

    def add_sand_to_all_sea(self):
        for r in range(self.height):
            for c in range(self.width):
                self.add_sand_near_sea(r, c)
        return self

    def add_sand_near_sea(self, r=0, c=0):
        if (not self.map.has_row(r) or not self.map.has_column(c)):
            return
        if (self.map.get_map_value(r, c) == self.terrain_data.sea.key):
            return
        if (self.map.is_surround_by_any(self.terrain_data.sea,  r, c)):
            self.map.set_map_value(r, c, self.terrain_data.sand)
        elif (self.map.is_surround_by_any(self.terrain_data.sand,  r, c) and randint(0, 100) > 95):
            self.map.set_map_value(r, c, self.terrain_data.sand)

    def add_mountain(self):
        for r in range(self.height):
            for c in range(self.width):
                self.add_mountain_in_grass(r, c)
        return self

    def add_mountain_in_grass(self, r=0, c=0):
        if (not self.map.has_row(r) or not self.map.has_column(c)):
            return 0
        if (self.map.get_map_value(r, c) != self.terrain_data.grass.key):
            return
        surround_by_grass = self.map.is_surround_by_any(
            self.terrain_data.grass,  r, c)
        surround_by_sand = self.map.is_surround_by_any(
            self.terrain_data.sand,  r, c)
        surround_by_mountain = self.map.is_surround_by_any(
            self.terrain_data.mountain,  r, c)
        if (surround_by_grass and not surround_by_sand):
            if (surround_by_mountain and randint(0, 100) > 95):
                self.map.set_map_value(r, c, self.terrain_data.mountain)
            elif (randint(0, 100) > 90):
                self.map.set_map_value(r, c, self.terrain_data.mountain)
