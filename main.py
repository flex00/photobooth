from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
import time


class PhotoboothWidget(Widget):
    def __init__(self):
        super().__init__()
        self.start = Button(text="Start Game", pos=(350, 250))
        self.add_widget(self.start)
        self.count = Label(text="", pos=(350, 250), font_size=90)
        self.pic = Label(text="", pos=(350, 250), font_size=90)
        self.start.bind(on_press=self.start_game)

    def start_game(self, obj):
        num = 4
        self.remove_widget(self.start)
        self.add_widget(self.count)

        def count_it(num):
            if num == 1:
                self.pic_preciew()
                return
            num -= 1
            self.count.text = str(num)
            Clock.schedule_once(lambda dt: count_it(num), 1)

        Clock.schedule_once(lambda dt: count_it(num), 0)

    def pic_preciew(self):
        self.remove_widget(self.count)
        self.add_widget(self.pic)
        self.pic.text = "photo"


class PhotoboothApp(App):
    def build(self):
        return PhotoboothWidget()


PhotoboothApp().run()
