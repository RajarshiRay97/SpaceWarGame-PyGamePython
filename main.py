import pygame
import math
import random
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

mixer.music.load('bensound-happyrock.wav')
mixer.music.play(-1)

pygame.display.set_caption("SpaceWar")

icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

background = pygame.image.load('space.png')
boundaryline = pygame.image.load('boundary.png')

score_value = 0
font = pygame.font.Font('Brightly Crush Shine.otf', 30)
textx = 10
texty = 10

overfont = pygame.font.Font('Brightly Crush Shine.otf', 60)

def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


playerImg = pygame.image.load('spacerocket.png')
playerx = 370
playery = 480
playerx_change = 0

enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
no_of_enemy = 6
for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(8)
    enemyy_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 480
bulletx_change = 0
bullety_change = 25
bullet_state = "ready"

bullet1Img = pygame.image.load('bullet1.png')
bullet1x = 0
bullet1y = 480
bullet1x_change = 0
bullet1y_change = 25
bullet1_state = "ready"

explosionImg = pygame.image.load('explosion.png')


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 30))


def fire_bullet1(x, y):
    global bullet1_state
    bullet1_state = "fire"
    screen.blit(bullet1Img, (x + 16, y - 30))


def iscollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow((enemyx - bulletx), 2)) + (math.pow((enemyy - bullety), 2)))
    if distance <= 27:
        return True
    else:
        return False


def iscollision1(enemyx, enemyy, bullet1x, bullet1y):
    distance1 = math.sqrt((math.pow((enemyx - bullet1x), 2)) + (math.pow((enemyy - bullet1y), 2)))
    if distance1 <= 27:
        return True
    else:
        return False

def show_gameover():
    over = overfont.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over, (250, 270))



def explosion(x, y):
    screen.blit(explosionImg, (x, y))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(boundaryline,(0,478))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -10
            if event.key == pygame.K_RIGHT:
                playerx_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('gunshot.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
                elif bullet1_state == "ready":
                    bullet1_sound = mixer.Sound('gunshot.wav')
                    bullet1_sound.play()
                    bullet1x = playerx
                    fire_bullet1(bullet1x, bullet1y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    for i in range(no_of_enemy):
        if enemyx[i] <= 0:
            enemyx_change[i] = 8
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -8
            enemyy[i] += enemyy_change[i]
        enemyx[i] += enemyx_change[i]

        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)

        if collision:
            collision_sound = mixer.Sound('expo.wav')
            collision_sound.play()
            bullety = 480
            bullet_state = "ready"
            explosion(enemyx[i], enemyy[i])
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        collision1 = iscollision1(enemyx[i], enemyy[i], bullet1x, bullet1y)

        if collision1:
            collision1_sound = mixer.Sound('expo.wav')
            collision1_sound.play()
            bullet1y = 480
            bullet1_state = "ready"
            explosion(enemyx[i], enemyy[i])
            score_value += 1
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

        if enemyy[i] >= 440:
            for j in range(no_of_enemy):
                enemyy[j] = 2000
            playery = 2000
            playerx = 2000
            show_gameover()
            break
        enemy(enemyx[i], enemyy[i], i)

    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    if bullet1y <= 0:
        bullet1y = 480
        bullet1_state = "ready"

    if bullet1_state == "fire":
        fire_bullet1(bullet1x, bullet1y)
        bullet1y -= bullet1y_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
