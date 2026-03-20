# модуль First_App_Kivy2.py
from kivy.app import App  # импорт приложения фрейморка kivy
from kivy.uix.label import Label  # импорт элемента label (метка)


class MainApp(App):  # формирование базового класса приложения
    def build(self):  # формирование функции в базовом классе
        self.title = 'Приложение на Kivy'  # Имя приложения
        self.icon = './pyt.ico'  # иконка (логотип) приложения
        label = Label(text='Привет от Kivy и Python!')  # значение метке
        return label  # возврат значения метки


if __name__ == '__main__':  # условие вызова приложения
    app = MainApp()  # Задание приложения
    app.run()  # запуск приложения
