from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from camera import cameradect
from storage import folder_setup, get_location, get_last_pic_name

KIVY_FONTS = [
    {
        "name": "Amatic",
        "fn_regular": "fonts/AmaticSC-Regular.ttf",
        "fn_bold": "fonts/Amatic-Bold.ttf"
    }
]

for font in KIVY_FONTS:
    LabelBase.register(**font)

class PhotoboothWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__()
        super(PhotoboothWidget, self).__init__(**kwargs)
        self.start = Button(text="Take Photo", pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(.5, .5), font_name='Amatic')
        self.count = Label(text="", pos_hint={'center_x': .5, 'center_y': .5}, font_size=190, font_name='Amatic')
        self.take_picture = Button(text="Nieuwe foto", pos_hint={'bottom': 1, 'left': 1}, size_hint=(.2, .2))
        self.print_picture = Button(text="Print foto", pos_hint={'bottom': 1, 'right': 1}, size_hint=(.2, .2))
        self.startup()
        folder_setup(self)

    def startup(self):
        self.clear_widgets()

        self.add_widget(self.start)
        self.start.font_name = 'Amatic'
        self.start.font_size = 72

        self.start.bind(on_press=self.start_countdown)

    def start_countdown(self, obj):
        self.clear_widgets()
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

    def start_print(self, obj):
        Clock.schedule_once(lambda dt: self.startup(), 5)



    def pic_preview(self):
        self.remove_widget(self.count)
        # self.add_widget(self.pic)
        # self.pic.text = "photo"
        cameradect()
        picture = Image(source=(get_location() + "/" + get_last_pic_name()), pos_hint={'center_x': .5, 'center_y': .5},
                        size_hint=(.5, .5))
        self.add_widget(picture)
        picture.keep_ratio = True
        self.take_picture.bind(on_press=self.start_countdown)
        self.add_widget(self.take_picture)
        self.print_picture.bind(on_press=self.start_print)
        self.add_widget(self.print_picture)

        # picture.size = (400,400)
        # picture.pos_hint={'center_x': .5, 'center_y': .5}


class PhotoboothApp(App):
    def build(self):
        self.root = root = PhotoboothWidget()
        root.bind(size=self._update_rect, pos=self._update_rect)
        Window.fullscreen = 'auto'

        with root.canvas.before:

            Color(0, 0, 0, 1)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
            root.add_widget(Image(
                source="./images/background.png",
                keep_ratio=False,
                allow_stretch=True), 1)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


PhotoboothApp().run()
