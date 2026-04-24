from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import *

class Cell(Widget):
    graphical_size = ListProperty([1, 1])
    graphical_pos = ListProperty([1, 1])

    def __init__(self, x, y, size, margin=4):
        super().__init__()
        self.actual_size = (size, size)
        self.graphical_size = (size - margin, size - margin)
        self.margin = margin
        self.actual_pos = (x, y)
        self.graphical_pos_attach()

    def graphical_pos_attach(self):
        self.graphical_pos = (self.actual_pos[0] - self.graphical_size[0] / 2, self.actual_pos[1] - self.graphical_size[1] / 2)

    def move_to(self, x, y):
        self.actual_pos = (x, y)
        self.graphical_pos_attach()

    def move_by(self, x, y, **kwargs):
        self.move_to(self.actual_pos[0] + x, self.actual_pos[1] + y, **kwargs)

    def get_pos(self):
        return self.actual_pos

    def step_by(self, direction, **kwargs):
        self.move_by(self.actual_size[0] * direction[0], self.actual_size[1] * direction[1], **kwargs)


class Form(Widget):
    def __init__(self, config):
        super().__init__()
        self.cells = []
        self.config = config
        self.worm = None

    def start(self):
        self.worm = Worm(self.config)
        self.add_widget(self.worm)
        Clock.schedule_interval(self.update, self.config.INTERVAL)


    def start(self):
        Clock.schedule_interval(self.update, 0.01)

    def update(self, _):
        for cell in self.cells:
            cell.pos = (cell.pos[0] + 2, cell.pos[1] + 3)

    def on_touch_down(self, touch):
        cell = Cell(touch.x, touch.y, 30)
        self.add_widget(cell)
        self.cells.append(cell)



class Worm(Widget):
    def __init__(self, config):
        super().__init__()
        self.cells = []
        self.config = config
        self.cell_size = config.CELL_SIZE
        self.head_init((100, 100))
        for i in range(config.DEFAULT_LENGTH):
            self.lengthen()

    def destroy(self):
        for i in range(len(self.cells)):
            self.remove_widget(self.cells[i])
        self.cells = []

    def lengthen(self, pos=None, direction=(0, 1)):
        # Если позиция установлена, мы перемещаем клетку туда, иначе - в соответствии с данным направлением
        if pos is None:
            px = self.cells[-1].get_pos()[0] + direction[0] * self.cell_size
            py = self.cells[-1].get_pos()[1] + direction[1] * self.cell_size
            pos = (px, py)
        self.cells.append(Cell(*pos, self.cell_size, margin=self.config.MARGIN))
        self.add_widget(self.cells[-1])

    def head_init(self, pos):
        self.lengthen(pos=pos)



class Config:
    DEFAULT_LENGTH = 20
    CELL_SIZE = 25
    APPLE_SIZE = 35
    MARGIN = 4
    INTERVAL = 0.2
    DEAD_CELL = (1, 0, 0, 1)
    APPLE_COLOR = (1, 1, 0, 1)



if __name__ == '__main__':
    WormApp().run()
