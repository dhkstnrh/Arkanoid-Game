import pygame
import random


def init():
    global x_pos_pedal, y_pos_pedal, rect_pedal, x_pos_ball, y_pos_ball, rect_ball, x_speed_ball, y_speed_ball, \
        rect_block, color_block, point, start

    # 페달을 화면 가운데에 두기
    x_pos_pedal = size_width_bg // 2 - size_width_pedal // 2
    y_pos_pedal = size_height_bg - size_height_pedal

    # 사각형의 정보를 가지고 있는 코드
    rect_pedal = pygame.Rect(x_pos_pedal, y_pos_pedal, size_width_pedal, size_height_pedal)

    x_pos_ball = size_width_bg // 2
    y_pos_ball = size_height_bg - size_height_pedal - size_radius_ball

    rect_ball = pygame.Rect(x_pos_ball, y_pos_ball, size_radius_ball * 2, size_radius_ball * 2)
    rect_ball.center = (x_pos_ball, y_pos_ball)

    # 공의 방향과 스피드
    x_speed_ball = 0.1
    y_speed_ball = 0.1

    # 블록 사이즈, 좌표, Rect
    rect_block = [[] for _ in range(10)]
    color_block = [[] for _ in range(10)]

    # 가로 10, 세로 3
    for i in range(10):
        for j in range(3):
            rect_block[i].append(pygame.Rect(i * size_width_block, j * size_height_block, size_width_block,
                                             size_height_block))
            color_block[i].append((random.randrange(255), random.randrange(150, 255), random.randrange(150, 255)))

    point = 0
    start = True


pygame.init()

background = pygame.display.set_mode((700, 480))
pygame.display.set_caption("Suwan_Arkanoid - Brick Breaking")

# 배경 사이즈
# 가로, 세로
size_width_bg = background.get_size()[0]
size_height_bg = background.get_size()[1]

# 페달의 사이즈, 좌표, rect
size_width_pedal = 100
size_height_pedal = 15

# 공의 사이즈, 좌표, Rect
size_radius_ball = 20

# 블록 사이즈, 좌표, Rect
size_width_block = size_width_bg // 10
size_height_block = 30

x_pos_block = 0
y_pos_block = 0

x_pos_mouse, y_pos_mouse = 0, 0

init()


# 숫자 찍기
def game_text(word, text_size=100, text_position=None):
    font = pygame.font.SysFont(None, text_size)

    text = font.render(word, True, (0, 0, 0))

    size_width_text = text.get_rect().size[0]
    size_height_text = text.get_rect().size[1]

    if text_position is None:
        x_pos_text = size_width_bg / 2 - size_width_text / 2
        y_pos_text = size_height_bg / 2 - size_height_text / 2
    else:
        x_pos_text, y_pos_text = text_position

    background.blit(text, (x_pos_text, y_pos_text))

def play_again():
    global play

    font = pygame.font.SysFont(None, 40)
    text = font.render("Press 'Enter' to play again or 'ESC' to quit", True, (0, 0, 0))

    size_width_text = text.get_rect().size[0]
    size_height_text = text.get_rect().size[1]

    x_pos_text = size_width_bg / 2 - size_width_text / 2
    y_pos_text = size_height_bg * 3 / 4 - size_height_text / 2

    background.blit(text, (x_pos_text, y_pos_text))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    init()
                    return
                elif event.key == pygame.K_ESCAPE:
                    play = False
                    return


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    # 시작 시간
    if start:
        start = False
        for i in range(3, 0, -1):
            background.fill((255, 255, 255))
            # 게임 시작 전 텍스트 출력
            game_text("Move the paddle with the mouse", text_size=36, text_position=(150, size_height_bg // 2 + 50))
            game_text(str(i))
            pygame.display.update()
            pygame.time.delay(1000)

    # 마우스로 페달 움직이기
    if event.type == pygame.MOUSEMOTION:
        x_pos_mouse, y_pos_mouse = pygame.mouse.get_pos()
        if x_pos_mouse - size_width_pedal // 2 >= 0 and x_pos_mouse + size_width_pedal // 2 <= size_width_bg:
            x_pos_pedal = x_pos_mouse - size_width_pedal // 2
            rect_pedal.left = x_pos_mouse - size_width_pedal // 2

    # 배경색 칠하기
    background.fill((255, 255, 255))

    # 페달 그리기
    pygame.draw.rect(background, (255, 255, 0), rect_pedal)

    # 공 좌표 계산
    if x_pos_ball - size_radius_ball <= 0:
        x_speed_ball = -x_speed_ball
    elif x_pos_ball >= size_width_bg - size_radius_ball:
        x_speed_ball = -x_speed_ball

    if y_pos_ball - size_radius_ball <= 0:
        y_speed_ball = -y_speed_ball
    elif y_pos_ball >= size_height_bg - size_radius_ball:
        background.fill((255, 255, 255))
        game_text("GAME OVER")
        play_again()
        continue

    # 공 좌표에 스피드 값 누적
    x_pos_ball += x_speed_ball
    y_pos_ball += y_speed_ball

    # 공 그리기
    rect_ball.center = (x_pos_ball, y_pos_ball)
    pygame.draw.circle(background, (255, 0, 255), (x_pos_ball, y_pos_ball), size_radius_ball)

    if rect_ball.colliderect(rect_pedal):
        y_speed_ball = -y_speed_ball

    # 블록 그리기 (for문으로 10개 * 3층 만들기)
    for i in range(10):
        for j in range(3):
            if rect_block[i][j]:
                pygame.draw.rect(background, color_block[i][j], rect_block[i][j])
                rect_block[i][j].topleft = (i * size_width_block, j * size_height_block)

                # 공 - 벽돌 닿았을 때
                if rect_ball.colliderect(rect_block[i][j]):
                    x_speed_ball = -x_speed_ball
                    y_speed_ball = -y_speed_ball
                    rect_block[i][j] = 0
                    point += 1

        # 게임 클리어
        if point == 30:
            background.fill((255, 255, 255))
            game_text("GAME CLEAR")
            play_again()
            continue

    pygame.display.update()

pygame.quit()
