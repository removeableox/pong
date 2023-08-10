import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

BG = (15, 15, 15)
F = pygame.font.Font(None, 36)
GOF = pygame.font.Font(None, 50)

FPS = 60

class Item:
    def __init__(self, i, x, y, dim):
        self.item = i
        self.x = x
        self.y = y
        self.dim = dim

class Borders(Item):
    def __init__(self, x, y, dim, i='None'):
        super().__init__(i, x, y, dim)

CIEL = Borders(0, 0, (900, 0))
FLOOR = Borders(0, 500, (900, 0))
WALL_LEFT = Borders(0, 0, (0, 500))
WALL_RIGHT = Borders(900, 0, (0, 500))

def scale(item, x, y, xpos=None, ypos=None):
    new_dim = (x, y)
    item.dim = list(new_dim)
    item.item = pygame.transform.scale(item.item, new_dim)

    if xpos and ypos:
        print('hi')
        item.x = xpos
        item.y = ypos

PB = Item(pygame.image.load(os.path.join('Assets', 'box.svg')), 855, 0, [46, 140])
GB = Item(pygame.image.load(os.path.join('Assets', 'box.svg')), 0, 0, [46, 140])
B = Item(pygame.image.load(os.path.join('Assets', 'ball.svg')), 425, 175, [100, 100])

scale(GB, 23, 70)
scale(B, 50, 50)
scale(PB, 23, 70, 877, B.y - 10)

SPEED = 8

def collision_check(rect1, rect2):
    if rect1.x < rect2.x + int(rect2.dim[0]) and rect1.x + int(rect1.dim[0]) > rect2.x and rect1.y < rect2.y + int(rect2.dim[1]) and rect1.y + int(rect1.dim[1]) > rect2.y:
        return True
    return False

def draw_window(score):
    WIN.fill(BG)
    WIN.blit(PB.item, (PB.x, PB.y))
    WIN.blit(GB.item, (GB.x, GB.y))
    WIN.blit(B.item, (B.x, B.y))

    #score
    text = f"Score: {score}"
    text_surface = F.render(text, True, (255, 255, 255))
    WIN.blit(text_surface, (400, 475))

    pygame.display.update()

def game_over():
    run = True
    while run:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            run = False
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        text_surface = GOF.render("GAME OVER", True, (255, 255, 255))
        WIN.blit(text_surface, (350, 200))
        text_surface = F.render("press space to play again", True, (255, 255, 255))
        WIN.blit(text_surface, (310, 250))
        pygame.display.update()

def reset():
    B.x = 425
    B.y = 175
    PB.y = B.y - 10

def main():
    vmvmnt = 0
    hmvmnt = 'r'
    score = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        global SPEED
        keys = pygame.key.get_pressed()
        block_speed = SPEED // 2
        if keys[pygame.K_UP] and PB.y > 0:
            PB.y -= block_speed
        if keys[pygame.K_DOWN] and PB.y < 430:
            PB.y += block_speed

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if hmvmnt == 'r':
            B.x += SPEED
        elif hmvmnt == 'l':
            B.x -= SPEED

        B.y += vmvmnt

        if collision_check(B, PB):
            print('COLLISION')
            score += 1
            hmvmnt = 'l'

            slope = random.randint(-3, 3)
            vmvmnt = slope
            SPEED += 0.1

        if collision_check(B, GB):
            hmvmnt = 'r'
            print('COLLISION')

            slope = random.randint(-6, 6)
            vmvmnt = slope

        if collision_check(B, CIEL):
            print('CIEL')
            vmvmnt *= -1

        if collision_check(B, FLOOR):
            print('FLOOR')
            vmvmnt /= -1

        if collision_check(B, WALL_LEFT):
            print('WALL')
            hmvmnt = 'r'
            game_over()
            score = 0
            vmvmnt = 0
            reset()

        if collision_check(B, WALL_RIGHT):
            score -= 1
            print('WALL')
            hmvmnt = 'r'
            game_over()
            score = 0
            vmvmnt = 0
            reset()

        GB.y = B.y - 10

        # uncomment this line to automate positioning of the right block
        # PB.y = B.y - 10

        draw_window(score)
    pygame.quit()

if __name__ == "__main__":
    main()

