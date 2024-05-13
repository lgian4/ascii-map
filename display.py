
import curses
from full_map.full_map import FullMap
from terrain import Terrain


class Display():
    def __init__(self, map: FullMap):
        self.map = map
        self.colors = {}

    def set_color_pair(self):
        self.colors[self.map.terrains.sand.key] = 1
        self.colors[self.map.terrains.sea.key] = 2
        self.colors[self.map.terrains.grass.key] = 3
        self.colors[self.map.terrains.mountain.key] = 4

        i = 1
        for terrain in self.map.terrains:
            curses.init_pair(i, self.get_curses_color(
                terrain.color), curses.COLOR_BLACK)
            self.colors[terrain.key] = i
            i += 1

    def get_curses_color(self, color: str) -> int:
        if (color == "blue"):
            return curses.COLOR_BLUE
        elif (color == "yellow"):
            return curses.COLOR_YELLOW
        elif (color == "green"):
            return curses.COLOR_GREEN
        elif (color == "brown"):
            return curses.COLOR_MAGENTA
        elif (color == "red"):
            return curses.COLOR_RED

    def get_color_pair(self, terrain: Terrain):
        if terrain.key in self.colors:
            return self.colors[terrain.key]
        return 0

    def run(self):
        self.scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.can_change_color()
        self.scr.keypad(True)
        curses.start_color()
        self.set_color_pair()

        player_y = self.map.height // 2
        player_x = self.map.width // 2

        i = 0
        self.scr.clear()
        for y, row in enumerate(self.map.map_data):
            for x, terrain_key in enumerate(row):
                self.scr.addstr(
                    y, x, self.map.terrains.prop_dict[terrain_key].symbol, curses.color_pair(self.get_color_pair(self.map.terrains.prop_dict[terrain_key])))

        while True:
            current_player_y = player_y
            current_player_x = player_x
            current_terrain_key = self.map.get_map_value(player_y, player_x)
            current_terrain = self.map.terrains.prop_dict[current_terrain_key]

            self.scr.addstr(self.map.height, self.map.width // 2,
                            str(current_terrain.elevation), curses.color_pair(1))
            self.scr.addstr(self.map.height, 0,
                            str(i), curses.color_pair(1))
            i += 1

            self.scr.addstr(current_player_y, current_player_x, 'X', curses.A_BOLD |
                            curses.A_BLINK | curses.color_pair(2))

            self.scr.refresh()

            key = self.scr.getch()
            self.scr.addstr(
                player_y, player_x, current_terrain.symbol, curses.color_pair(self.get_color_pair(current_terrain)))

            if key == curses.KEY_UP and player_y > 0:
                player_y -= 1
            elif key == curses.KEY_DOWN and player_y < self.map.height - 1:
                player_y += 1
            elif key == curses.KEY_LEFT and player_x > 0:
                player_x -= 1
            elif key == curses.KEY_RIGHT and player_x < self.map.width - 1:
                player_x += 1
            elif key == ord('q'):
                break

            current_terrain_key = self.map.get_map_value(player_y, player_x)
            current_terrain = self.map.terrains.prop_dict[current_terrain_key]
            if (current_terrain.elevation < 1 or current_terrain.elevation > 2):
                player_y = current_player_y
                player_x = current_player_x

        curses.endwin()
