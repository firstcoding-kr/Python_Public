import pygame
import random
import os

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('My Game')

clock = pygame.time.Clock()

# 현재 파일이 실행되는 코드의 경로를 가져오는 것
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'image')
# 배경 이미지
background = pygame.image.load(
    os.path.join(image_path, 'background.png')
)

# 캐릭터 설정
character = pygame.image.load(
    os.path.join(image_path, 'character.png')
)

character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_speed = 1

# 적 설정
enemy = pygame.image.load(
    os.path.join(image_path, 'enemy.png')
)
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_speed = 0.5

game_font = pygame.font.Font(None, 40)
gameover_msg = 'Game Over'

score_font = pygame.font.Font(None, 20)
score = 0

# 내 캐릭터의 최초 위치 (가로의 중앙)
posx = screen_width // 2 - character_width // 2
posy = screen_height - character_height

# 하늘에서 떨어지는 물체의 위치 정의
enemys = [ [random.randint(0, screen_width - enemy_width), 0] ]

loopCount = 0
# 메인 게임 루프
running = True
while running:
    dt = clock.tick(60) # 60 fps

    loopCount += 1
    if loopCount % 300 == 0: # 5초
        enemys.append([random.randint(0, screen_width - enemy_width), 0])
        enemy_speed += 0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: posx -= character_speed * dt
    if keys[pygame.K_RIGHT]: posx += character_speed * dt

    if posx < 0 : posx = 0
    if posx > screen_width - character_width :
        posx = screen_width - character_width

    character_rect = character.get_rect()
    character_rect.left = posx
    character_rect.top = posy
    screen.blit(character, (posx, posy))

    game_over_box = game_font.render(gameover_msg, False, (255, 0, 0))
    game_Msg_rect = game_over_box.get_rect()
    game_Msg_rect.center = (screen_width//2, screen_height//2)

    for e in enemys:
        e[1] += enemy_speed * dt

        # 물체가 바닥에 닿았을때
        if e[1] > screen_height - enemy_height:
            e[0] = random.randint(0, screen_width - enemy_width)
            e[1] = 0

            score += 1

        enemy_rect = enemy.get_rect()
        enemy_rect.left = e[0]
        enemy_rect.top = e[1]
        
        if character_rect.colliderect(enemy_rect):
            running = False
            screen.blit(game_over_box, game_Msg_rect)
            
        screen.blit(enemy, (e[0], e[1]))

    score_box = score_font.render('score : %d' % score, False, (0, 0, 0))
    screen.blit(score_box, (10, 10))

    #pygame.draw.rect(screen, (0, 255, 0), (posx, posy, 40, 40))
    pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
