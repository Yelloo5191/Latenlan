import pygame

from .config import *
from .util import display

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image, world):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(image)
        self.original_image = pygame.transform.scale(self.original_image, (16, 16))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(0, -2)
        self.rect.x = x
        self.rect.y = y
        self.width = self.rect.width
        self.height = self.rect.height
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
        self.dashing = False
        self.dash_timer = 0
        self.dash_speed = 50
        self.max_health = 40
        self.health = 40

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
        if keys[pygame.K_LSHIFT]:
            if self.dash_timer == 0:
                self.dashing = True
                self.dash_timer = 240
        if self.dash_timer > 0:
            self.dash_timer -= 1
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
        if self.dashing:
            if self.direction == "right":
                if not self.collisions["right"]:
                    if self.rect.x + self.dash_speed + self.width > WIDTH:
                        self.vel[0] += WIDTH - self.rect.x - self.width
                    else:
                        self.vel[0] += self.dash_speed
            elif self.direction == "left":
                if not self.collisions["left"]:
                    if self.rect.x - self.dash_speed < 0:
                        self.vel[0] -= self.rect.x
                    else:
                        self.vel[0] -= self.dash_speed
            self.dashing = False

        self.y_momentum += self.gravity
        if self.y_momentum > 10:
            self.y_momentum = 10
        self.vel[1] += self.y_momentum

        self.movement()
        self.animate()
        self.draw()

    def collide_test(self, tiles):
        return [tile for tile in tiles if self.rect.colliderect(tile.rect)]

    def movement(self):
        self.collisions = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.vel[0]
        hit_list = self.collide_test(self.world.tile_list)
        for tile in hit_list:
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
                self.rect.bottom = tile.rect.top
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
    
    def hit(self, dmg):
        if self.health - dmg <= 0:
            self.health = 0
            self.die()
        else:
            self.health -= dmg
    
    def die(self, game):
        pass