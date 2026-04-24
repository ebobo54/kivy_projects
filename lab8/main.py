from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

class Cell(Widget):
    def __init__(self, x, y, size):
        super().__init__()
        self.size = (size, size)
        self.pos = (x, y)


class Form(Widget):
    def __init__(self):
        super().__init__()
        self.cells = []

    def start(self):
        Clock.schedule_interval(self.update, 0.01)

    def update(self, _):
        for cell in self.cells:
            cell.pos = (cell.pos[0] + 2, cell.pos[1] + 3)

    def on_touch_down(self, touch):
        cell = Cell(touch.x, touch.y, 30)
        self.add_widget(cell)
        self.cells.append(cell)



class WormApp(App):
    def build(self):
        self.form = Form()
        self.form.start()
        return self.form


if __name__ == '__main__':
    WormApp().run()
