import math
import random
import time

import pygame

render_way = 1
render_by_time = True
line_generation_gap = 1
ZERO = 1e-9
width = 2560
height = 1440
num_obs = 10
num_points = 5000
radius = 3
line_width = 10
point_color = (190, 190, 100)
show_lines = True
use_actual_mouse = False


def Vector(x, y):
    return (x[0] - y[0], x[1] - y[1])


def negative(vector):
    return (-vector[0], -vector[1])


def vector_product(vectorA, vectorB):
    return vectorA[0] * vectorB[1] - vectorB[0] * vectorA[1]


def is_intersected(A, B, C, D):
    AC = Vector(A, C)
    AD = Vector(A, D)
    BC = Vector(B, C)
    BD = Vector(B, D)
    CA = negative(AC)
    CB = negative(BC)
    DA = negative(AD)
    DB = negative(BD)

    return (vector_product(AC, AD) * vector_product(BC, BD) <= ZERO) \
        and (vector_product(CA, CB) * vector_product(DA, DB) <= ZERO)


def in_frame(pos):
    return 0 < pos[0] < width and 0 < pos[1] < height


def move(pos, angle):
    return (pos[0] + math.cos(angle / 180 * math.pi) * 10, pos[1] + math.sin(angle / 180 * math.pi) * 10)


def fuck_line(origin_pos, angle):
    last_pos = origin_pos
    flag = True
    while in_frame(last_pos) and flag:
        pygame.draw.circle(screen, (*point_color, random.randint(20, 50)), last_pos, radius)
        cur_pos = move(last_pos, angle)
        for line in obstacles:
            if is_intersected(cur_pos, last_pos, *line):
                flag = False
        last_pos = cur_pos


pygame.init()
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
central_pos = (width / 2, height / 2)
rendered_line_number = 0
if __name__ == '__main__':
    pygame.display.set_caption("Ray")

    obstacles = []
    start_time = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
        if use_actual_mouse:
            mouse_pos = pygame.mouse.get_pos()
            central_pos = mouse_pos
        else:
            central_pos = (central_pos[0] + random.random() * 200 - 15, central_pos[1] + random.random() * 150 - 15)
            central_pos = (central_pos[0] % width, central_pos[1] % height)

        surface2 = screen.convert_alpha()
        screen.fill((40, 35, 70))
        surface2.fill((255, 255, 255, 0))

        if render_way == 1:
            for i in range(0, 360, 3):
                fuck_line(central_pos, i)
        elif render_way == 2:
            for i in range(100):
                for j in range(100):
                    cur_pos = (width / 100 * i, height / 100 * j)
                    flag = True
                    for line in obstacles:
                        if is_intersected(cur_pos, central_pos, *line):
                            flag = False
                    if flag:
                        pygame.draw.circle(screen, (*point_color, random.randint(0, 50)), cur_pos, radius)
        elif render_way == 3:
            for _ in range(num_points):
                pos = (random.randint(0, width), random.randint(0, height))
                flag = True
                for line in obstacles:
                    if is_intersected(pos, central_pos, *line):
                        flag = False
                if flag:
                    pygame.draw.circle(surface2, (*point_color, random.randint(30, 70)), pos, radius)

        if render_by_time:
            if rendered_line_number * line_generation_gap < time.time() - start_time:
                rendered_line_number += 1
                pos1 = (random.randint(0, width), random.randint(0, height))
                pos2 = (random.randint(0, width), random.randint(0, height))
                obstacles.append((pos1, pos2))
        else:
            if random.random() < 0.01:
                pos1 = (random.randint(0, width), random.randint(0, height))
                pos2 = (random.randint(0, width), random.randint(0, height))
                obstacles.append((pos1, pos2))
        obstacles = obstacles[-num_obs:]
        if show_lines:
            for line in obstacles:
                pygame.draw.lines(screen, (255, 255, 255), False, line, line_width)
        screen.blit(surface2, (0, 0))
        pygame.display.update()
