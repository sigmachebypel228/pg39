import pygame
from all_colors import *

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Рисование")
clock = pygame.time.Clock()

# Настройки кисти
BACKGROUND = (255, 255, 255)
brush_color = (0, 0, 0)
brush_width = 5
canvas = pygame.Surface(screen.get_size())
canvas.fill(BACKGROUND)

# Настройки палитры
dragging_pallete = False
border_color = (0, 0, 0)
cur_index = 0
color_size = 50
pallete_rect = pygame.Rect(10, 10, color_size * 12, color_size)
pallete = pygame.Surface(pallete_rect.size)
pallete_offset = (0, 0)

# Настройки прямоугольников
drawing_rect = False
start_pos = None
rect_color = red
fill_rect = False
current_rects = []


def draw_pallete():
    pallete.fill(BACKGROUND)
    for i in range(12):
        color_rect = pygame.Rect(i * color_size, 0, color_size, color_size)
        pygame.draw.rect(pallete, colors[i], color_rect)
    border_rect = pygame.Rect(cur_index * color_size, 0, color_size, color_size)
    pygame.draw.rect(pallete, border_color, border_rect, width=3)
    screen.blit(pallete, pallete_rect.topleft)


running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                if pallete_rect.collidepoint(event.pos):
                    selected_color_index = ((event.pos[0] - pallete_rect.left) // color_size)
                    cur_index = selected_color_index
                    brush_color = colors[cur_index]
                    rect_color = colors[cur_index]

            elif event.button == 3:  # ПКМ
                if pallete_rect.collidepoint(event.pos):
                    dragging_pallete = True
                    pallete_offset = (event.pos[0] - pallete_rect.x,
                                      event.pos[1] - pallete_rect.y)
                else:
                    drawing_rect = True
                    start_pos = mouse_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # ПКМ
                if dragging_pallete:
                    dragging_pallete = False
                elif drawing_rect:
                    drawing_rect = False
                    rect_width = mouse_pos[0] - start_pos[0]
                    rect_height = mouse_pos[1] - start_pos[1]
                    if abs(rect_width) > 5 and abs(rect_height) > 5:
                        rect = pygame.Rect(
                            min(start_pos[0], mouse_pos[0]),
                            min(start_pos[1], mouse_pos[1]),
                            abs(rect_width),
                            abs(rect_height)
                        )
                        current_rects.append((rect, rect_color, fill_rect))

        elif event.type == pygame.MOUSEMOTION:
            if dragging_pallete:
                pallete_rect.x = mouse_pos[0] - pallete_offset[0]
                pallete_rect.y = mouse_pos[1] - pallete_offset[1]

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fill_rect = not fill_rect
            elif event.key == pygame.K_c:
                canvas.fill(BACKGROUND)
                current_rects = []

    # Рисование кистью (ЛКМ)
    if mouse_pressed[0] and not pallete_rect.collidepoint(mouse_pos):
        pygame.draw.circle(canvas, brush_color, mouse_pos, brush_width)

    # Отрисовка
    screen.blit(canvas, (0, 0))

    # Отрисовка всех прямоугольников
    for rect, color, fill in current_rects:
        pygame.draw.rect(screen, color, rect, width=0 if fill else 1)

    # Отрисовка текущего прямоугольника
    if drawing_rect and not dragging_pallete:
        rect_width = mouse_pos[0] - start_pos[0]
        rect_height = mouse_pos[1] - start_pos[1]
        temp_rect = pygame.Rect(
            min(start_pos[0], mouse_pos[0]),
            min(start_pos[1], mouse_pos[1]),
            abs(rect_width),
            abs(rect_height)
        )
        pygame.draw.rect(screen, rect_color, temp_rect, width=0 if fill_rect else 1)

    draw_pallete()

    # Информация
    font = pygame.font.SysFont(None, 24)
    info = [
        "ЛКМ: Рисовать кистью / Выбирать цвет",
        "ПКМ: Рисовать прямоугольник",
        "ПКМ на палитре: Перемещать палитру",
        f"Заливка: {'ВКЛ (SPACE)' if fill_rect else 'ВЫКЛ (SPACE)'}",
        "Очистка: C"
    ]

    for i, text in enumerate(info):
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (10, SCREEN_HEIGHT - 30 - i * 25))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()