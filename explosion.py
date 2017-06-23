import pygame
import time
from object import Object

class Explosion(Object):
    start = 0
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.start = int(round(time.time() * 1000))
    def is_going(self):
        now = int(round(time.time() * 1000))
        return  now - 1000 <= self.start