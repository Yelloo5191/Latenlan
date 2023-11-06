from json import load
import pygame
import sys
import time
import math
import random
from pygame.locals import *
from util.entities import GhoulDeath, ProjectileHit

from util.player import Player
from util.enemies import Demon, Ghoul
from util.config import *
from util.ui import HealthBar
from util.util import *

pygame.init()
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.play(-1)


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


def main():
    run = True

    game_map = load_map("world/map")
    world = World(game_map)
    player = Player(100, 100, [3, 5], "assets/player/player.png", world)
    demon = Demon(300, 100, .1, "assets/enemies/demon.png")
    spawn_timer = 0
    ghouls = []
    particles = []
    health_bar = HealthBar(
        10, 10, 100, 10, (255, 0, 0), player.health, player.max_health)

    cursor = pygame.image.load("assets/misc/cursor.png")
    pygame.mouse.set_visible(False)

    current_time = pygame.time.get_ticks()
    while run:

        # Render FPS
        fps = int(clock.get_fps())
        pygame.display.set_caption(f"FPS: {fps}")

        # Rendering
        display.fill(colors[4])
        demon.update()
        world.draw()
        health_bar.update(player.health)
        player.update()

        # Ghoul Handling
        for ghoul in ghouls:
            ghoul.update(player)
            for projectile in ghoul.projectiles:
                if projectile.rect.x < 0 or projectile.rect.x > 480 or projectile.rect.y < 0 or projectile.rect.y > 480:
                    ghoul.projectiles.remove(projectile)
                if projectile.rect.colliderect(player.rect):
                    ghoul.projectiles.remove(projectile)
                    player.hit(projectile.damage)
                projectile.update()

        # Projectile Handling
        for projectile in player.projectiles:
            if projectile.rect.x < 0 or projectile.rect.x > 480 or projectile.rect.y < 0 or projectile.rect.y > 480:
                player.projectiles.remove(projectile)
            projectile.update()
            for ghoul in ghouls:
                if projectile.rect.colliderect(ghoul.rect):
                    player.projectiles.remove(projectile)
                    ghoul.hit(projectile.damage)
                    particles.extend([ProjectileHit(
                        ghoul.rect.centerx + random.randint(-10, 10), ghoul.rect.centery + random.randint(-10, 10))
                        for _ in range(5)])
                    if ghoul.health <= 0:
                        ghouls.remove(ghoul)
                        particles.extend([GhoulDeath(
                            ghoul.rect.x, ghoul.rect.y) for _ in range(20)])
                    break

        # Particle Handling
        for particle in particles:
            if particle.lifetime > 20:
                particles.remove(particle)
            particle.update()

        # Cursor Rendering
        display.blit(cursor, (get_mouse_pos()[
                     0] - 5, get_mouse_pos()[1] - 5))

        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Every 30 seconds, summon ghouls
        spawn_timer += 1
        if spawn_timer == 300:
            demon.summon(ghouls)
            spawn_timer = 0

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


main()
