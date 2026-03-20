# модуль First_App_Kivy.py
import kivy.app  # импорт фрейморка kivy
import kivy.uix.label  # импорт визуального элемента label (метка)


class MainApp(kivy.app.App):  # формирование базового класса приложения
    def build(self):  # формирование функции в базовом классе
        return kivy.uix.label.Label(text="Привет от Kivy!")


app = MainApp(title="Первое приложение на Kivy")  # Задание имени приложеня
app.run()  # запуск приложения
