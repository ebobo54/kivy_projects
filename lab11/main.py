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

    def on_press(self):
        if self.val + 1 < len(self.col):
            self.val += 1
        else:
            self.val = 0
        self.background_color = self.col[self.val]

class Board(Widget):
    def Start(self):
        self.pins = []
        for a in range(4):
            b = Pin()
            b.on_press()                     # инициализация цвета
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

# KV-строка загружена ПОСЛЕ объявления класса Board
Builder.load_string("""
<Board>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: 310, 70
""")

class MasterMind(Widget):
    h = None

    def Test(self, inp, coder):
        out = []
        code = list(coder)
        inp_copy = list(inp)       # работаем с копией, чтобы не испортить оригинал
        for a in range(4):
            if code[a] == inp_copy[a]:
                out.append(2)
                code[a] = "a"
                inp_copy[a] = 80.5
        for a in range(4):
            if inp_copy[a] in code:
                out.append(1)
        for _ in range(4 - len(out)):
            out.append(0)
        return out

    def Check(self, button):
        inp = [pin.val for pin in button.parent.pins]
        if inp != self.code:
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
        a = Board()
        # Используем self.h как опорную точку (верхний край)
        a.pos = (0, self.h - 80 * Npos)
        a.Start()
        submit_btn = Button(text="Submit", size=(50, 50),
                            pos=(a.pos[0] + 10, a.pos[1] + 10),
                            on_press=self.Check)
        a.add_widget(submit_btn)
        self.add_widget(a)
        self.b.append(a)

    def Setup(self, *args):
        self.attempts = 0
        self.b = []
        if self.h is None:
            # Вычисляем один раз после получения реального размера окна
            self.h = self.height - 10   # 10 – отступ сверху
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
        self.WinLabel = Label(text=win_text, pos=(500, 500), font_size=50)
        self.add_widget(self.WinLabel)
        restart_btn = Button(text="Restart", pos=(450, 470), size=(200, 50),
                             on_press=self.Restart)
        self.add_widget(restart_btn)

class MasterMindApp(App):
    def build(self):
        game = MasterMind()
        # Запускаем настройку после того, как окно примет окончательный размер
        Clock.schedule_once(game.Setup, 0)
        return game

if __name__ == '__main__':
    MasterMindApp().run()