import json
import pygame
import random
import sys

map_size = 778
square_size = 32
list_of_obstacles = None
if len(sys.argv) == 2:
    f = open(sys.argv[1], "r")
    data = json.loads(f.read())
    map_size = data["map_size"]
    list_of_obstacles = data["obstacle_coordinates"]
    for elem in range(len(list_of_obstacles)):
        x = int(list_of_obstacles[elem][0]) * square_size
        y = int(list_of_obstacles[elem][1]) * square_size
        list_of_obstacles[elem] = (x, y)

width = height = int(map_size)
border_width = 5
square_size = 32
squares_per_width = width // square_size
squares_per_height = height // square_size
north = (0, -1)
east = (1, 0)
south = (0, 1)
west = (-1, 0)


def draw_map(surface):
    """Aceasta functie este apelata in bucla "while" a jocului pentru a redesena la fiecare frame tabla de joc formata
    din patratele albe si gri alternate ca pe tabla de sah pentru a fi mai usor de inteles distantele din joc.
    Tabla are si niste granite rosii care nu trebuie atinse de catre jucator.
    :param surface: suprafata de joc
    """

    pygame.draw.line(surface, (255, 0, 0), (0, 0), (0, height), border_width)
    pygame.draw.line(surface, (255, 0, 0), (0, 0), (width, 0), border_width)
    pygame.draw.line(surface, (255, 0, 0), (width, height), (0, height), border_width)
    pygame.draw.line(surface, (255, 0, 0), (width, height), (width, 0), border_width)
    for i in range(height // square_size):
        for j in range(width // square_size):
            if (i + j) % 2:
                square1 = pygame.Rect((border_width + i * square_size, border_width + j * square_size),
                                      (square_size, square_size))
                pygame.draw.rect(surface, (224, 224, 224), square1)
            else:
                square2 = pygame.Rect((border_width + i * square_size, border_width + j * square_size),
                                      (square_size, square_size))
                pygame.draw.rect(surface, (255, 255, 255), square2)


def get_random_coordinates():
    """Functia aceasta returneaza o tupla formata din doua coordonate care reprezinta un patratel de pe tabla.
    :return: tupla cu 2 coordonate spatiale random
    """
    return (random.randint(0, squares_per_width - 1) * square_size,
            random.randint(0, squares_per_height - 1) * square_size)


def randomise_position(obstacles):
    """Aceasta functie apeleaza functia "get_random_coordinates()" asigurandu-se ca returneaza o pozitie neocupata de
    obstacole.
    :param obstacles: lista de pozitii ocupate
    :return: tupla cu 2 coordonate spatiale care nu se suprapun cu un obstacol
    """
    pos = get_random_coordinates()
    while pos in obstacles:
        pos = get_random_coordinates()
    return pos


class Target(object):
    """Aceasta clasa reprezinta patratelul la care trebuie sa ajunga sarpele pentru a avansa in cadrul jocului si
    pentru a strange un scor cat mai mare. Clasa este formata dintr-o tupla "position" si o tupla "color", ambele
    folosite in metoda "draw" cu ajutorul careia jucatorul poate vedea unde trebuie sa ajunga pe tabla de joc.
    """

    def __init__(self, obstacles):
        self.position = randomise_position(obstacles)
        self.color = (255, 255, 0)

    def draw(self, surface):
        square = pygame.Rect((border_width + self.position[0], border_width + self.position[1]),
                             (square_size, square_size))
        pygame.draw.rect(surface, self.color, square)
        pygame.draw.rect(surface, (255, 128, 0), square, 3)


class Snake(object):
    """Clasa aceasta reprezinta avatarul jucatorului si este formata dintr-un intreg "length" (lungimea sarpelui in
    patratele de pe tabla), "coordinates" o lista de tuple care reprezinta pozitiile corpului si se comporta ca o
    coada si "direction" care reprezinta directia de deplasare a sarpelui.
    """

    def __init__(self):
        self.length = 2
        self.coordinates = [((width - 2 * border_width) // 2, (height - 2 * border_width) // 2),
                            ((width - 2 * border_width) - square_size, (height - 2 * border_width) // 2)]
        self.color = (0, 204, 0)
        self.direction = random.choice([north, east, south])

    def draw(self, surface):
        """Metoda aceasta este apelata in bucla "while" a jocului si deseneaza un patratel pe tabla pentru fiecare
        tupla din lista "coordinates".
        :param surface: suprafata de joc
        """
        for position in self.coordinates:
            square = pygame.Rect((border_width + position[0], border_width + position[1]), (square_size, square_size))
            pygame.draw.rect(surface, self.color, square)
            pygame.draw.rect(surface, (255, 0, 0), square, 3)

    def handle_keys(self):
        """Metoda "handle_keys()" asociaza tasta "ESC" iesirii din joc si tastele "UP","RIGHT","DOWN","LEFT" cu
        directiile in care se poate deplasa sarpele.
        :return: -1 pentru oprirea jocului sau 1 in caz contrar
        """
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
        """Metoda "set_direction()" actualizeaza directioa de deplasare a sarpelui si nu permite
        deplasarea intr-un sens invers al directiei curente.
        :param direction:
        """
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def get_head_coordinates(self):
        """Metoda aceasta returneaza prima pozitie din lista de coordonate a sarpelui.
        :return: tupla cu 2 coordoante spatiale
        """
        return self.coordinates[0]

    def move(self, obstacles):
        """Aceasta metoda actualizeaza lista de coordonate ale sarpelui cu un pas inainte in functie de directia de
        miscare.
        :param obstacles: lista de pozitii in care se afla obstacole
        :return: -1 daca a pierdut, 1 in caz contrar
        """
        head_position = self.get_head_coordinates()
        next_position = (
            head_position[0] + self.direction[0] * square_size, head_position[1] + self.direction[1] * square_size)

        if len(self.coordinates) > 2 and next_position in self.coordinates[2:] or next_position in obstacles or \
                next_position[0] < 0 or next_position[0] >= width - 2 * border_width or next_position[1] < 0 or \
                next_position[1] >= height - 2 * border_width:
            return -1
        else:
            self.coordinates.insert(0, next_position)
            if len(self.coordinates) > self.length:
                self.coordinates.pop()
        return 1


class Obstacles(object):
    """Clasa "Obstacles" reprezinta patratele pe care sarpele trebuie sa le evite si este formata dintr-o lista de
    pozitii  si o tupla RGB pentru culoare.
    """

    def __init__(self, obstacles=None):
        if obstacles is None:
            obstacles = [get_random_coordinates() for _ in range(12)]
        self.positions = [obstacles[i] for i in range(len(obstacles))]
        self.color = (255, 0, 0)

    def draw(self, surface):
        """Aceasta metoda deseneaza patratelele care trebuie evitate pe tabla de joc.
        :param surface: suprafata de joc
        """
        for position in self.positions:
            square = pygame.Rect((border_width + position[0], border_width + position[1]),
                                 (square_size, square_size))
            pygame.draw.rect(surface, self.color, square)
            pygame.draw.rect(surface, (255, 128, 0), square, 3)


def start_game(high_score):
    """Aceasta functie reprezinta partida de joc in sine.
    :param high_score: un intreg reprezentand cel mai mare scor obtinut din toate partidele pana in rpezent
    :return: un intreg reprezentand scorul obtinut in partida curenta
    """
    pygame.init()
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((width, height))
    surface = pygame.Surface(window.get_size())
    obstacles = Obstacles(list_of_obstacles)
    snake = Snake()
    target = Target(obstacles.positions + snake.coordinates)
    score = 0
    font = pygame.font.Font("Roboto-Medium.ttf", 20)

    while True:
        clock.tick(5)
        exit_flag = snake.handle_keys()
        if exit_flag == -1:
            break
        draw_map(surface)
        obstacles.draw(surface)
        lost_flag = snake.move(obstacles.positions)
        if lost_flag == -1:
            break
        if snake.get_head_coordinates() == target.position:
            snake.length += 1
            score += 1
            target.position = randomise_position(obstacles.positions + snake.coordinates)
        snake.draw(surface)
        target.draw(surface)
        window.blit(surface, (0, 0))
        score_text = font.render("Score: {0}".format(score), True, (0, 0, 0))
        window.blit(score_text, (10, 10))
        high_score_text = font.render("High score: {0}".format(high_score), True, (0, 0, 0))
        window.blit(high_score_text, (600, 10))
        exit_text = font.render("Press 'ESC' to exit", True, (0, 0, 0))
        window.blit(exit_text, (250, 10))
        pygame.display.update()

    return score


def draw_score(window, font, score, high_score):
    """Aceasta functie afiseaza scorul, high score-ul si "Press key 'Space' to start the game" in meniul principal al
    jocului.
    """
    score_text = font.render("Score: {0}".format(score), True, (255, 128, 0))
    window.blit(score_text, (width / 2 - 300, height / 2 - 100))
    high_score_text = font.render("High score: {0}".format(high_score), True, (255, 128, 0))
    window.blit(high_score_text, (width / 2 - 300, height / 2 - 150))
    start_text = font.render("Press key 'Space' to start the game", True, (255, 128, 0))
    window.blit(start_text, (width / 2 - 300, height / 2 - 50))


def main():
    """Aceasta functie deschide meniul principal al jocului.
    """
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
