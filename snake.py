import os
import pygame
import random
from enum import Enum

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TILE_SIZE = 32
GRID_WIDTH = WINDOW_WIDTH // TILE_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // TILE_SIZE

class SpriteDirection(Enum):
    HEAD_UP = 1
    HEAD_DOWN = 2
    HEAD_LEFT = 3
    HEAD_RIGHT = 4
    TAIL_UP = 5
    TAIL_DOWN = 6
    TAIL_LEFT = 7
    TAIL_RIGHT = 8
    BODY_VERTICAL = 9
    BODY_HORIZONTAL = 10
    BODY_TOP_LEFT = 11
    BODY_TOP_RIGHT = 12
    BODY_BOTTOM_LEFT = 13
    BODY_BOTTOM_RIGHT = 14

class io_handler:
    def __init__(self):
        self.last_input = 'w'

        start_x = (GRID_WIDTH // 2) * TILE_SIZE
        start_y = (GRID_HEIGHT // 2) * TILE_SIZE
        self.snake = [(start_x, start_y), (start_x - TILE_SIZE, start_y)]

        self.gerar_nova_fruta()

    def aligned(self, pos):
        return (pos[0] // TILE_SIZE, pos[1] // TILE_SIZE)

    def move_snake(self):
        if len(self.snake) == 0:
            return
        
        hx, hy = self.snake[0]

        if self.last_input == 'w':
            nova_cabeca = (hx, WINDOW_HEIGHT - TILE_SIZE if hy <= 0 else hy - TILE_SIZE)
        elif self.last_input == 'a':
            nova_cabeca = (WINDOW_WIDTH - TILE_SIZE if hx <= 0 else hx - TILE_SIZE, hy)
        elif self.last_input == 's':
            nova_cabeca = (hx, 0 if hy >= WINDOW_HEIGHT - TILE_SIZE else hy + TILE_SIZE)
        elif self.last_input == 'd':
            nova_cabeca = (0 if hx >= WINDOW_WIDTH - TILE_SIZE else hx + TILE_SIZE, hy)
        else:
            nova_cabeca = (hx, hy)

        self.snake.insert(0, nova_cabeca)

        if self.aligned(nova_cabeca) == self.aligned(self.fruit):
            self.gerar_nova_fruta()
        else:
            self.snake.pop()

    def change_direction(self, direction):
        if (self.last_input == 'w' and direction != 's') or \
           (self.last_input == 's' and direction != 'w') or \
           (self.last_input == 'a' and direction != 'd') or \
           (self.last_input == 'd' and direction != 'a'):
            self.last_input = direction
            
    def direction_between(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2

        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) > WINDOW_WIDTH // 2:
            dx = -dx

        if abs(dy) > WINDOW_HEIGHT // 2:
            dy = -dy

        if dx > 0:
            return 'd'
        elif dx < 0:
            return 'a'
        elif dy > 0:
            return 's'
        else:
            return 'w'

    def is_pair(self,a,b,d1,d2):
        return (d1 == a and d2 == b) or (d1 == b and d2 == a)

    def gerar_nova_fruta(self):
        while True:
            nova_fruta = (
                random.randrange(0, WINDOW_WIDTH, TILE_SIZE),
                random.randrange(0, WINDOW_HEIGHT, TILE_SIZE),
            )
            
            if nova_fruta not in self.snake:
                self.fruit = nova_fruta
                break

    def check_game_over(self):
        head = self.snake[0]
        if head in self.snake[1:]:
            self.last_input = 'end'
            if pygame.get_init() and pygame.display.get_init():
                try:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                except Exception:
                    pass
            print("Game Over! A cobra colidiu consigo mesma.")

    def get_sprite(self, i):
        length = len(self.snake)

        if i == 0:
            dir = self.direction_between(self.snake[1], self.snake[0])
            if dir == 'w': return SpriteDirection.HEAD_UP
            elif dir == 'a': return SpriteDirection.HEAD_LEFT
            elif dir == 's': return SpriteDirection.HEAD_DOWN
            else: return SpriteDirection.HEAD_RIGHT

        if i == length - 1:
            dir = self.direction_between(self.snake[length - 2], self.snake[length - 1])
            if dir == 'w': return SpriteDirection.TAIL_UP
            elif dir == 'a': return SpriteDirection.TAIL_LEFT
            elif dir == 's': return SpriteDirection.TAIL_DOWN
            else: return SpriteDirection.TAIL_RIGHT

        prev = self.snake[i - 1]
        curr = self.snake[i]
        next = self.snake[i + 1]

        d1 = self.direction_between(curr, prev)
        d2 = self.direction_between(curr, next)

        if self.is_pair('w', 's', d1, d2):
            return SpriteDirection.BODY_VERTICAL
        elif self.is_pair('a', 'd', d1, d2):
            return SpriteDirection.BODY_HORIZONTAL
        elif self.is_pair('w', 'd', d1, d2):
            return SpriteDirection.BODY_TOP_RIGHT
        elif self.is_pair('w', 'a', d1, d2):
            return SpriteDirection.BODY_TOP_LEFT
        elif self.is_pair('s', 'd', d1, d2):
            return SpriteDirection.BODY_BOTTOM_RIGHT
        else:
            return SpriteDirection.BODY_BOTTOM_LEFT
    
    def ret_right_sprite(self, i):
        sprite = self.get_sprite(i)
        return SPRITES[sprite]


def game_loop():
    global SPRITES

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    SPRITES = {
        SpriteDirection.HEAD_UP: pygame.image.load('./Graphics/head_up.png').convert_alpha(),
        SpriteDirection.HEAD_DOWN: pygame.image.load('./Graphics/head_down.png').convert_alpha(),
        SpriteDirection.HEAD_LEFT: pygame.image.load('./Graphics/head_left.png').convert_alpha(),
        SpriteDirection.HEAD_RIGHT: pygame.image.load('./Graphics/head_right.png').convert_alpha(),
        SpriteDirection.TAIL_UP: pygame.image.load('./Graphics/tail_up.png').convert_alpha(),
        SpriteDirection.TAIL_DOWN: pygame.image.load('./Graphics/tail_down.png').convert_alpha(),
        SpriteDirection.TAIL_LEFT: pygame.image.load('./Graphics/tail_left.png').convert_alpha(),
        SpriteDirection.TAIL_RIGHT: pygame.image.load('./Graphics/tail_right.png').convert_alpha(),
        SpriteDirection.BODY_VERTICAL: pygame.image.load('./Graphics/body_vertical.png').convert_alpha(),
        SpriteDirection.BODY_HORIZONTAL: pygame.image.load('./Graphics/body_horizontal.png').convert_alpha(),
        SpriteDirection.BODY_TOP_LEFT: pygame.image.load('./Graphics/body_topleft.png').convert_alpha(),
        SpriteDirection.BODY_TOP_RIGHT: pygame.image.load('./Graphics/body_topright.png').convert_alpha(),
        SpriteDirection.BODY_BOTTOM_LEFT: pygame.image.load('./Graphics/body_bottomleft.png').convert_alpha(),
        SpriteDirection.BODY_BOTTOM_RIGHT: pygame.image.load('./Graphics/body_bottomright.png').convert_alpha(),
    }

    food_img = pygame.image.load('./Graphics/apple.png').convert_alpha()

    instance = io_handler()
    running = True

    while running:
        screen.fill((0, 0, 0))

        # desenhar comida
        screen.blit(food_img, instance.fruit)

        # desenhar cobra
        for i in range(len(instance.snake)):
            x, y = instance.snake[i]
            sprite = instance.ret_right_sprite(i)
            screen.blit(sprite, (x, y))

        instance.move_snake()
        instance.check_game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    instance.change_direction('w')
                elif event.key == pygame.K_a:
                    instance.change_direction('a')
                elif event.key == pygame.K_s:
                    instance.change_direction('s')
                elif event.key == pygame.K_d:
                    instance.change_direction('d')
                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()
        clock.tick(10) #velocidade da cobra

    pygame.quit()


if __name__ == "__main__":
    game_loop()