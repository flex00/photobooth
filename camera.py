import os
import subprocess
import time
import logging
import sys
from storage import get_location, get_next_pic_name

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
