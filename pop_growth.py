import pygame as pg
import os
import math
import random

# color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# screen specifics
screen_width = 1440
screen_height = 800

# values
x = 0
y = 0
iterations = 100
default_size = 100


def draw_point(display, x, y, color, point_size):

    pg.font.init()
    font = pg.font.Font(None, point_size)
    point = font.render(".", True, (color))
    point_pos = point.get_rect(centerx=x, y=y)

    display.blit(point, point_pos)


def function_linear(display, increment, x, y, iterations, point_size):

    for i in range(iterations):

        draw_point(display, 100 + x * 10, ((screen_height-80) - (point_size/2)) - y * 10, WHITE, point_size)

        y += increment
        x += 1


def draw_borders(display, increment, x, y, iterations, point_size):

    for i in range(iterations):

        draw_point(display, 100 + x * 10, ((screen_height-80) - (point_size/2)) - y * 10, GREY, point_size)

        draw_point(display, 100 + y * 10, ((screen_height-80) - (point_size / 2)) - x * 10, GREY, point_size)

        y += increment
        x += 1


def function_exponential(display, increment, x, y, iterations, point_size):

    y += 1
    for i in range(iterations):

        # draws point
        draw_point(display, 100 + x * 10, ((screen_height-80) - (point_size/2)) - y, GREEN, point_size)

        # updates values
        y *= increment
        x += 1


def function_reciprocal(display, increment, x, y, iterations, point_size):
    y += 1
    for i in range(iterations):

        # draws point
        draw_point(display, 100 + x * 10, ((screen_height-80) - (point_size/2)) - y*1000, RED, point_size)

        # updates values
        y *= 1/increment
        x += 1


def function_logarithmic(display, increment, x, y, iterations, point_size):

    y += 2
    for i in range(iterations):

        # updates values
        y = math.log(x+increment)
        x += 1

        # draws point
        draw_point(display, 100 + x * 10, ((screen_height-80) - (point_size/2)) - y * 100, BLUE, point_size)


def pop_sim_display(display, x, iterations, point_size, pop_size, pop_cap, birth_rate, death_rate):

    # define color hex (for fun)
    RANDOM_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    for i in range(iterations):

        # draw instance
        draw_point(display, 100 + x * 5, ((screen_height-80) - (point_size/2)) - pop_size * 10, RANDOM_COLOR, point_size)

        # update population size
        pop_size += (pop_size/2) * birth_rate
        pop_size -= death_rate

        # update rates
        death_rate = -1 + pop_size/pop_cap
        if pop_size >= pop_cap:
            birth_rate = 0
        else:
            birth_rate = 1

        # print(pop_size + ", " + birth_rate + "," + death_rate)

        # iterate instance
        x += 1


def main():
    # initialize pygame
    pg.init()

    # create screen
    screen = pg.display.set_mode((screen_width, screen_height), pg.SCALED)
    pg.display.set_caption("population growth simulation")

    # define objects
    clock = pg.time.Clock()

    # functions
    # function_linear(screen, 1, x, y, 1000, default_size)
    # function_exponential(screen, 1.5, x, y, 1000, default_size)
    # function_reciprocal(screen, 1.5, x, y, 1000, default_size)
    # function_logarithmic(screen, 1.5, x, y, 1000, default_size)

    # population simulation
    pop_sim_display(screen, x, 1000, default_size, 5, 20, 1, 1)

    # draw borders
    pg.draw.aaline(screen, GREY, (100, 0), (100, screen_height))
    pg.draw.aaline(screen, GREY, (0, (screen_height-80)), (screen_width, (screen_height-80)))
    draw_borders(screen, 0, x, y, 1000, 50)

    # draw milestones
    draw_point(screen, 100, (screen_height - 230), RED, 100)
    draw_point(screen, 100, (screen_height-330), RED, 100)
    draw_point(screen, 100, (screen_height - 430), RED, 100)

    # update display
    pg.display.flip()

    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                going = False
                os.sys.exit()
                pg.quit()


main()
