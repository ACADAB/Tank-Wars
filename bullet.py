import pygame
from object import Object

class Bullet(Object):
    speed = 25
    def __init__(self, x, y, image, width, height, direction):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.imagewidth, self.imageheight = self.image.get_size()
        self.screen['width'] = width
        self.screen['height'] = height
        self.direction = direction

    def move(self):
        if (self.direction == 0):
            self.y -= self.speed
        if (self.direction == 1):
            self.x += self.speed
        if (self.direction == 2):
            self.y += self.speed
        if (self.direction == 3):
            self.x -= self.speed
    def out_of_bounds(self):
        return self.x > self.screen['width'] or self.x < 0 or self.y < 0 or self.y > self.screen['height']