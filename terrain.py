from typing import Dict, Union
from enum import Enum
from typing import Generator


class Terrain:
    def __init__(self, key,  name, color, symbol, elevation):
        self.key = key
        self.name = name
        self.color = color
        self.symbol = symbol
        self.elevation = elevation


class TerrainType(Enum):
    GRASS = 'grass'
    MOUNTAIN = 'mountain'
    SAND = 'sand'
    SEA = 'sea'
    EMPTY = ''


class TerrainData:
    def __init__(self, sea: Terrain, mountain: Terrain, sand: Terrain, grass: Terrain):
        self.sea = sea
        self.mountain = mountain
        self.sand = sand
        self.grass = grass
        self.prop_dict = {
            sea.key: sea,
            mountain.key: mountain,
            sand.key: sand,
            grass.key: grass,
        }

    def __iter__(self) -> Generator[Terrain, None, None]:
        for attr in ['sea', 'mountain', 'sand', 'grass']:
            yield getattr(self, attr)
