import pygame
import random
import sys

width = height = 778
border_width = 5
square_size = 32
squares_per_width = width // square_size
squares_per_height = height // square_size
north = (0, -1)
east = (1, 0)
south = (0, 1)
west = (-1, 0)


def draw_map(surface):
    pygame.draw.line(surface, (255, 0, 0), (0, 0), (0, height), border_width)
    pygame.draw.line(surface, (255, 0, 0), (0, 0), (width, 0), border_width)
    pygame.draw.line(surface, (255, 0, 0), (width, height), (0, height), border_width)
    pygame.draw.line(surface, (255, 0, 0), (width, height), (width, 0), border_width)
    for i in range(height // square_size):
        for j in range(width // square_size):
            if (i + j) % 2:
                square1 = pygame.Rect((border_width + i * square_size, border_width + j * square_size),
                                      (square_size, square_size))
                pygame.draw.rect(surface, (128, 128, 128), square1)
            else:
                square2 = pygame.Rect((border_width + i * square_size, border_width + j * square_size),
                                      (square_size, square_size))
                pygame.draw.rect(surface, (255, 255, 255), square2)


def get_random_coordinates():
    return (random.randint(0, squares_per_width - 1) * square_size,
            random.randint(0, squares_per_height - 1) * square_size)


class Target(object):
    def __init__(self):
        self.position = get_random_coordinates()
        self.color = (255, 255, 0)

    def draw(self, surface):
        square = pygame.Rect((border_width + self.position[0], border_width + self.position[1]),
                             (square_size, square_size))
        pygame.draw.rect(surface, self.color, square)
        pygame.draw.rect(surface, (255, 128, 0), square, 3)


class Snake(object):
    def __init__(self):
        self.length = 2
        self.coordinates = [((width - 2 * border_width) // 2, (height - 2 * border_width) // 2),
                            ((width - 2 * border_width) - square_size, (height - 2 * border_width) // 2)]
        self.color = (0, 204, 0)
        self.direction = random.choice([north, east, south])

    def draw(self, surface):
        for position in self.coordinates:
            square = pygame.Rect((border_width + position[0], border_width + position[1]), (square_size, square_size))
            pygame.draw.rect(surface, self.color, square)
            pygame.draw.rect(surface, (255, 0, 0), square, 3)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -1
                elif event.key == pygame.K_UP:
                    self.set_direction(north)
                elif event.key == pygame.K_RIGHT:
                    self.set_direction(east)
                elif event.key == pygame.K_DOWN:
                    self.set_direction(south)
                elif event.key == pygame.K_LEFT:
                    self.set_direction(west)
        return 1

    def set_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def get_head_coordinates(self):
        return self.coordinates[0]

    def move(self):
        head_position = self.get_head_coordinates()
        next_position = (
            head_position[0] + self.direction[0] * square_size, head_position[1] + self.direction[1] * square_size)

        if len(self.coordinates) > 2 and next_position in self.coordinates[2:] or next_position[0] < 0 or \
                next_position[0] >= width - 2 * border_width or next_position[1] < 0 or \
                next_position[1] >= height - 2 * border_width:
            return -1
        else:
            self.coordinates.insert(0, next_position)
            if len(self.coordinates) > self.length:
                self.coordinates.pop()
        return 1


def start_game(high_score):
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((width, height))
    surface = pygame.Surface(window.get_size())
    target = Target()
    snake = Snake()
    score = 0
    font = pygame.font.Font("Roboto-Medium.ttf", 20)

    while True:
        clock.tick(5)
        exit_flag = snake.handle_keys()
        if exit_flag == -1:
            break
        draw_map(surface)
        lost_flag = snake.move()
        if lost_flag == -1:
            break
        if snake.get_head_coordinates() == target.position:
            snake.length += 1
            score += 1
            target.position = get_random_coordinates()
        snake.draw(surface)
        target.draw(surface)
        window.blit(surface, (0, 0))
        score_text = font.render("Score: {0}".format(score), True, (255, 0, 0))
        window.blit(score_text, (10, 10))
        high_score_text = font.render("High score: {0}".format(high_score), True, (255, 0, 0))
        window.blit(high_score_text, (600, 10))
        exit_text = font.render("Press 'ESC' to exit", True, (255, 0, 0))
        window.blit(exit_text, (250, 10))
        pygame.display.update()

    return score


def draw_score(window, font, score, high_score):
    score_text = font.render("Score: {0}".format(score), True, (255, 128, 0))
    window.blit(score_text, (width / 2 - 300, height / 2 - 100))
    high_score_text = font.render("High score: {0}".format(high_score), True, (255, 128, 0))
    window.blit(high_score_text, (width / 2 - 300, height / 2 - 150))
    start_text = font.render("Press key 'Space' to start the game", True, (255, 128, 0))
    window.blit(start_text, (width / 2 - 300, height / 2 - 50))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((width, height))
    surface = pygame.Surface(window.get_size())
    font = pygame.font.Font("Roboto-Medium.ttf", 40)
    high_score = 0
    score = 0
    draw_score(window, font, score, high_score)
    while True:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score = start_game(high_score)
        if score > high_score:
            high_score = score
        window.blit(surface, (0, 0))
        draw_score(window, font, score, high_score)
        pygame.display.update()


main()
