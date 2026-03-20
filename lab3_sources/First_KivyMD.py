from kivymd.app import MDApp
from kivymd.uix.label import MDLabel


class MainApp(MDApp):
    def build(self):
        # self.icon = 'pyt.ico'
        # self.title = 'Первое приложение на KivyMD'
        return MDLabel(text="Привет от KivyMD", halign="center")


MainApp().run()
