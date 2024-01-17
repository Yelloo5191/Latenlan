import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import filedialog

TILE_SIZE = 16
WINDOW_SIZE = (960 + (1 * 960), 392 + (1 * 392))
SCALED_WINDOW = (960, 392)
WIDTH = SCALED_WINDOW[0]
HEIGHT = SCALED_WINDOW[1]

root = tk.Tk()
root.withdraw()

screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(SCALED_WINDOW)

pygame.init()

font = pygame.font.Font(None, 16)


def load_map(path, world):
    f = open(path, 'r')
    data = eval(f.read())
    f.close()
    world.data = data
    world.update_tiles()


def import_map(world):
    # open file dialog
    # load map
    # return map
    path = filedialog.askopenfilename()

    if path == "":
        return

    return load_map(path, world)


def export_map(world):
    # open file dialog
    # save map
    data = world.data
    path = filedialog.asksaveasfilename()

    if path == "":
        return
    if not path.endswith(".txt"):
        path += ".txt"

    with open(path, 'w') as f:
        f.write(str(data))


def empty_map():
    return [[0 for i in range(40)] for j in range(23)]


def pretty_print_map(map):
    for row in map:
        print(row)


class Button:
    def __init__(self, x, y, width, height, text, color, onClick, *args):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.onClick = onClick
        self.args = args

    def draw(self):
        pygame.draw.rect(display, self.color, self.rect, 0, 3)
        text = font.render(self.text, True, (255, 255, 255))
        display.blit(text, (self.rect.x + 5, self.rect.y + 5))

    def update(self):
        self.draw()
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            mx //= 2
            my //= 2
            if self.rect.collidepoint(mx, my):
                self.onClick(*self.args)


class Tile:
    def __init__(self, x, y, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.tile = (self.image, self.rect)

    def draw(self, display):
        display.blit(self.image, self.rect)


class World:
    def __init__(self, data):
        self.tiles = {
            "stalagmite": 1,
            "path": 2,
            "stone": 3,
            "stonetodark": 4,
            "dark": 5
        }
        self.data = data

        self.selected_tile = 1

        self.update_tiles()

    def draw(self, display):
        for tile in self.tile_list:
            tile.draw(display)
            # pygame.draw.rect(display, (0, 0, 255), tile.rect, 1)

    def update_tiles(self):
        self.tile_list = []
        y = 0
        for row in self.data:
            x = 0
            for tile in row:
                if tile == 1:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/stalagmite.png"))
                elif tile == 2:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/path.png"))
                elif tile == 3:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/stone.png"))
                elif tile == 4:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/stonetodark.png"))
                elif tile == 5:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/dark.png"))
                x += 1
            y += 1

    def draw_options(self, x, y, display):
        self.option_rects = {}
        for tile, index in self.tiles.items():
            display.blit(pygame.transform.scale(pygame.image.load(
                f"assets/world/{tile}.png"), (32, 32)), (x, y))
            collision_rect = pygame.Rect(x, y, 32, 32)
            self.option_rects[index] = collision_rect

            if self.selected_tile == index:
                pygame.draw.rect(display, (255, 0, 0), collision_rect, 1)
            x += 32

    def update(self):

        if pygame.mouse.get_pressed()[0]:
            # check if mouse is in map area and not in options area
            mx, my = pygame.mouse.get_pos()
            mx //= 2
            my //= 2

            if mx < 640 and my < 360:
                tile_x = mx // TILE_SIZE
                tile_y = my // TILE_SIZE
                self.data[tile_y][tile_x] = self.selected_tile
                self.update_tiles()
            else:
                # mouse is in options area, check which tile is selected
                mx, my = pygame.mouse.get_pos()
                mx //= 2
                my //= 2

                for i in self.option_rects:
                    if self.option_rects[i].collidepoint(mx, my):
                        self.selected_tile = i
        elif pygame.mouse.get_pressed()[2]:

            mx, my = pygame.mouse.get_pos()
            mx //= 2
            my //= 2

            if mx < 640 and my < 360:
                tile_x = mx // TILE_SIZE
                tile_y = my // TILE_SIZE
                self.data[tile_y][tile_x] = 0
                self.update_tiles()

    def get_tile(self, x, y):
        return self.data[y][x]


def main():
    run = True

    game_map = World(empty_map())
    map_area = pygame.Surface((640, 360))

    import_but = Button(650, 10, 100, 32, "Import", (50, 180, 100),
                        import_map, game_map)
    export_but = Button(650, 52, 100, 32, "Export", (180, 50, 100),
                        export_map, game_map)

    while run:
        display.fill((53, 49, 64))
        map_area.fill((255, 255, 255))

        game_map.draw(map_area)
        game_map.draw_options(0, 360, display)
        game_map.update()

        import_but.update()
        export_but.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        display.blit(map_area, (0, 0))
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
