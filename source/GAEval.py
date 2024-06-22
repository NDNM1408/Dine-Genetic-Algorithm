import pygame
import os
import random
import math 
import sys
import numpy as np
# from genetic import Genetic
pygame.init()


# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

BIGBIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird3.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird4.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.dino_duck = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0
        self.W = np.random.randn(16,5)
        self.W2 = np.random.randn(3,16)
        self.score = 0
    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect = self.image.get_rect()

        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1


    def duck(self):
        self.image = DUCKING[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS+40
        self.step_index += 1




    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH * game_speed / 20

    def update(self):
        self.rect.x -= game_speed*0.9

        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        pygame.draw.rect(SCREEN, (100,100,100), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        # self.image = image[self.step//5]
        self.rect.y = 250 + random.choice([-50,50,15])
        self.index = 0
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
        pygame.draw.rect(SCREEN, (100,100,100), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

class BigBird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250 - 50
        self.index = 0
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
        pygame.draw.rect(SCREEN, (100,100,100), (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

def remove(index):
    dinosaurs.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)



def eval(fps=30):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, points
    clock = pygame.time.Clock()
    

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    game_speed = 20
    points = 0
    obstacles = []
    dino_eval = Dinosaur()
    dino_eval.W = np.load('Data\w_best.npy')
    dino_eval.W2 = np.load('Data\w2_best.npy')
    print(f'W1: {dino_eval.W}')
    print(f'W2: {dino_eval.W2}')
    dinosaurs = [dino_eval]

    def score():
        global points, game_speed
        points += 1
        if points % 300 == 0:
            game_speed += 1
        text = FONT.render(f'GA Score:{points}', True, (0, 0, 0))
        text_2 = FONT.render(f'EVALUATE MODE!',True,(0,0,0))
        SCREEN.blit(text_2, (850, 20))
        SCREEN.blit(text, (850, 50))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        dino_eval.update()
        dino_eval.draw(SCREEN)
        speed_text = pygame.font.Font('freesansbold.ttf', 20).render(f'Game Speed:{str(game_speed)}', True, (0, 0, 0))
        SCREEN.blit(speed_text, (50, 510))

        if len(dinosaurs) == 0:
            print(f'Dino final score: {points}')
            break
        if dino_eval.dino_run==False:
            dino_eval.score+=0.1
        else:
            dino_eval.score+=1

        if len(obstacles) == 0:
            rand_int = random.randint(0, 2)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif rand_int == 2:
                if np.random.rand()<0.5:
                        obstacles.append(Bird(BIRD))
                else:
                    obstacles.append(BigBird(BIGBIRD))
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if dino_eval.rect.colliderect(obstacle.rect):
                dino_eval.score = points
                menu(1)
                dinosaurs = []
            else:
                if dino_eval.rect.y == dino_eval.Y_POS or dino_eval.rect.y == dino_eval.Y_POS+40:
                    # output = dino_eval.W @ np.array([dino_eval.rect.y,distance((dino_eval.rect.x, dino_eval.rect.y),obstacle.rect.midtop)],dtype=float).reshape(-1,1)
                    output = dino_eval.W @ np.array([dino_eval.rect.y,obstacle.rect.x,obstacle.rect.y,distance((dino_eval.rect.x, dino_eval.rect.y),obstacle.rect.midtop),game_speed],dtype=float).reshape(-1,1)
                    output   = np.maximum(output,0)
                    output = dino_eval.W2 @ output
                    output = output.reshape(-1)
                    if np.argmax(output)==0 :
                        dino_eval.dino_jump = True
                        dino_eval.dino_run = False
                        dino_eval.dino_duck = False
                    
                    elif np.argmax(output)==1 :
                        dino_eval.dino_jump = False
                        dino_eval.dino_run = False
                        dino_eval.dino_duck = True
                    else:
                        dino_eval.dino_jump = False
                        dino_eval.dino_run = True
                        dino_eval.dino_duck = False

        score()
        background()
        clock.tick(int(fps))
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        # Nếu lần đầu chơi
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        # Đã chơi và thua do mất mạng
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("GA Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                eval(120)
menu(0)