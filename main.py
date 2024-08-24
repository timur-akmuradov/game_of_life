import pygame
from sys import exit
from random import randint

pygame.init()

screen = pygame.display.set_mode((0, 0))

clock = pygame.time.Clock()

infoObject = pygame.display.Info()

# Разрешение окна
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Размер ячейки
GRID_SIZE = 6

# Размер игровой сетки
GRID_WIDTH = int((infoObject.current_w -
                  (infoObject.current_w * 0.15)) // GRID_SIZE)
GRID_HEIGHT = infoObject.current_h // GRID_SIZE

# Цвета
BLACK = (0, 0, 0)
GREY = (178, 178, 178)
WHITE = (255, 255, 255)

# Частота кадров
FPS = 20

# Информационные строки
HELP_TXT = ["Space - Pause / Continue", "R - Randomize cells",
            "C - To clean field", "ESC - To quit the game"]

# Количество живых клеток в соотношении к разрешению окна
CELLS = int((SCREEN_WIDTH + SCREEN_HEIGHT) * 2)


class Game:
    """Основной класс игры."""
    field: list
    toggle: bool
    cells: int

    def __init__(self) -> None:
        self.restart()

    def get_neighbours_count(self, x, y) -> int:
        """Считает количество живых соседей у переданной клетки."""
        count = 0

        # Диапазоны для поиска вокруг переданной клетки
        xrange = [x-1, x, x+1]
        yrange = [y-1, y, y+1]

        # Поиск по диапазонам вокруг клетки
        for x1 in xrange:
            for y1 in yrange:
                # Пропускаем текущую клетку
                if x1 == x and y1 == y:
                    continue
                try:
                    # Если соседняя клетка живая - увеличиваем счетчик
                    if self.field[x1][y1] == 1:
                        count += 1
                # Обработка исключения, если индекс вне списка
                except IndexError:
                    count = 0
                    continue
        return count

    def set_random_positions(self) -> None:
        """Устанавливает живые клетки в случайных позициях."""
        for _ in range(self.cells):
            rand_x = randint(0, GRID_HEIGHT - 1)
            rand_y = randint(0, GRID_WIDTH - 1)
            self.field[rand_x][rand_y] = 1

    def update_field(self) -> None:
        """Обновляет игровую сетку в соответствии с правилами игры."""

        # Создаем новое игровое поле, для одновременного обновления всех клеток
        new_field = [[0 for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]

        # Проходимся по всему игровому полю
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                # Передаем количество живых соседей текущей клетки
                neighbors = self.get_neighbours_count(x, y)
                if self.field[x][y] == 1:
                    if neighbors < 2:
                        new_field[x][y] = 0
                    elif neighbors == 2 or neighbors == 3:
                        new_field[x][y] = 1
                    elif neighbors > 3:
                        new_field[x][y] = 0
                else:
                    if neighbors == 3:
                        new_field[x][y] = 1
        # Обновляем игровое поле
        self.field = new_field

    def clear(self) -> None:
        """Очищает игровое поле."""
        self.field = [[0 for _ in range(GRID_WIDTH)]
                      for _ in range(GRID_HEIGHT)]
        self.toggle = False
        self.cells = 0

    def restart(self) -> None:
        """Перезагружает игровое поле с новыми живыми клетками."""
        self.clear()
        self.cells = CELLS
        self.set_random_positions()

    def draw(self) -> None:
        """Отрисовка клеток на игровом поле."""
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                position = (y * GRID_SIZE, x * GRID_SIZE)
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                if self.field[x][y] == 0:
                    pygame.draw.rect(screen, WHITE, rect)
                elif self.field[x][y] == 1:
                    pygame.draw.rect(screen, BLACK, rect)


def handle_keys(game) -> None:
    """Обрабатывает нажатия клавиш пользователем."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.toggle = not game.toggle
            elif event.key == pygame.K_r:
                game.restart()
            elif event.key == pygame.K_c:
                game.clear()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


def draw_gui() -> None:
    """Отрисовка игрового интерфейса."""
    pygame.init()
    pygame.font.init()

    screen.fill(GREY)

    path = pygame.font.match_font("times new roman")
    Font = pygame.font.Font(path, 25)
    pos_x = int(SCREEN_WIDTH - (SCREEN_WIDTH * 0.14))

    help_line_1 = Font.render(HELP_TXT[0], 1, BLACK)
    help_line_2 = Font.render(HELP_TXT[1], 1, BLACK)
    help_line_3 = Font.render(HELP_TXT[2], 1, BLACK)
    help_line_4 = Font.render(HELP_TXT[3], 1, BLACK)

    screen.blit(help_line_1, (pos_x, 50))
    screen.blit(help_line_2, (pos_x, 100))
    screen.blit(help_line_3, (pos_x, 150))
    screen.blit(help_line_4, (pos_x, 200))


def main() -> None:
    game = Game()

    draw_gui()

    # Основной игровой цикл
    while True:
        handle_keys(game)
        game.draw()
        pygame.display.update()

        # Цикл текущего поколения клеток
        while game.toggle:
            clock.tick(FPS)
            game.draw()
            game.update_field()
            handle_keys(game)
            pygame.display.update()


if __name__ == '__main__':
    main()
