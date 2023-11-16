import pygame
from pygame.locals import *

TILE_SIZE = 16
WINDOW_SIZE = (960 + (1 * 960), 392 + (1 * 392))
SCALED_WINDOW = (960, 392)
WIDTH = SCALED_WINDOW[0]
HEIGHT = SCALED_WINDOW[1]

screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(SCALED_WINDOW)


def empty_map():
    return [[0 for i in range(40)] for j in range(23)]


def pretty_print_map(map):
    for row in map:
        print(row)


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
                # namaste beta
                # how is your 7 eleven beta
                mx, my = pygame.mouse.get_pos()
                mx //= 2
                my //= 2
                print("s")

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

    while run:
        display.fill((100, 150, 180))
        map_area.fill((8, 9, 20))

        game_map.draw(map_area)
        game_map.draw_options(0, 360, display)
        game_map.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        display.blit(map_area, (0, 0))
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
