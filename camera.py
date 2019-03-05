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
