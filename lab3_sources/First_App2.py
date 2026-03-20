# модуль First_App2.py
from kivy.app import App  # импорт приложения фрейморка kivy
from kivy.uix.label import Label  # импорт элемента label (метка)


class MainApp(App):   # формирование базового класса приложения
    def build(self):  # формирование функции в базовом классе
        self.title = 'Приложение один'
        self.icon = './pyt.ico'  # задание собственной иконки
        label = Label(text='Привет от Kivy и Python!')  # значение метке
        return label   # возврат значения метки


if __name__ == '__main__':  # условие вызова главного приложения
    app = MainApp(title="Первое приложение")  # Задание имени приложения
    app.run()                                 # запуск приложения
