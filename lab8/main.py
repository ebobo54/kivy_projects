from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import *
import random

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

class Worm(Widget):
    def __init__(self, config):
        super().__init__()
        self.cells = []
        self.config = config
        self.cell_size = config.CELL_SIZE
        self.head_init((100, 100))
        for i in range(config.DEFAULT_LENGTH):
            self.lengthen()

    def move(self, direction):
        for i in range(len(self.cells) - 1, 0, -1):
            self.cells[i].move_to(*self.cells[i - 1].get_pos())
        self.cells[0].step_by(direction)


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

    def gather_positions(self):
        return [cell.get_pos() for cell in self.cells]
    # Проверка пересекается ли голова с другим объектом
    def head_intersect(self, cell):
        return self.cells[0].get_pos() == cell.get_pos()




class Form(Widget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.worm = None
        self.cur_dir = (0, 0)
        self.fruit = None
        self.game_on = True

    def update(self, _):
        if not self.game_on:
            return
        self.worm.move(self.cur_dir)
        if self.worm.head_intersect(self.fruit):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            self.worm.lengthen(direction=random.choice(directions))
            self.fruit_dislocate()
        if self.worm_bite_self():
            self.game_on = False

    def worm_bite_self(self):
        for cell in self.worm.cells[1:]:
            if self.worm.head_intersect(cell):
                return cell
        return False

    def random_cell_location(self, offset):
        x_row = self.size[0] // self.config.CELL_SIZE
        x_col = self.size[1] // self.config.CELL_SIZE
        return random.randint(offset, x_row - offset), random.randint(offset, x_col - offset)

    def random_location(self, offset):
        x_row, x_col = self.random_cell_location(offset)
        return self.config.CELL_SIZE * x_row, self.config.CELL_SIZE * x_col

    def fruit_dislocate(self):
        x, y = self.random_location(2)
        self.fruit.move_to(x, y)


    def start(self):
        self.worm = Worm(self.config)
        self.add_widget(self.worm)
        if self.fruit is not None:
            self.remove_widget(self.fruit)
        self.fruit = Cell(0, 0, self.config.APPLE_SIZE)
        self.fruit_dislocate()
        self.add_widget(self.fruit)
        Clock.schedule_interval(self.update, self.config.INTERVAL)
        self.game_on = True
        self.cur_dir = (0, -1)

    def stop(self):
        self.game_on = False
        Clock.unschedule(self.update)

    def game_over(self):
        self.stop()


    def update(self, _):
        self.worm.move(self.cur_dir)
    
    def on_touch_down(self, touch):
        if not self.game_on:
            self.worm.destroy()
            self.start()
            return

    
    def update(self, _):
        self.worm.move(self.cur_dir)
        if self.worm.head_intersect(self.fruit):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            self.worm.lengthen(direction=random.choice(directions))
            self.fruit_dislocate()



class WormApp(App):
    def build(self):
        self.config = Config()
        self.form = Form(self.config)
        return self.form

    def on_start(self):
        self.form.start()



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