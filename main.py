from json import load
import pygame
import sys
import time
import math
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
TILE_SIZE = 16
FPS = 60
WINDOW_SIZE = (1200, 1200)
SCALED_WINDOW = (480, 480)
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(SCALED_WINDOW)

colors = [(29, 16, 67), (13, 12, 48), (26, 21, 45), (17, 15, 29), (8, 9, 20)]


def load_map(path):
    f = open(path + '.txt', 'r')
    data = eval(f.read())
    f.close()
    return(data)


class Tile:
    def __init__(self, x, y, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.tile = (self.image, self.rect)

    def draw(self):
        display.blit(self.image, self.rect)


class World:
    def __init__(self, data):
        self.tile_list = []
        self.data = data

        y = 0
        for row in self.data:
            x = 0
            for tile in row:
                if tile == 1:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/stalagmite.png"))
                elif tile == 2:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/stone1.png"))
                elif tile == 3:
                    self.tile_list.append(
                        Tile(x, y, "assets/world/stone2.png"))
                x += 1
            y += 1

    def draw(self):
        for tile in self.tile_list:
            tile.draw()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, image, world):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        self.world = world
        self.jumped = False
        self.colliding_ground = False
        self.player_flip = False

    def draw(self):
        display.blit(self.image, self.rect)

    def update(self, dt):
        self.draw()

        dx, dy = 0, 0

        # self.velocity[1] += 5

        # key = pygame.key.get_pressed()
        # if key[K_w] and self.jumped == False:
        #     self.colliding_ground = False
        #     self.velocity[1] = -50
        #     self.jumped = True
        # if key[K_w] == False and self.colliding_ground == True:
        #     self.jumped = False
        # if key[K_a]:
        #     dx -= 5 * dt
        #     self.player_flip = True
        # if key[K_d]:
        #     dx += 5 * dt
        #     self.player_flip = False
        # else:
        #     pass
        #     # self.player_action = 'idle'

        # if self.velocity[1] > 10:
        #     self.velocity[1] = 10
        # dy += self.velocity[1] * dt

        # for tile in self.world.tile_list:
        #     if tile.tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
        #         dx = 0

        #     if tile.tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
        #         if self.velocity[1] < 0:
        #             self.colliding_ground = True
        #             dy = tile.tile[1].bottom - self.rect.top
        #             self.velocity[1] = 0
        #         elif self.velocity[1] >= 0:
        #             self.colliding_ground = True
        #             dy = tile.tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy


def main():
    last_time = time.time()
    run = True

    game_map = load_map("world/map")
    world = World(game_map)
    player = Player(100, 100, [0, 10], "assets/player/player.png", world)
    while run:
        # Delta Time Calculation
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        # Rendering
        display.fill(colors[4])
        world.draw()
        player.update(dt)

        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(FPS)
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()


main()
