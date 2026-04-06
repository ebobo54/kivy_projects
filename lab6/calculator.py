from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window 
class CalculatorApp(App):
    def build(self):
        self.history = []
        self.history_visible = False

        root = BoxLayout(orientation="horizontal", padding=10, spacing=10)
        self.calc_layout = BoxLayout(orientation="vertical", spacing=10, size_hint=(0.7, 1))

        self.input = TextInput(multiline=False, readonly=True, halign="right", font_size=40, size_hint=(1, 0.2))
        self.calc_layout.add_widget(self.input)

        control_layout = GridLayout(cols=4, spacing=10, size_hint=(1, 0.1))
        for label in ('<-', 'C', 'M', '='):
            control_layout.add_widget(Button(text=label, font_size=28, on_press=self.on_control_press))
        self.calc_layout.add_widget(control_layout)

        buttons = [
            ['7', '8', '9', '*'],
            ['4', '5', '6', '/'],
            ['.', '0', '00', '-']
        ]
        button_layout = GridLayout(cols=4, spacing=10, size_hint=(1, 0.7))
        for row in buttons:
            for label in row:
                button_layout.add_widget(Button(text=label, font_size=32, on_press=self.on_button_press))
        self.calc_layout.add_widget(button_layout)

        root.add_widget(self.calc_layout)

        self.history_layout = BoxLayout(orientation="vertical", size_hint=(0, 1))
        self.history_scroll = ScrollView()
        self.history_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        self.history_scroll.add_widget(self.history_grid)
        self.history_layout.add_widget(self.history_scroll)
        root.add_widget(self.history_layout)

        Window.bind(on_key_down=self.on_key_down)
        return root

    def on_button_press(self, instance):
        self.add_char(instance.text)

    def on_control_press(self, instance):
        if instance.text == '<-':
            self.input.text = self.input.text[:-1]
        elif instance.text =='C':
            self.input.text = ''
        elif instance.text =='M':
            self.toggle_history()
        elif instance.text =='=':
            self.calculate()
    
    def add_char(self, char):
        if char in '+-*':
            if self.input.text and self.input.text[-1] in '+-*':
                self.input.text = self.input.text[:-1] + char
            elif self.input.text:
                self.input.text += char
        else:
            self.input.text += char

    def calculate(self):
        try:
            result = str(eval(self.input.text))  
            self.history.append(f"{self.input.text} = {result}")
            self.input.text = result
            self.update_history()
        except Exception:
            self.input.text = "Ошибка"
        
    def toggle_history(self):
        if self.history_visible:
            self.historylayout.size_hint_x = 0
            self.history_visible = False
        else:
            self.history_layout.size_hint_x = 0.3
            self.history_visible = True
    
    def update_history(self):
        self.history_grid.clear_widgets()
        for item in reversed(self.history):
            btn = Button(text=item, size_hint_y=None, height=40)
            btn.bind(on_press=self.load_history)
            self.history_grid.ad_widget(btn)
    
    def load_history(self, instance):
        expr = instance.text.split('=')[0].strip()
        self.input.text = expr
    
    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if 48 <= key <=57:
            self.add_char(chr(key))
        if codepoint is not None and codepoint in '+-*/':
            self.add_char(codepoint)
        if key == 8:
            self.input.text = self.input.text[:-1]
        if key == 13:
            self.calculate()
        if codepoint is not None and codepoint in 'mM':
            self.toggle_history()
        if codepoint is not None and codepoint in 'cC':
            self.input.text=''
        numpud_digits = {
            256: '0',
            257: '1',
            258: '2',
            259: '3',
            260: '4',
            261: '5',
            262: '6',
            263: '7',
            264: '8',
            265: '9'
        }
        if key in nmpad_digits:
            self.add_char(numpud_digits[key])   
        numpad_ops = {
            270: '+',
            269: '-',
            268: '*',
            267: '/',
            271: '.',
        }
        if key in numpad_ops:
            self.add_char(numpad_ops[key])
if __name__=="__main__":
    CalculatorApp().run()