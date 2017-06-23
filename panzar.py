import subprocess
import pygame
import time
from object import Object


class Panzar(Object):
    health = 0
    firetime = 0
    def __init__(self, x, y, health, direction,  image, width, height):
        self.x = x
        self.y = y
        self.health = health
        self.direction = direction
        self.image = pygame.image.load(image)
        self.imagewidth, self.imageheight = self.image.get_size()
        self.screen['width'] = width
        self.screen['height'] = height

    def move(self):
        if (self.direction == 0):
            self.y = max(self.y - self.speed, 0)
        if (self.direction == 1):
            self.x = min(self.x + self.speed, self.screen['width']-self.imagewidth)
        if (self.direction == 2):
            self.y = min(self.y + self.speed, self.screen['height']-self.imageheight)
        if (self.direction == 3):
            self.x = max(self.x - self.speed, 0)

    def move_back(self):
        if (self.direction == 2):
            self.y = max(self.y - self.speed, 0)
        if (self.direction == 3):
            self.x = min(self.x + self.speed, self.screen['width']-self.imagewidth)
        if (self.direction == 0):
            self.y = min(self.y + self.speed, self.screen['height']-self.imageheight)
        if (self.direction == 1):
            self.x = max(self.x - self.speed, 0)

    def get_muzzle_coordes(self):
        if (self.direction == 0):
            return (self.x+self.imagewidth/2-10, self.y)
        if (self.direction == 1):
            return (self.x + self.imagewidth, self.y + self.imageheight/2-10)
        if (self.direction == 2):
            return (self.x + self.imagewidth/2-10, self.y+self.imageheight)
        if (self.direction == 3):
            return(self.x, self.y+self.imageheight/2-10)

    def fire(self):
        self.firetime = int(round(time.time() * 1000))

    def is_reloading(self):
        return int(round(time.time() * 1000)) - 1000 <= self.firetime