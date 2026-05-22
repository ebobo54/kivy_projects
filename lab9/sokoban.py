import pygame, sys, os
from pygame.locals import *

def get_offset(d, w):
    """Смещение в карте для указанного направления"""
    if d == 'l':
        return -1
    elif d == 'r':
        return 1
    elif d == 'u':
        return -w
    elif d == 'd':
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

class Sokoban:
    def __init__(self):
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
        self.w = 19
        self.h = 11
        self.man = 163
        self.solution = []
        self.todo = []
        self.push = 0 

    def draw(self, screen, skin):
        """Отрисовка уровня"""
        w = skin.get_width() // 4
        for i in range(self.w):
            for j in range(self.h):
                item = self.level[j * self.w + i]
                if item == '#':
                    screen.blit(skin, (i * w, j * w), (0, 2 * w, w, w))
                elif item == '-':
                    screen.blit(skin, (i * w, j * w), (0, 0, w, w))
                elif item == '@':
                    screen.blit(skin, (i * w, j * w), (w, 0, w, w))
                elif item == '$':
                    screen.blit(skin, (i * w, j * w), (2 * w, 0, w, w))
                elif item == '.':
                    screen.blit(skin, (i * w, j * w), (0, w, w, w))
                elif item == '+':
                    screen.blit(skin, (i * w, j * w), (w, w, w, w))
                elif item == '*':
                    screen.blit(skin, (i * w, j * w), (2 * w, w, w, w))

    def _move(self, d):
        """Выполнить движение в направлении d ('l','r','u','d')"""
        h = get_offset(d, self.w)
        target = self.man + h

        if self.level[target] in ('-', '.'):
            move_man(self.level, target)
            move_floor(self.level, self.man)
            self.man = target
            self.solution.append(d)

        elif self.level[target] in ('$', '*'):
            h2 = h * 2
            target2 = self.man + h2
            if self.level[target2] in ('-', '.'):
                move_box(self.level, target2)
                move_floor(self.level, target)
                move_man(self.level, target)
                move_floor(self.level, self.man)
                self.man = target
                self.solution.append(d.upper())
                self.push += 1

    def undo(self):
        """Отменить последний ход"""
        if not self.solution:
            return
        self.todo.append(self.solution[-1])
        last_move = self.solution.pop()
        h = get_offset(last_move.lower(), self.w) * -1 

        if last_move.islower(): 
            move_man(self.level, self.man + h)
            move_floor(self.level, self.man)
            self.man += h
        else:
            move_floor(self.level, self.man - h)
            move_box(self.level, self.man)
            move_man(self.level, self.man + h)
            self.man += h
            self.push -= 1

    def redo(self):
        """Повторить отменённый ход"""
        if not self.todo:
            return
        move = self.todo.pop()
        self._move(move.lower())

def main():
    pygame.init()

    skinfile = os.path.join('borgar.png')
    try:
        skin = pygame.image.load(skinfile)
    except pygame.error as e:
        print('Ошибка загрузки файла', skinfile)
        raise SystemExit(e)

    tile_w = skin.get_width() // 4 
    tile_h = skin.get_height() // 3
    win_w = 19 * tile_w
    win_h = 11 * tile_h

    screen = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption('Sokoban')

    skin = skin.convert()

    game = Sokoban()
    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 50)

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

        screen.fill(skin.get_at((0, 0)))
        game.draw(screen, skin)
        pygame.display.flip()

if __name__ == '__main__':
    main()