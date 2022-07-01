import pygame
import random
import time

pygame.init()

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

unit_width = screen_width//30
unit_height = screen_height//30

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

gameFont1 = pygame.font.SysFont('Gulim', 20)
gameFont2 = pygame.font.SysFont('Gulim', 20)

class Snake:
    def __init__(self, x, y):
        self.color = COLOR_GREEN
        self.body = [[x, y]]
        self.count = 1
        self.dir = 1 # 0은 오른쪽, 1은 위쪽, 2는 왼쪽, 3은 아래쪽
        self.tail = self.body[-1]

    def grow(self):
        self.count += 1
        self.body.append(self.tail)

    def setDir(self, dir):
        if abs(self.dir - dir) == 2: return
        self.dir = dir

    def move(self):
        head = self.body[0][:]
        self.tail = self.body.pop()

        if self.dir == 0:
            head[0] += unit_width
        elif self.dir == 1:
            head[1] -= unit_height
        elif self.dir == 2:
            head[0] -= unit_width
        else:
            head[1] += unit_height

        self.body.insert(0, head)
        
    def checkEatFood(self, food):
        rect = pygame.Rect(self.body[0][0], self.body[0][1], unit_width, unit_height)
        if rect.colliderect(food):
            return True
        else:
            return False

    def checkCollideSelf(self):
        return self.body[0] in self.body[1:]

    def draw(self):
        for i in range(self.count):
            rect = pygame.Rect(self.body[i][0], self.body[i][1], unit_width, unit_height)
            pygame.draw.rect(screen, self.color, rect)
        
class Food:
    def __init__(self):
        self.color = COLOR_RED
        self.x = random.randrange(0, 600, unit_width)
        self.y = random.randrange(0, 600, unit_height)
        self.width = unit_width
        self.height = unit_height

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def change(self, snake:Snake):
        while True:
            self.x = random.randrange(0, 600, unit_width)
            self.y = random.randrange(0, 600, unit_height)
            rect = pygame.Rect(self.x, self.y, self.width, self.height)

            isValid = True
            for sna in snake.body:
                snakeRect = pygame.Rect(sna[0], sna[1], self.width, self.height)
                if rect.colliderect(snakeRect):
                    isValid = False
                    break
            if isValid: break 
            
count = 0
moveRate = 15
clock = pygame.time.Clock()
pygame.display.set_caption('Snake Game')

randx = random.randrange(0, 600, unit_width)
randy = random.randrange(0, 600, unit_height)

snake = Snake(randx, randy)

food = Food()

score = 0
gametime = 0
level = 1


isSnake = False
running = True
while running:
    clock.tick(60)
    count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            isSnake = True

    screen.fill(COLOR_WHITE)

    foodRect = food.getRect()
    pygame.draw.rect(screen, COLOR_RED, foodRect)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]: snake.setDir(0)
    if keys[pygame.K_w]: snake.setDir(1)
    if keys[pygame.K_a]: snake.setDir(2)
    if keys[pygame.K_s]: snake.setDir(3)

    if isSnake:
        if count % moveRate == 0:
            snake.move()
            if snake.checkEatFood(foodRect):
                snake.grow()
                score += 1
                food.change(snake)

            if snake.checkCollideSelf():
                running = False
    else:
        start = gameFont1.render('게임을 시작하려면 아무키나 눌러주세요', False, COLOR_BLACK)
        screen.blit(start, (120, screen_height//2-50))
        startTime = time.time()

    snake.draw()

    gametime = int(time.time() - startTime)

    if gametime >= 120:
        level = 5
        moveRate = 2
    elif gametime >= 90:
        level = 4
        moveRate = 4
    elif gametime >= 60:
        level = 3
        moveRate = 6
    elif gametime >= 30:
        level = 2
        moveRate = 9
    elif gametime >= 15:
        level = 1
        moveRate = 12
    else:
        level = 0
        moveRate = 15

    timeText = gameFont2.render('time : ' + str(gametime), False, COLOR_BLACK)
    scoreText = gameFont2.render('score : ' + str(score), False, COLOR_BLACK)
    levelText = gameFont2.render('Level ' + str(level), False, COLOR_BLACK)
    
    screen.blit(timeText, (10, 10))
    screen.blit(scoreText, (screen_width - 100, 10))
    screen.blit(levelText, (screen_width//2 - 30, 10))

    if running == False:
        pass

    pygame.display.update()

pygame.quit()
