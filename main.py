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
WINDOW_SIZE = (800, 800)
SCALED_WINDOW = (480, 480)
WIDTH = SCALED_WINDOW[0]
HEIGHT = SCALED_WINDOW[1]
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

    def draw(self):
        for tile in self.tile_list:
            tile.draw()
            # pygame.draw.rect(display, (0, 0, 255), tile.rect, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image, world):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(image)
        self.original_image = pygame.transform.scale(self.original_image, (16, 16))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.vel = [0, 0]
        self.y_momentum = 0
        self.world = world
        self.state = "idle"
        self.direction = "right"
        self.moving = False
        self.jumping = False
        self.jump_count = 0
        self.jump_height = 10
        self.gravity = 1
        self.collisions = {"top": False, "bottom": False, "right": False, "left": False}
        self.air_timer = 0

    def draw(self):
        display.blit(self.image, self.rect)
        # pygame.draw.rect(display, (255, 0, 0), self.rect, 1)

    def update(self, dt):
        self.vel = [0, 0]
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction = "right"
            self.moving = True
        if keys[pygame.K_a]:
            self.direction = "left"
            self.moving = True
        if keys[pygame.K_w]:
            if self.jump_count < 2 and self.collisions["bottom"] or self.air_timer < 15:
                self.jumping = True
        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.moving = False

        if self.moving:
            if self.direction == "right":
                self.vel[0] += self.speed[0]
            elif self.direction == "left":
                self.vel[0] -= self.speed[0]
        if self.jumping:
            self.y_momentum = -self.jump_height
            self.jump_count += 1
            self.jumping = False

        self.y_momentum += self.gravity
        if self.y_momentum > 10:
            self.y_momentum = 10
        self.vel[1] += self.y_momentum

        self.movement()
        self.animate()
        self.draw()

    def collide_test(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                hit_list.append(tile)
        return hit_list

    def movement(self):
        self.collisions = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.vel[0]
        hit_list = self.collide_test(self.world.tile_list)
        for tile in hit_list:
            #check if tile is below player
            if tile.rect.y > self.rect.y + self.rect.height:
                if self.vel[0] > 0:
                    self.rect.right = tile.rect.left
                    self.collisions["right"] = True
                elif self.vel[0] < 0:
                    self.rect.left = tile.rect.right
                    self.collisions["left"] = True
        self.rect.y += self.vel[1]
        hit_list = self.collide_test(self.world.tile_list)
        for tile in hit_list:
            if self.vel[1] > 0:
                self.rect.bottom = tile.rect.top + 2
                self.collisions["bottom"] = True
            elif self.vel[1] < 0:
                self.rect.top = tile.rect.bottom
                self.collisions["top"] = True
        
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height
        
        if self.collisions["bottom"]:
            self.jump_count = 0
            self.air_timer = 0
            self.jumping = False
        else:
            self.air_timer += 1
    
    def animate(self):
        if self.direction == "right":
            self.image = self.original_image
        elif self.direction == "left":
            self.image = pygame.transform.flip(self.original_image, True, False)
                
def main():
    run = True

    game_map = load_map("world/map")
    world = World(game_map)
    player = Player(100, 100, [3, 5], "assets/player/player.png", world)

    current_time = pygame.time.get_ticks()
    while run:
        # Delta Time Calculation
        # dt = pygame.time.get_ticks() - current_time
        # current_time = pygame.time.get_ticks()
        dt = 1

        # Render FPS
        fps = int(clock.get_fps())
        pygame.display.set_caption(f"FPS: {fps}")

        # Rendering
        display.fill(colors[4])
        world.draw()
        player.update(dt)

        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


main()