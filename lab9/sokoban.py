import pygame, sys, os
from pygame.locals import *

# ─── Вспомогательные функции ──────────────────────────────────────
def get_offset(d, w):
    """Смещение в карте для указанного направления"""
    if d == 'l':   # left
        return -1
    elif d == 'r': # right
        return 1
    elif d == 'u': # up
        return -w
    elif d == 'd': # down
        return w
    return 0

def move_man(level, pos):
    """Переместить игрока на позицию pos"""
    if level[pos] == '-':
        level[pos] = '@'
    elif level[pos] == '.':
        level[pos] = '+'

def move_floor(level, pos):
    """Вернуть клетке вид пола (пустого или целевого)"""
    if level[pos] in ('@', '+'):
        level[pos] = '.' if level[pos] == '+' else '-'

def move_box(level, pos):
    """Поместить ящик на позицию pos"""
    if level[pos] == '-':
        level[pos] = '$'
    elif level[pos] == '.':
        level[pos] = '*'

# ─── Класс игры ───────────────────────────────────────────────────
class Sokoban:
    def __init__(self):
        # Карта уровня: 19 столбцов x 11 строк
        self.level = list(
            "----#####----------"
            "----#---#----------"
            "----#$--#----------"
            "--###--$##---------"
            "--#--$-$-#---------"
            "###-#-##-#---######"
            "#---#-##-#####--..#"
            "#-$--$----------..#"
            "#####-###-#@##--..#"
            "----#-----#########"
            "----#######--------")
        self.w = 19          # ширина в клетках
        self.h = 11          # высота в клетках
        self.man = 163       # начальная позиция игрока (индекс в списке)
        self.solution = []   # история ходов (для undo)
        self.todo = []       # отменённые ходы (для redo)
        self.push = 0        # счётчик толканий ящика

    def draw(self, screen, skin):
        """Отрисовка уровня"""
        w = skin.get_width() // 4   # ширина одного спрайта
        for i in range(self.w):
            for j in range(self.h):
                item = self.level[j * self.w + i]
                # Стена
                if item == '#':
                    screen.blit(skin, (i * w, j * w), (0, 2 * w, w, w))
                # Пустое место
                elif item == '-':
                    screen.blit(skin, (i * w, j * w), (0, 0, w, w))
                # Игрок
                elif item == '@':
                    screen.blit(skin, (i * w, j * w), (w, 0, w, w))
                # Ящик
                elif item == '$':
                    screen.blit(skin, (i * w, j * w), (2 * w, 0, w, w))
                # Цель
                elif item == '.':
                    screen.blit(skin, (i * w, j * w), (0, w, w, w))
                # Игрок на цели
                elif item == '+':
                    screen.blit(skin, (i * w, j * w), (w, w, w, w))
                # Ящик на цели
                elif item == '*':
                    screen.blit(skin, (i * w, j * w), (2 * w, w, w, w))

    def _move(self, d):
        """Выполнить движение в направлении d ('l','r','u','d')"""
        h = get_offset(d, self.w)
        target = self.man + h

        # Простое перемещение игрока (пустая клетка или цель)
        if self.level[target] in ('-', '.'):
            move_man(self.level, target)
            move_floor(self.level, self.man)
            self.man = target
            self.solution.append(d)

        # Толкание ящика
        elif self.level[target] in ('$', '*'):
            h2 = h * 2
            target2 = self.man + h2
            if self.level[target2] in ('-', '.'):
                move_box(self.level, target2)
                move_floor(self.level, target)   # очищаем старую позицию ящика
                move_man(self.level, target)
                move_floor(self.level, self.man)
                self.man = target
                self.solution.append(d.upper())  # заглавная буква – ход с толканием
                self.push += 1

    def undo(self):
        """Отменить последний ход"""
        if not self.solution:
            return
        self.todo.append(self.solution[-1])
        last_move = self.solution.pop()
        h = get_offset(last_move.lower(), self.w) * -1  # обратное смещение

        if last_move.islower():   # ход без ящика
            move_man(self.level, self.man + h)
            move_floor(self.level, self.man)
            self.man += h
        else:                     # ход с ящиком
            move_floor(self.level, self.man - h)        # очищаем позицию за ящиком
            move_box(self.level, self.man)              # возвращаем ящик на место
            move_man(self.level, self.man + h)          # перемещаем игрока
            self.man += h
            self.push -= 1

    def redo(self):
        """Повторить отменённый ход"""
        if not self.todo:
            return
        move = self.todo.pop()
        self._move(move.lower())

# ─── Основной код ─────────────────────────────────────────────────
def main():
    pygame.init()

    # Загружаем изображение спрайтов
    skinfile = os.path.join('borgar.png')
    try:
        skin = pygame.image.load(skinfile)
    except pygame.error as e:
        print('Ошибка загрузки файла', skinfile)
        raise SystemExit(e)

    # Вычисляем размеры окна на основе карты и размера тайла
    tile_w = skin.get_width() // 4   # предполагаем спрайт-лист 4 столбца
    tile_h = skin.get_height() // 3  # если 3 строки; если 1 строка – поделить на 1
    win_w = 19 * tile_w
    win_h = 11 * tile_h

    # Создаём окно (convert можно делать только после этого)
    screen = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption('Sokoban')

    # Оптимизируем спрайт под формат окна
    skin = skin.convert()

    # Создаём экземпляр игры
    game = Sokoban()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 50)

    # Главный игровой цикл
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    game._move('l')
                elif event.key == K_UP:
                    game._move('u')
                elif event.key == K_RIGHT:
                    game._move('r')
                elif event.key == K_DOWN:
                    game._move('d')
                elif event.key == K_BACKSPACE:
                    game.undo()
                elif event.key == K_SPACE:
                    game.redo()

        # Фон – цвет левого верхнего пикселя спрайт-листа
        screen.fill(skin.get_at((0, 0)))
        game.draw(screen, skin)
        pygame.display.flip()

if __name__ == '__main__':
    main()