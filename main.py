from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from camera import cameradect
from storage import folder_setup, get_next_pic_name, get_location


class PhotoboothWidget(Widget):
    def __init__(self):
        super().__init__()
        self.startup()
        folder_setup(self)
        print(get_next_pic_name())

    def startup(self):
        self.clear_widgets()
        self.start = Button(text="Take Photo", pos=(350, 250))
        self.add_widget(self.start)
        self.count = Label(text="", pos=(350, 250), font_size=90)
        self.pic = Label(text="", pos=(350, 250), font_size=90)
        self.start.bind(on_press=self.start_countdown)

    def start_countdown(self, obj):
        count_from = 4
        self.remove_widget(self.start)
        self.add_widget(self.count)

        def count_it(count_from):
            if count_from == 1:
                self.pic_preview()
                return
            count_from -= 1
            self.count.text = str(count_from)
            Clock.schedule_once(lambda dt: count_it(count_from), 1)

        Clock.schedule_once(lambda dt: count_it(count_from), 0)

    def pic_preview(self):
        self.remove_widget(self.count)
        self.add_widget(self.pic)
        self.pic.text = "photo"
        picture = Image(source=(get_location() + get_next_pic_name()), pos_hint={'center_x': 0.5, 'center_y': .6})
        self.add_widget(picture)
        cameradect()
        Clock.schedule_once(lambda dt: self.startup(), 5)


class PhotoboothApp(App):
    def build(self):
        return PhotoboothWidget()


PhotoboothApp().run()
