import re
from datetime import datetime
import os

folder_location = "./photos"


def folder_setup(self):
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)
    today = datetime.now()
    set_location(("./photos/" + today.strftime('%Y%m%d')))
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)


def get_location():
    return folder_location


def set_location(location):
    global folder_location
    folder_location = location
    return

def get_last_pic_name():
    list_of_files = os.listdir(get_location())
    def extract_number(f):
        s = re.findall("(\d+).jpg", f)
        print(s)
        return (int(s[0]) if s else -1, f)
    if list_of_files:
        print(list_of_files)
        return max(list_of_files, key=extract_number)
    else:
        return ""


def get_next_pic_name():
    max_file = get_last_pic_name()
    if max_file:
        max_file = max_file[3:-4]
        max_file = int(max_file) + 1
        return "pic" + str(max_file).zfill(4) + ".jpg"
    else:
        return "pic0000.jpg"