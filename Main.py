# Import Stuff That we need
import pygame
import math
import random
from pygame import mixer as mix

# Set the basic styling
pygame.init()
screen = pygame.display.set_mode((800, 600))
is_running = True
title = "Space Invaders"
background = pygame.image.load('background.png')
pygame.display.set_caption(title)
icon = pygame.image.load("space-invaders.png")
pygame.display.set_icon(icon)
# Load and play music
mix.music.load('background.mp3')
mix.music.play(-1)

# Player
player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_number = 6
for i in range(enemy_number):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(5)
    enemy_y_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

score_value = 0
text = pygame.font.Font('Capture it.ttf', 32)
text_x = 10
text_y = 10

game_over_font = pygame.font.Font('Positive System.otf', 100)


# Show the score
def show_score(x, y):
    score = text.render(f"Score: {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (x, y))


# Show the GAME OVER text
def game_over_text():
    over_text = game_over_font.render(f"GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (110, 250))


# Draw The Enemy
def enemy(x, y, e):
    screen.blit(enemy_img[e], (x, y))


# Draw The Player
def player(x, y):
    screen.blit(player_img, (x, y))


# Fire The Bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Detect Collisions
def collision(bullet_xcor, bullet_ycor, enemy_xcor, enemy_ycor):
    dist = math.sqrt(math.pow(enemy_xcor - bullet_xcor, 2) + (math.pow(enemy_ycor - bullet_ycor, 2)))
    if dist < 27:
        return True
    else:
        return False


# Game Loop
while is_running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mix.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(player_x, bullet_y)
                    bullet_x = player_x
                fire_bullet(player_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_x_change = 0

    # Player Movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement
    for i in range(enemy_number):
        collide = collision(player_x, player_y, enemy_x[i], enemy_y[i])
        if enemy_y[i] > 440:
            for h in range(enemy_number):
                enemy_y[h] = 2000
            game_over_text()
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 5
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -5
            enemy_y[i] += enemy_y_change[i]
        # Use the collision function to detect a collision
        detect = collision(bullet_x, bullet_y, enemy_x[i], enemy_y[i])
        if detect:
            collide_sound = mix.Sound('explosion.wav')
            collide_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        # Score and other stuff
    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
