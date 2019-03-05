from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.clock import Clock
import time
import gphoto2 as gp
import logging


def cameradect():
    logging.basicConfig(
        format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    text = gp.check_result(gp.gp_camera_get_summary(camera))
    print('Summary')
    print('=======')
    print(text.text)
    print('Abilities')
    print('=========')
    abilities = gp.check_result(gp.gp_camera_get_abilities(camera))
    print('model:', abilities.model)
    print('status:', abilities.status)
    print('port:', abilities.port)
    print('speed:', abilities.speed)
    print('operations:', abilities.operations)
    print('file_operations:', abilities.file_operations)
    print('folder_operations:', abilities.folder_operations)
    print('usb_vendor:', abilities.usb_vendor)
    print('usb_product:', abilities.usb_product)
    print('usb_class:', abilities.usb_class)
    print('usb_subclass:', abilities.usb_subclass)
    print('usb_protocol:', abilities.usb_protocol)
    print('library:', abilities.library)
    print('id:', abilities.id)
    print('device_type:', abilities.device_type)
    gp.check_result(gp.gp_camera_exit(camera))
    return 0


class PhotoboothWidget(Widget):
    def __init__(self):
        super().__init__()
        self.start = Button(text="Start Game", pos=(350, 250))
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
                self.pic_preciew()
                return
            count_from -= 1
            self.count.text = str(count_from)
            Clock.schedule_once(lambda dt: count_it(count_from), 1)

        Clock.schedule_once(lambda dt: count_it(count_from), 0)

    def pic_preview(self):
        self.remove_widget(self.count)
        self.add_widget(self.pic)
        self.pic.text = "photo"
        cameradect()


class PhotoboothApp(App):
    def build(self):
        return PhotoboothWidget()


PhotoboothApp().run()
