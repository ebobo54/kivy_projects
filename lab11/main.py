from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random as r


class Mark(Button):
    size = (20, 20)
    col = ((0, 0, 0, 0), (0.5, 0.5, 0.5, 1), (0, 0, 0, 1))
    val = 2

    def a(self):
        self.background_color = self.col[self.val]


class Pin(Button):
    alf = 1
    col = ((1, 0, 0, alf), (0, 1, 0, alf), (0, 0, 1, alf),
           (1, 0, 1, alf), (1, 1, 0, alf), (0, 1, 1, alf))
    val = -1
    size = (50, 50)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_color()

    def on_press(self):
        if self.val + 1 < len(self.col):
            self.val += 1
        else:
            self.val = 0
        self.update_color()

    def update_color(self):
        if 0 <= self.val < len(self.col):
            self.background_color = self.col[self.val]
        else:
            self.background_color = (0, 0, 0, 0)


class Board(Widget):
    def Start(self):
        self.pins = []
        for a in range(4):
            b = Pin()
            b.pos = (self.pos[0] + 70 + a * 60, self.pos[1] + 10)
            self.add_widget(b)
            self.pins.append(b)

    def SumUp(self, resList):
        x = ((self.pos[0] + 10, self.pos[1] + 10),
             (self.pos[0] + 40, self.pos[1] + 10),
             (self.pos[0] + 10, self.pos[1] + 40),
             (self.pos[0] + 40, self.pos[1] + 40))
        for b in range(4):
            a = Mark(pos=x[b])
            a.val = resList[b]
            a.a()
            self.add_widget(a)


Builder.load_string("""
<Board>:
    size_hint: None, None
    size: 310, 70
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
""")


class MasterMind(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.h = None
        self.board_height = 70
        self.margin = 10

    def Test(self, inp, coder):
        out = []
        code = list(coder)
        inp_copy = list(inp)

        for i in range(4):
            if inp_copy[i] == code[i]:
                out.append(2)
                code[i] = -1
                inp_copy[i] = -2

        for i in range(4):
            if inp_copy[i] >= 0 and inp_copy[i] in code:
                out.append(1)
                code[code.index(inp_copy[i])] = -1

        out += [0] * (4 - len(out))
        return out

    def Check(self, button):
        inp = [pin.val for pin in button.parent.pins]
        if inp != list(self.code):
            button.parent.SumUp(self.Test(inp, self.code))
            button.parent.remove_widget(button)
            if self.attempts < 5:
                self.SpawnBoard(self.attempts + 1)
                self.attempts += 1
            else:
                self.EndGame(False)
        else:
            self.EndGame(True)

    def SpawnBoard(self, Npos):
        board = Board()
        y_top = self.h - Npos * (self.board_height + self.margin)
        board.pos = (0, y_top - self.board_height)
        board.Start()
        submit = Button(
            text="Submit",
            size=(50, 30),
            pos=(board.pos[0] + 5, board.pos[1] + 5),
            on_press=self.Check
        )
        board.add_widget(submit)
        self.add_widget(board)
        self.b.append(board)

    def Setup(self, *args):
        self.attempts = 0
        self.b = []
        self.h = self.height - self.margin
        self.code = tuple(r.randint(0, 5) for _ in range(4))
        self.SpawnBoard(0)

    def Restart(self, button):
        for b in self.b:
            self.remove_widget(b)
        self.remove_widget(self.WinLabel)
        self.remove_widget(button)
        self.Setup()

    def EndGame(self, condition):
        win_text = "You Won" if condition else "You Lost"
        self.WinLabel = Label(
            text=win_text,
            size_hint=(None, None),
            size=(200, 50),
            pos=(self.center_x - 100, self.center_y + 25),
            font_size=40
        )
        self.add_widget(self.WinLabel)
        restart_btn = Button(
            text="Restart",
            size=(150, 50),
            pos=(self.center_x - 75, self.center_y - 50),
            on_press=self.Restart
        )
        self.add_widget(restart_btn)


class MasterMindApp(App):
    def build(self):
        game = MasterMind()
        Clock.schedule_once(game.Setup, 0)
        return game


if __name__ == '__main__':
    MasterMindApp().run()