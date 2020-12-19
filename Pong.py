import sys
import pygame
import random


def ball_animations():
    global ball_speed_x, ball_speed_y, opponent_score, player_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - player.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - opponent.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animations():
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top <= ball.y:
        opponent.top += opponent_speed
    if opponent.bottom >= ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time
    ball.center = (screen_width / 2, screen_height / 2)

    current_time = pygame.time.get_ticks()
    if current_time - score_time < 1000:
        num = game_font.render("3", False, light_grey)
        screen.blit(num, (screen_width / 2 - 13, screen_height / 2 + 30))
    if 1000 < current_time - score_time < 2000:
        num = game_font.render("2", False, light_grey)
        screen.blit(num, (screen_width / 2 - 13, screen_height / 2 + 30))
    if 2000 < current_time - score_time < 3000:
        num = game_font.render("1", False, light_grey)
        screen.blit(num, (screen_width / 2 - 13, screen_height / 2 + 30))

    if current_time - score_time < 3000:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 5 * random.choice((1, -1))
        ball_speed_y = 5 * random.choice((1, -1))
        score_time = 0


# General Setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 600
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyPong")

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 10, screen_height / 2 - 10, 15, 15)
opponent = pygame.Rect(screen_width - 20, screen_height / 2 - 50, 10, 100)
player = pygame.Rect(10, screen_height / 2 - 50, 10, 100)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Game Variables
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = 5 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7
score_time = 1
pause = 1

# Sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

# Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 16)

# Game Loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_RETURN:
                pause *= -1
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7

    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Game Logic
    if pause > 0:
        player_animations()
        opponent_ai()
        ball_animations()
        player.y += player_speed
    else:
        paused = game_font.render("PAUSED", False, light_grey)
        screen.blit(paused, (20, 20))

    if score_time != 0:
        ball_restart()

    player_text = game_font.render(f"{player_score}", False, light_grey)
    if player_score > 9:
        screen.blit(player_text, (screen_width / 2 - 23, screen_height / 2 + 10))
    else:
        screen.blit(player_text, (screen_width / 2 - 13, screen_height / 2 + 10))
    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (screen_width / 2 + 5, screen_height / 2 + 10))

    pygame.display.flip()
    clock.tick(60)
