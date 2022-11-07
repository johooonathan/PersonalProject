import pygame as pg
import random as rd


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        ball_speed_x *= -1
        opponent_score += 1
        reset()
    if ball.right >= screen_width:
        ball_speed_x *= -1
        player_score += 1
        reset()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.bottom = screen_height
    elif player.bottom >= screen_height:
        player.top = 0


def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed



def print_score():
    font = pg.font.Font(None, 100)
    player_counter = font.render(f"score: {player_score}", True, (GREY))
    textpos_player = player_counter.get_rect(centerx=background.get_width()/2 - 200, y=100)

    opponent_counter = font.render(f"score: {opponent_score}", True, (GREY))
    textpos_opponent = opponent_counter.get_rect(centerx=background.get_width() / 2 + 200, y=100)

    screen.blit(player_counter, textpos_player)
    screen.blit(opponent_counter, textpos_opponent)


def restart():
    global player_score, opponent_score
    loop = False
    player_score = 0
    opponent_score = 0

    loop = True

def reset():
    loop = False
    def_game_obj_and_var()
    loop = True


def def_game_obj_and_var():
    global ball, player, opponent, ball_size_x, ball_size_y, ball_speed_x, ball_speed_y, MYSTERY_COLOR, BLACK, WHITE, GREY

    # game_variables
    ball_speed_x = rd.randrange(-15, 15)
    ball_speed_y = rd.randrange(-15, 15)
    ball_size_x = rd.randrange(10, 100)
    ball_size_y = rd.randrange(10, 100)

    # color definitions
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (100, 100, 100)
    MYSTERY_COLOR = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))

    #game objects
    ball = pg.Rect(screen_width / 2, screen_height / 2, ball_size_x, ball_size_y)
    player = pg.Rect(10, screen_height / 2, 10, 140)
    opponent = pg.Rect(screen_width - 20, screen_height / 2, 10, 140)


# screen specifics
screen_width = 2480
screen_height = 1280

# game variables
loop = True
player_speed = 0
opponent_speed = 7
player_score = 0
opponent_score = 0


# game objects

while True:
    if loop:
        pg.init()

        def_game_obj_and_var()

        screen = pg.display.set_mode((screen_width, screen_height), pg.SCALED)
        pg.display.set_caption("A Really really bad version of pong")

        background = pg.Surface(screen.get_size())
        background = background.convert()
        background.fill(WHITE)

        clock = pg.time.Clock()



        going = True
        while going:
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        player_speed += 7
                    if event.key == pg.K_w:
                        player_speed -= 7

                    if event.key == pg.K_r:
                        restart()
                        going = False
                    if event.key == pg.K_t:
                        reset()

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_s:
                        player_speed -= 7
                    if event.key == pg.K_w:
                        player_speed += 7

            # game logic
            ball_animation()
            opponent_animation()
            player_animation()

            # visuals
            screen.blit(background, (0, 0))
            pg.draw.rect(screen, GREY, player)
            pg.draw.rect(screen, GREY, opponent)
            pg.draw.ellipse(screen, MYSTERY_COLOR, ball)
            pg.draw.aaline(screen, GREY, (screen_width/2, 0), (screen_width/2,screen_height))

            print_score()
            pg.display.flip()


