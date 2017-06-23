import pygame


class Object:
    direction = 0
    speed = 0
    x = 0
    y = 0
    image = 0
    screen = {}
    imagewidth = 0
    imageheight = 0

    def __init__(self, x, y, image, width, height):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.imagewidth, self.imageheight = self.image.get_size()
        self.screen['width'] = width
        self.screen['height'] = height

    def get_image(self):
        return pygame.transform.rotate(self.image, -90*self.direction)

    def collides_with(self, obj):
        if (self.x + self.imagewidth >= obj.x >= self.x and self.y + self.imageheight >= obj.y >= self.y):
            return True
        elif (self.x + self.imagewidth >= obj.x + obj.imagewidth >= self.x and self.y + self.imageheight >= obj.y >= self.y):
            return True
        elif (self.x + self.imagewidth >= obj.x >= self.x and self.y + self.imageheight >= obj.y + obj.imageheight >= self.y):
            return True
        elif (self.x + self.imagewidth >= obj.x + obj.imagewidth >= self.x and self.y + self.imageheight >= obj.y + obj.imageheight >= self.y):
            return True
        else:
            return False