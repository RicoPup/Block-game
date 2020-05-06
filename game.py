import pygame
import random
import sys

pygame.init()

pygame.mixer_music.load("Techno.wav")
pygame.mixer_music.play(-1)

WIDTH = 800
HEIGHT = 600

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOUR = (0, 0, 0)


class Player:
    size = 50
    pos = [WIDTH/2, HEIGHT-2*size]

    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.pos


p1 = Player(40, [int(WIDTH/2), int(HEIGHT-100)])


class Enemy:
    size = 50
    pos = [WIDTH/2, HEIGHT-2*size]

    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.pos


enemy_list = []

for i in range(1):
    e_size = random.randint(20, 100)
    e = Enemy(e_size, [random.randint(0, WIDTH - e_size), int(0+(2*e_size))])
    enemy_list.append(e)


# player_size = 50
# player_pos = [WIDTH/2, HEIGHT-2*player_size]

# enemy_size = 50
# enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
# enemy_list = [enemy_pos]

SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

_score = 0

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)


def set_level(score, spd):
    if score < 10:
        spd = 5
    elif score < 20:
        spd = 8
    elif score < 30:
        spd = 10
    elif score < 40:
        spd = 13
    elif score < 60:
        spd = 15
    elif score < 80:
        spd = 20
    return spd


def drop_enemies(enemies):
    delay = random.random()
    if len(enemies) < 10 and delay < 0.1:
        for i in range(1):
            e_size = random.randint(20, 100)
            e = Enemy(e_size, [random.randint(0, WIDTH - e_size), int(0 + 10)])
            enemies.append(e)


def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(screen, BLUE, (enemy.get_pos()[0], enemy.get_pos()[1], enemy.get_size(), enemy.get_size()))


def update_enemy_positions(enemies, score):
    for idx, enemy in enumerate(enemies):
        if enemy.get_pos()[1] >= 0 and enemy.get_pos()[1] < HEIGHT:
            enemy.get_pos()[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemies, player):
    for enemy_pos in enemies:
        if detect_collision(enemy_pos, player):
            return True
    return False


def detect_collision(player, enemy):
    p_x = player.get_pos()[0]
    p_y = player.get_pos()[1]

    e_x = enemy.get_pos()[0]
    e_y = enemy.get_pos()[1]

    if (e_x >= p_x and e_x < (p_x + player.get_size())) or (p_x >= e_x and p_x < (e_x + enemy.get_size())):
        if (e_y >= p_y and e_y < (p_y + player.get_size())) or (p_y >= e_y and p_y < (e_y + enemy.get_size())):
            return True
    return False


while not game_over:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = p1.get_pos()[0]
            y = p1.get_pos()[1]

            if event.key == pygame.K_LEFT:
                x -= p1.get_size()
            elif event.key == pygame.K_RIGHT:
                x += p1.get_size()

            p1.pos = [x, y]

    screen.fill(BACKGROUND_COLOUR)

    drop_enemies(enemy_list)
    _score = update_enemy_positions(enemy_list, _score)
    SPEED = set_level(_score, SPEED)

    if collision_check(enemy_list, p1):
        game_over = True

    text = "Score:" + str(_score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH-210, HEIGHT-40))

    draw_enemies(enemy_list)
    pygame.draw.rect(screen, RED, (p1.get_pos()[0], p1.get_pos()[1], p1.get_size(), p1.get_size()))

    clock.tick(30)

    pygame.display.update()
