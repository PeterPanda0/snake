from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()

# Цвет игровых объектов
APPLE_COLOR = (200, 0, 0)
SNAKE_COLOR = (0, 200, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс описывает общие атрибуты игровых объектов."""

    def __init__(self, body_color=SNAKE_COLOR):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self, surface, position):
        """Метод рисует объект на игрвой поверхности."""
        rect = pygame.Rect(
            (position[0], position[1]), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс описывает объект - яблоко."""

    def __init__(self, busy_positions=None):
        """:type param: list"""
        busy_positions = [] if busy_positions is None else busy_positions
        super().__init__(APPLE_COLOR)
        self.randomize_position(busy_positions)

    def randomize_position(self, positions=None):
        """Устанавливает случайное значение для яблока."""
        """:type positions: list"""
        positions = [] if positions is None else positions
        if len(positions) == GRID_WIDTH * GRID_HEIGHT:
            pygame.quit()
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 10) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 10) * GRID_SIZE
            )
            if new_position not in positions:
                break
        self.position = new_position

    def draw(self, surface):
        """Отрисовка яблока."""
        super().draw(surface, self.position)


class Snake(GameObject):
    """Дочерний класс описывает объект - змейку."""

    def __init__(self):
        super().__init__()
        self.positions = [self.position]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        self.head = self.get_head_position()
        self.positions.insert(
            0,
            ((self.head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
             (self.head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT))
        self.last = self.positions.pop(-1)

    #  Метод draw класса Snake
    def draw(self, surface):
        """Отрисовка змейки."""
        # Отрисовка головы
        super().draw(surface, self.positions[0])
        # Отрисовка хвоста
        super().draw(surface, self.positions[-1])
        # Затирание последнего сегмента
        if self.last:
            rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку на начальную позицию."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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
    """Объявление экземпляров, бесконечный цикл игры."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            snake.positions.insert(0, apple.position)
            apple.randomize_position(snake.positions)

        if snake.positions[0] in snake.positions[2:]:
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
