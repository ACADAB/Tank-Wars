import pygame
import subprocess
from panzar import Panzar
from bullet import Bullet
from explosion import Explosion
from box import Box
import random


def get_screen_resolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    return {'width': int(resolution[0]), 'height': int(resolution[1])}


pygame.init()

display_width = int(get_screen_resolution()['width'])
display_height = int(get_screen_resolution()['height'])-60

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tank wars')
pygame.display.toggle_fullscreen()

black = (0, 0, 0)
white = (255, 255, 255)
clock = pygame.time.Clock()
tank_health = 2

boxwidth, boxheight = pygame.image.load('box.png').get_size()

def paint(obj,x, y):
    gameDisplay.blit(obj.get_image(), (x, y))

def isArrow(button):
    return (button == pygame.K_UP or button == pygame.K_RIGHT or button == pygame.K_DOWN or button == pygame.K_LEFT)

def isWASD(button):
    return (button == pygame.K_a or button == pygame.K_w or button == pygame.K_s or button == pygame.K_d)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def game_intro():
    intro = True
    global tank_health
    tank_health = 2
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    main_game()
                elif event.key == pygame.K_UP:
                    tank_health+=1
                elif event.key == pygame.K_DOWN:
                    tank_health=max(tank_health-1, 1)
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects(str(tank_health), largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        TextAnnouncement, TARect = text_objects("space to start, arrows to choose health, escape to exit", pygame.font.Font('freesansbold.ttf', 60))
        TARect.center = ((display_width / 2),(display_height * 0.75))
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(TextAnnouncement, TARect)
        pygame.display.update()
        clock.tick(15)

def main_game():

    crashed = False
    global tank_health

    arrows_down = 0
    wasd_down = 0

    bullets = list()
    boxes = list()
    explosions = list()

    for i in range(1, display_height - boxheight, 180):
        for j in range(1, display_width - boxheight, 180):
            if (random.randint(1, 3) % 2 != 0):
                boxes.append(Box(j, i, 'box.png', display_width, display_height))

    p2 = Panzar(display_width * 0.15, display_height * 0.5, tank_health, 1,'tank.png', display_width, display_height)
    p1 = Panzar(display_width * 0.8, display_height * 0.5, tank_health, 3,'tank.png', display_width, display_height)
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if isArrow(event.key):
                    p1.speed = 5
                    arrows_down += 1
                    if event.key == pygame.K_UP:
                        p1.direction = 0
                    elif event.key == pygame.K_RIGHT:
                        p1.direction = 1
                    elif event.key == pygame.K_DOWN:
                        p1.direction = 2
                    elif event.key == pygame.K_LEFT:
                        p1.direction = 3
                if(isWASD(event.key)):
                    p2.speed = 5
                    wasd_down += 1
                    if event.key == pygame.K_w:
                        p2.direction = 0
                    elif event.key == pygame.K_d:
                        p2.direction = 1
                    elif event.key == pygame.K_s:
                        p2.direction = 2
                    elif event.key == pygame.K_a:
                        p2.direction = 3
                if event.key == pygame.K_t and not p2.is_reloading():
                    p2.fire()
                    bullets.append(Bullet(p2.get_muzzle_coordes()[0], p2.get_muzzle_coordes()[1], 'bullet.png', display_width, display_height, p2.direction))
                    bullets[len(bullets) - 1].move()
                if event.key == pygame.K_m and not p1.is_reloading():
                    p1.fire()
                    bullets.append(Bullet(p1.get_muzzle_coordes()[0], p1.get_muzzle_coordes()[1], 'bullet.png', display_width, display_height, p1.direction))
                    bullets[len(bullets)-1].move()
                if event.key == pygame.K_ESCAPE:
                    crashed = True

            if event.type == pygame.KEYUP:
                if isArrow(event.key):
                    if(arrows_down == 1):
                        p1.speed = 0
                    arrows_down -= 1
                if(isWASD(event.key)):
                    if(wasd_down == 1):
                        p2.speed = 0
                    wasd_down -= 1

        gameDisplay.fill(white)
        for i in boxes:
            paint(i, i.x, i.y)

        p1.move()
        p2.move()
        if(p1.collides_with(p2)):
            p2.move_back()
            p1.move_back()

        for i in boxes:
            if p1.collides_with(i) or i.collides_with(p1):
                p1.move_back()
            if(p2.collides_with(i) or i.collides_with(p2)):
                p2.move_back()
        paint(p1, p1.x, p1.y)
        paint(p2, p2.x, p2.y)
        for i in bullets:
            if(i.out_of_bounds()):
                bullets.remove(i)
            else:
                paint(i, i.x, i.y)
            i.move()

            #collision between a bullet and a box
            for j in boxes:
                if i.collides_with(j) or j.collides_with(i):
                    explosions.append(Explosion(i.x, i.y, 'explose.png'))
                    bullets.remove(i)
                    j.health -= 1
                    if(j.health == 0):
                        boxes.remove(j)

            #collision with a bullet and a tank
            if i.collides_with(p1) or p1.collides_with(i):
                p1.health -= 1
                explosions.append(Explosion(i.x, i.y, 'explose.png'))
                bullets.remove(i)
                if(p1.health == 0):
                    restart(2)
            if i.collides_with(p2) or p2.collides_with(i):
                p2.health -= 1
                explosions.append(Explosion(i.x, i.y, 'explose.png'))
                bullets.remove(i)
                if (p2.health == 0):
                    restart(1)

        for i in explosions:
            if(i.is_going()):
                paint(i, i.x, i.y)
            else:
                explosions.remove(i)

        CountText, CTRect = text_objects(str(p2.health) + " : " + str(p1.health), pygame.font.Font('freesansbold.ttf', 30))
        CTRect.center = ((display_width / 2), (display_height * 0.5))
        gameDisplay.blit(CountText, CTRect)

        pygame.display.update()
        clock.tick(60)

def restart(n):
    res = True
    global tank_health
    tank_health = 2
    while res:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    game_intro()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 135)
        TextSurf, TextRect = text_objects("Tank " + str(n) + " is the winner", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        TextAnnouncement, TARect = text_objects("space to restart, escape to exit", pygame.font.Font('freesansbold.ttf', 60))
        TARect.center = ((display_width / 2), (display_height * 0.75))
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(TextAnnouncement, TARect)
        pygame.display.update()
        clock.tick(15)
game_intro()
pygame.quit()
quit()