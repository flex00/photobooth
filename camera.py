import os
import io
import logging
import subprocess
import time
import logging
import sys
from PIL import Image, ImageOps
import io
from kivy.core.image import Image as CoreImage

from storage import get_location, get_next_pic_name
from PIL import Image

try:
    import gphoto2 as gp

    gphoto = True
except ImportError:
    gphoto = False


def cameradect():
    if not gphoto:
        return
    camera = gp.Camera()
    camera.init()
    print('Capturing image')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))

    target = os.path.join(get_location(), time.strftime("%H%M%S"))
    print('Copying image to', )
    camera_file = gp.check_result(gp.gp_camera_file_get(
        camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    print("check result")
    gp.check_result(gp.gp_file_save(camera_file, target))
    gp.check_result(gp.gp_camera_exit(camera))
    return


class CameraGphoto2:

    def __init__(self):

        super().__init__()

        self.hasPreview = True
        self.hasIdle = True

        logging.info('Using python-gphoto2 bindings')

        self._setupLogging()
        self._setupCamera()

    def __exit__(self, exc_type, exc_value, traceback):

        self.cleanup()

    def cleanup(self):

        try:
            config = self._cap.get_config()
            config.get_child_by_name('imageformat').set_value(
                self._imageformat)
            config.get_child_by_name('imageformatsd').set_value(
                self._imageformat)
            # config.get_child_by_name('autopoweroff').set_value(
            #     self._autopoweroff)
            self._cap.set_config(config)
        except BaseException as e:
            logging.warning('Error while changing camera settings: {}.'.format(e))

        self._cap.exit(self._ctxt)

    @staticmethod
    def _setupLogging():

        gp.error_severity[gp.GP_ERROR] = logging.ERROR
        gp.check_result(gp.use_python_logging())

    def _setupCamera(self):

        self._ctxt = gp.Context()
        self._cap = gp.Camera()
        self._cap.init(self._ctxt)

        logging.info('Camera summary: %s',
                     str(self._cap.get_summary(self._ctxt)))

        try:
            # get configuration tree
            config = self._cap.get_config()

            # make sure camera format is not set to raw
            imageformat = config.get_child_by_name('imageformat')
            self._imageformat = imageformat.get_value()
            if 'raw' in self._imageformat.lower():
                imageformat.set_value('Large Fine JPEG')
            imageformatsd = config.get_child_by_name('imageformatsd')
            self._imageformatsd = imageformatsd.get_value()
            if 'raw' in self._imageformatsd.lower():
                imageformatsd.set_value('Large Fine JPEG')

            # make sure autopoweroff is disabled
            # this doesn't seem to work
            # autopoweroff = config.get_child_by_name('autopoweroff')
            # self._autopoweroff = autopoweroff.get_value()
            # logging.info('autopoweroff: {}'.format(self._autopoweroff))
            # if int(self._autopoweroff) > 0:
            #     autopoweroff.set_value('0')

            # apply configuration and print current config
            self._cap.set_config(config)
        except BaseException as e:
            logging.warning('Error while changing camera settings: {}.'.format(e))

        self._printConfig(self._cap.get_config())

    @staticmethod
    def _configTreeToText(tree, indent=0):

        config_txt = ''

        for chld in tree.get_children():
            config_txt += indent * ' '
            config_txt += chld.get_label() + ' [' + chld.get_name() + ']: '

            if chld.count_children() > 0:
                config_txt += '\n'
                config_txt += CameraGphoto2._configTreeToText(chld, indent + 4)
            else:
                config_txt += str(chld.get_value())
                try:
                    choice_txt = ' ('

                    for c in chld.get_choices():
                        choice_txt += c + ', '

                    choice_txt += ')'
                    config_txt += choice_txt
                except gp.GPhoto2Error:
                    pass
                config_txt += '\n'

        return config_txt

    @staticmethod
    def _printConfig(config):
        config_txt = 'Camera configuration:\n'
        config_txt += CameraGphoto2._configTreeToText(config)
        logging.info(config_txt)

    def setActive(self):

        try:
            config = self._cap.get_config()
            config.get_child_by_name('output').set_value('PC')
            self._cap.set_config(config)
        except BaseException as e:
            logging.warning('Error while setting camera output to active: {}.'.format(e))

    def setIdle(self):

        try:
            config = self._cap.get_config()
            config.get_child_by_name('output').set_value('Off')
            self._cap.set_config(config)
        except BaseException as e:
            logging.warning('Error while setting camera output to idle: {}.'.format(e))

    def getPreview(self):

        camera_file = self._cap.capture_preview()
        file_data = camera_file.get_data_and_size()
        return Image.open(io.BytesIO(file_data))

    def getPicture(self):

        file_path = self._cap.capture(gp.GP_CAPTURE_IMAGE)
        camera_file = self._cap.file_get(file_path.folder, file_path.name,
                                         gp.GP_FILE_TYPE_NORMAL)
        file_data = camera_file.get_data_and_size()
        return Image.open(io.BytesIO(file_data))

    def capturePreview(self):

        # picture = self._cap.getPreview()
        camera_file = self._cap.capture_preview()
        file_data = camera_file.get_data_and_size()

        data = io.BytesIO(file_data)
        im = CoreImage(data, ext="jpg").texture
        return im
