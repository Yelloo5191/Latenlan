import pygame
from .config import *

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(SCALED_WINDOW)

def load_map(path):
    f = open(path + '.txt', 'r')
    data = eval(f.read())
    f.close()
    return(data)