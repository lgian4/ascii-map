import os
from terrain import TerrainData, Terrain, TerrainType
from full_map.full_map import FullMapBuilder
from display import Display


def generate_map(map_data, generators):
    for generator in generators:
        generator.generate(map_data)


def main():

    terrain_data = TerrainData(
        Terrain('se', TerrainType.SEA.value, 'blue', '~', 0),
        Terrain('m', TerrainType.MOUNTAIN.value, 'red', '▲', 3),
        Terrain('sa', TerrainType.SAND.value,  'yellow', ',', 1),
        Terrain('g', TerrainType.GRASS .value, 'green', '-', 2),
    )

    size = os.get_terminal_size()
    width, height = size.columns, size.lines

    map_builder = FullMapBuilder(terrain_data)
    map_builder.set_size(height- 2 , width -2)
    map_builder.set_min_island_size(20)
    map = map_builder.build()
    display = Display(map)
    display.run()


if __name__ == "__main__":
    main()
