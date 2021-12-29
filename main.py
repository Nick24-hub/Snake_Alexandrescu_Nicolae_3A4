import pygame

width = 768
height = 768
square_size = 32

def draw_map(surface):
    for i in range(height):
        for j in range(width):
            if (i + j) % 2:
                square1 = pygame.Rect((i * square_size, j * square_size), (square_size, square_size))
                pygame.draw.rect(surface, (0, 0, 0), square1)
            else:
                square2 = pygame.Rect((i * square_size, j * square_size), (square_size, square_size))
                pygame.draw.rect(surface, (255, 255, 255), square2)


def start_game():
    pygame.init()
    window = pygame.display.set_mode((width, height))
    surface = pygame.Surface(window.get_size())


    while True:
        draw_map(surface)
        window.blit(surface, (0, 0))
        pygame.display.update()

start_game()
