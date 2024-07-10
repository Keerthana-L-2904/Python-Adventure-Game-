import pygame
import sys
from tkinter import *

pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FIREBALL_RATE = 25

# Initialize Pygame window and set up
canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Web Adventure Run Game')
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 20)

# Load images and set initial positions
cactus_img = pygame.image.load('cactus_bricks.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0

fire_img = pygame.image.load('fire_bricks.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0

# Define classes
class Topscore:
    def __init__(self):
        self.maxx = 0

    def top_score(self, score):
        if score > self.maxx:
            self.maxx = score
        return self.maxx

topscore = Topscore()

class Monster:
    monster_velocity = 10

    def __init__(self):
        self.monster_img = pygame.image.load('monster.png')
        self.monster_img_rect = self.monster_img.get_rect()
        self.monster_img_rect.width -= 10
        self.monster_img_rect.height -= 10
        self.monster_img_rect.top = WINDOW_HEIGHT / 2
        self.monster_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.monster_img, self.monster_img_rect)
        if self.monster_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.monster_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.monster_img_rect.top -= self.monster_velocity
        elif self.down:
            self.monster_img_rect.top += self.monster_velocity

class Fireball:
    fireball_velocity = 20

    def __init__(self):
        self.fire = pygame.image.load('fireball.png')
        self.fireball_img = pygame.transform.scale(self.fire, (20, 20))
        self.fireball_img_rect = self.fireball_img.get_rect()
        self.fireball_img_rect.top = monster.monster_img_rect.bottom + 10
        self.fireball_img_rect.left = monster.monster_img_rect.left

    def update(self):
        canvas.blit(self.fireball_img, self.fireball_img_rect)
        if self.fireball_img_rect.left > 0:
            self.fireball_img_rect.left -= self.fireball_velocity

class SuperBoy:
    velocity = 10

    def __init__(self):
        self.superboy_img = pygame.image.load('boy.png')
        self.superboy_img_rect = self.superboy_img.get_rect()
        self.superboy_img_rect.left = 20
        self.superboy_img_rect.top = WINDOW_HEIGHT / 2 - 100
        self.down = True
        self.up = False
        self.superboy_score = 0 

    def update(self):
        canvas.blit(self.superboy_img, self.superboy_img_rect)
        if self.superboy_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if SCORE > self.superboy_score:
                self.superboy_score = SCORE
        if self.superboy_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.superboy_score:
                self.superboy_score = SCORE
        if self.up:
            self.superboy_img_rect.top -= 10
        if self.down:
            self.superboy_img_rect.bottom += 10

def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('died.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('end.jpg')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    canvas.blit(game_over_img, game_over_img_rect)
    
    #POSITION
    tk_width = 400
    tk_height = 200
    tk_x = (WINDOW_WIDTH// 2)+150
    tk_y = (WINDOW_HEIGHT // 2 )+150
    
    #Tkinter Window
    root = Tk()
    root.title("Game Over")
    root.geometry(f"{tk_width}x{tk_height}+{tk_x}+{tk_y}")

    label_score = Label(root, text=f"Your Score: {SCORE}", font=("Helvetica", 16))
    label_score.pack(pady=10)

    label_top_score = Label(root, text=f"Top Score: {topscore.maxx}", font=("Helvetica", 16))
    label_top_score.pack(pady=10)

    def play_again():
        root.destroy()
        game_loop()

    def quit_game():
        pygame.quit()
        sys.exit()

    play_again_button = Button(root, text="Play Again", command=play_again)
    play_again_button.pack(pady=10)

    quit_button = Button(root, text="Quit", command=quit_game)
    quit_button.pack(pady=10)

    root.mainloop()

def start_game():
    canvas.fill(BLACK)
    start_img = pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

def check_level(SCORE):
    global LEVEL
    if SCORE < 10:
        cactus_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE < 20:
        cactus_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE < 30:
        cactus_img_rect.bottom = 150
        fire_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE < 40:
        cactus_img_rect.bottom = 200
        fire_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4
    elif SCORE < 50:
        cactus_img_rect.bottom = 250
        fire_img_rect.top = WINDOW_HEIGHT - 250
        LEVEL = 5
    else:
        cactus_img_rect.bottom = 300
        fire_img_rect.top = WINDOW_HEIGHT - 300
        LEVEL = 6

def game_loop():
    global monster
    monster = Monster()
    fire = Fireball()
    superboy = SuperBoy()
    fireball_count = 0
    global SCORE
    SCORE = 0
    global HIGH_SCORE
    fireball_list = []
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1, 0.0)
    while True:
        canvas.fill(BLACK)
        check_level(SCORE)
        monster.update()
        fireball_count += 1

        if fireball_count == ADD_NEW_FIREBALL_RATE:
            fireball_count = 0
            new_flame = Fireball()
            fireball_list.append(new_flame)
        for f in fireball_list:
            if f.fireball_img_rect.left <= 0:
                fireball_list.remove(f)
                SCORE += 1
            f.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    superboy.up = True
                    superboy.down = False
                elif event.key == pygame.K_DOWN:
                    superboy.down = True
                    superboy.up = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    superboy.up = False
                    superboy.down = True
                elif event.key == pygame.K_DOWN:
                    superboy.down = True
                    superboy.up = False

        score_font = font.render('Score:' + str(SCORE), True, GREEN)
        score_font_rect = score_font.get_rect()
        score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height / 2)
        canvas.blit(score_font, score_font_rect)

        level_font = font.render('Level:' + str(LEVEL), True, GREEN)
        level_font_rect = level_font.get_rect()
        level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height / 2)
        canvas.blit(level_font, level_font_rect)

        top_score_font = font.render('Top Score:' + str(topscore.maxx), True, GREEN)
        top_score_font_rect = top_score_font.get_rect()
        top_score_font_rect.center = (800, cactus_img_rect.bottom + score_font_rect.height / 2)
        canvas.blit(top_score_font, top_score_font_rect)

        canvas.blit(cactus_img, cactus_img_rect)
        canvas.blit(fire_img, fire_img_rect)
        superboy.update()

        for f in fireball_list:
            if f.fireball_img_rect.colliderect(superboy.superboy_img_rect):
                game_over()
                if SCORE > superboy.superboy_score:
                    superboy.superboy_score = SCORE
        pygame.display.update()
        CLOCK.tick(FPS)

start_game()

