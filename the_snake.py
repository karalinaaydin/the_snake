"""Игра Змейка.

Код описывает алгоритм игры, в которой змейка, съедая яблоки,
увеличивается в размере. Игра заканчивается, когда змейка
врезается сама в себя.
"""
from random import randint, choice

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
directions_list = [UP, DOWN, LEFT, RIGHT]
random_direction = choice(directions_list)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Snake')

clock = pygame.time.Clock()


class GameObject:
    """Родительский класс, описывающий все объекты игры."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализирует класс GameObject.

        Конструктор принимает на входе 2 аргумента: position, body_color.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект игры.

        Спецификации отрисовки заданны в дочерних классах.
        """


class Snake(GameObject):
    """Дочерний класс класса GameObject."""

    def __init__(self):
        """Инициализирует класс Snake."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random_direction
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        super().__init__(self.positions, self.body_color)

    def update_direction(self):
        """Обновляет текущее направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Отрисовывет объект класса."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position[0], position[1],
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last[0], self.last[1],
                                    GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты первого элемента из positions."""
        return self.positions[0]

    def move(self, apple):
        """Описывает правила движения змейки."""
        current_head = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (current_head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (current_head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        if new_head in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if new_head == apple.position:
                self.length += 1
                apple.randomize_position()
            else:
                self.last = self.positions.pop()

    def reset(self):
        """Описывает алгоритм сброса змейки в начальное состояние."""
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = 1
        self.direction = random_direction
        self.next_direction = None
        self.last = None


class Apple(GameObject):
    """Дочерний класс класса GameObject."""

    def __init__(self):
        """Инициализирует класс Apple."""
        self.body_color = APPLE_COLOR
        self.position = (0, 0)
        super().__init__(self.position, self.body_color)
        self.randomize_position()

    def randomize_position(self):
        """Возвращает случайное значение координат.

        Определяет положение яблока следующим образом:
        метод ranint возвращает случайное значение, полученное из диапозона
        значений от 0 до значения, равного ширине и высоте игрового поля -1,
        после чего полученное значение умнодается на размер клетки.
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывет объект класса."""
        rect = pygame.Rect(self.position[0], self.position[1],
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обрабатывает ввод.

    Обработка клавиш определяет направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Описывает основной игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
