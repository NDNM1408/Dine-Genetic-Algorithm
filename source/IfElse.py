import pygame
import os
import random
import sys
import numpy as np

pygame.init()

# Khởi tạo màn hình game
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Hình ảnh khủng long chạy
RUNNING = [pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png"))]

# Hình ảnh khủng long nhảy
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))

# Hình ảnh khủng long cúi người
DUCKING = [pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png"))]

# Hình ảnh xương rồng
SMALL_CACTUS = [pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png"))]

#Hình ảnh chim
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

BIGBIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird3.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird4.png"))]

# Hình ảnh đám mây
CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

# Hình ảnh nền
BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

#Thêm âm thanh
SoundOnJump = pygame.mixer.Sound('assets/Sounds/jump.wav')
SoundOnPoint = pygame.mixer.Sound('assets/Sounds/point.wav')
SoundOnDie = pygame.mixer.Sound('assets/Sounds/die.wav')

# Đối tượng khủng long
class Dinosaur:
    # Vị trí khởi tạo khủng long
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    # Hàm khởi tạo đối tượng khủng long
    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        # Trạng thái khủng long ban đầu
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.score = 0

        # Bước chạy của khủng long
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, self.image.get_width(), self.image.get_height())
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()            
            
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.dino_run = True

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)




class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = pygame.Rect(self.image[self.type].get_rect())
        self.rect.x = SCREEN_WIDTH + random.randint(0,200)*(1+game_speed*0.01)

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
        self.rect = self.rect

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

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    dinosaur = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0
    dinosaurs = [dinosaur]


    def score():
        global points, game_speed
        points += 1
        if points % 300 == 0:
            game_speed += 1
    
        if points % 200 == 0:
            SoundOnPoint.play()

        text = font.render("If Else Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
    def rectCollision(rect1, rect2):
        if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
            return True
        return False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        SCREEN.fill((255, 255, 255))
        # dinosaur.dino_jump = False
        # dinosaur.dino_run = True
        # dinosaur.dino_duck = False
        clock = pygame.time.Clock()


        dinosaur.update()
        speed_text = pygame.font.Font('freesansbold.ttf', 20).render(f'Game Speed:{str(game_speed)}', True, (0, 0, 0))
        SCREEN.blit(speed_text, (50, 510))



        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                if np.random.rand()<0.5:
                    obstacles.append(Bird(BIRD))
                else:
                    obstacles.append(BigBird(BIGBIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            # Nếu xảy ra va chạm giữa khủng long và vật thể sẽ kết thúc game
            if rectCollision(dinosaur.rect, obstacle.rect):
                SoundOnDie.play()
                dinosaur.score = points
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)
        
        dinosaur.draw(SCREEN)

  
        vr = game_speed
        vj = Dinosaur().JUMP_VEL * 4
        g = 0.8
        Dx = Dinosaur().image.get_width()
        Oy = 0
        if len(obstacles) > 0 :
            Oy = obstacles[0].image[0].get_height()
        h1 = vr * ((vj - np.sqrt(vj**2-2*g*Oy))/g) + Dx
        if len(obstacles) > 0:
            if (obstacles[0].rect.x-Dinosaur().rect.x) <= (h1 + Dx + 20) and 380 - (obstacles[0].rect.y+Oy) <40:
                if dinosaur.dino_duck == True:
                    dinosaur.dino_jump = True
                    dinosaur.dino_run = False
                    dinosaur.dino_duck = False
                if (dinosaur.rect.y == dinosaur.Y_POS or dinosaur.rect.y == dinosaur.Y_POS + 40):
                    SoundOnJump.play()
                    dinosaur.dino_jump = True
                    dinosaur.dino_run = False 
                    dinosaur.dino_duck = False
                
            if 380 - (obstacles[0].rect.y+Oy) >= 40:
                if dinosaur.rect.y == dinosaur.Y_POS:
                    dinosaur.dino_jump = False
                    dinosaur.dino_run = False
                    dinosaur.dino_duck = True
            if not (dinosaur.dino_jump or dinosaur.dino_duck):
                dinosaur.dino_jump = False
                dinosaur.dino_duck = False
                dinosaur.dino_run = True


        background()

        cloud.draw(SCREEN)
        cloud.update()
        clock.tick(120)

        score()
        
        pygame.display.update()

# Menu game
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
            score = font.render("If Else Score: " + str(points), True, (0, 0, 0))
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
                main()


menu(death_count=0)