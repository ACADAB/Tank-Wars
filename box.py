import random
import pygame
from object import Object


class Box(Object):
    health = 1

    def __init__(self, x, y, image, width, height):
        self.image = pygame.image.load(image)
        self.imagewidth, self.imageheight = self.image.get_size()
        self.imagewidth -= 3
        self.imageheight -= 3
        self.screen['width'] = width
        self.screen['height'] = height
        self.x = x
        self.y = y