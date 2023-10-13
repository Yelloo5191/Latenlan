import pygame
import random

from .entities import Projectile
from .util import display


class Demon(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (174, 348))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.vel = [0, 0]
        self.state = "idle"
        self.targetPosX = random.randint(200, 400)
        self.targetPosY = random.randint(75, 125)

    def draw(self):
        display.blit(self.image, self.rect)
        # pygame.draw.rect(display, (255, 0, 0), self.rect, 1)

    def update(self):
        if self.rect.x == self.targetPosX:
            self.targetPosX = random.randint(200, 300)
        elif self.rect.x < self.targetPosX:
            self.x += self.speed
        elif self.rect.x > self.targetPosX:
            self.x -= self.speed

        if self.rect.y == self.targetPosY:
            self.targetPosY = random.randint(100, 150)
        elif self.rect.y < self.targetPosY:
            self.y += self.speed
        elif self.rect.y > self.targetPosY:
            self.y -= self.speed
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

        self.draw()

    def summon(self, ghouls):
        if len(ghouls) < 5:
            ghouls.append(Ghoul(self.rect.x, self.rect.y,
                          0.5, "assets/enemies/ghoul.png"))


class Ghoul(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100
        self.vel = [0, 0]
        self.state = "idle"
        self.targetPosX = random.randint(random.randint(
            0, 200), random.randint(200, 480) - self.rect.width)
        self.targetPosY = random.randint(random.randint(
            0, 200), random.randint(200, 480) - self.rect.height)
        self.attack_timer = 0
        self.projectiles = []

    def draw(self):
        display.blit(self.image, self.rect)
        # pygame.draw.rect(display, (255, 0, 0), self.rect, 1)

    def update(self, target):
        if self.rect.x == self.targetPosX or self.targetPosX < target.rect.x - 100 or self.targetPosX > target.rect.x + 100:
            self.targetPosX = random.randint(
                target.rect.x - 100, target.rect.x + 100)
        elif self.rect.x < self.targetPosX:
            self.image = pygame.transform.flip(
                self.original_image, True, False)
            # give floating illusion to movement like up and down
            self.x += self.speed
            self.y += random.randint(-1, 1) * self.speed

        elif self.rect.x > self.targetPosX:
            self.image = self.original_image
            self.x -= self.speed
            self.y += random.randint(-1, 1) * self.speed

        if self.rect.y == self.targetPosY:
            self.targetPosY = random.randint(
                target.rect.y - 150, target.rect.y + 50)
        elif self.rect.y < self.targetPosY:
            self.y += self.speed
        elif self.rect.y > self.targetPosY:
            self.y -= self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.draw()
        self.attack()

    def attack(self):
        # every 2 seconds shoot 4 projectiles in a circle
        if self.attack_timer == 0:
            for i in range(4):
                self.projectiles.append(Projectile(
                    self.rect.x, self.rect.y, 1, 1, "assets/enemies/projectile.png", i * 90))
            self.attack_timer = 240
        elif self.attack_timer > 0:
            self.attack_timer -= 1

    def hit(self, damage):
        self.health -= damage
