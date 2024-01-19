from random import randint

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

    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    body_color = (0, 0, 0)

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализирует класс GameObject,
        принимает на входе 2 аргумента: position, body_color
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект игры.
        Спецификации отрисовки заданны в дочерних классах.
        """
        pass


class Snake(GameObject):
    """Дочерний класс класса GameObject."""

    length = 1
    positions = [(0, 0)]
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)
    last = None

    def __init__(self):
        """Инициализирует класс Snake."""
        super().__init__((0, 0), (0, 255, 0))

    def update_direction(self):
        """Обновляет текущее направление дивжения объекта класса
        на заданное новое.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Отрисовывет объект класса."""
        for position in self.positions[:-1]:
            rect = pygame.Rect((position[0], position[1]),
                               (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect((self.last[0], self.last[1]),
                                    (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты первого элемента списка positions
        (головы змейки).
        """
        return self.positions[0]

    def move(self, apple):
        """Описывает правила "движения" змейки"""
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

            if new_head[0] < 0:
                new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
            elif new_head[0] >= SCREEN_WIDTH:
                new_head = (0, new_head[1])
            elif new_head[1] < 0:
                new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
            elif new_head[1] >= SCREEN_HEIGHT:
                new_head = (new_head[0], 0)

            self.positions[0] = new_head

    def reset(self):
        """Описывает алгоритм сброса змейки в начальное состояние"""
        self.positions = [(0, 0)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


class Apple(GameObject):
    """Дочерний класс класса GameObject."""

    body_color = (255, 0, 0)
    position = (0, 0)

    def randomize_position(self):
        """Возвращает случайное значение координат -
        определяет положение яблока.
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def __init__(self):
        """Инициализирует класс Apple."""
        super().__init__((0, 0), (255, 0, 0))
        self.randomize_position()

    def draw(self, surface):
        """Отрисовывет объект класса."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit


if __name__ == '__main__':
    main()
