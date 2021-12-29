import pygame
import random

width = 768
height = 768
square_size = 32
squares_per_width = width // square_size
squares_per_height = height // square_size


def draw_map(surface):
    for i in range(height):
        for j in range(width):
            if (i + j) % 2:
                square1 = pygame.Rect((i * square_size, j * square_size), (square_size, square_size))
                pygame.draw.rect(surface, (128, 128, 128), square1)
            else:
                square2 = pygame.Rect((i * square_size, j * square_size), (square_size, square_size))
                pygame.draw.rect(surface, (255, 255, 255), square2)


def random_coordinates():
    return (random.randint(0, squares_per_width - 1) * square_size,
            random.randint(0, squares_per_height - 1) * square_size)


class Target(object):
    def __init__(self):
        self.position = random_coordinates()
        self.color = (255, 255, 0)

    def draw(self, surface):
        square = pygame.Rect((self.position[0], self.position[1]), (square_size, square_size))
        pygame.draw.rect(surface, self.color, square)
        pygame.draw.rect(surface, (255, 128, 0), square, 3)


class Snake(object):
    def __init__(self):
        self.length = 2
        self.coordinates = [(width / 2, height / 2), (width / 2 - square_size, height / 2)]
        self.color = (0, 204, 0)

    def draw(self, surface):
        for position in self.coordinates:
            square = pygame.Rect((position[0], position[1]), (square_size, square_size))
            pygame.draw.rect(surface, self.color, square)
            pygame.draw.rect(surface, (255, 0, 0), square, 3)


def start_game():
    pygame.init()
    window = pygame.display.set_mode((width, height))
    surface = pygame.Surface(window.get_size())
    target = Target()
    snake = Snake()

    while True:
        draw_map(surface)
        snake.draw(surface)
        target.draw(surface)
        window.blit(surface, (0, 0))
        pygame.display.update()


start_game()
