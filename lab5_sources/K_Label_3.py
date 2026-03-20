# модуль K_Label_3.py
from kivy.graphics.svg import Window
from kivy.lang import Builder
from kivy.app import App

KV = '''
BoxLayout:
    orientation: "vertical"
    Label:
        text: "Текст 1"
        font_size: 32
    Label:
        text: "Текст 2"
        font_size: 64
        color: 1,0,0,1
    Label:
        text: "Текст 64"
        font_size: 64
        font_name: './Font/cataneo.ttf'
    Label:
        text: "Текст 32"
        font_size: 32
        font_name: './Font/cataneo.ttf'    
'''
Window.size = (360, 600)
# Window.size = (600, 400)


class MainApp(App):
    def build(self):
        return Builder.load_string(KV)


MainApp().run()
