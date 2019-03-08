from datetime import datetime
import os

folder_location = "./photos"


def folder_setup(self):
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)
    today = datetime.now()
    setlocation(("./photos/" +  today.strftime('%Y%m%d')))
    if not os.path.isdir(folder_location):
        os.mkdir(folder_location)


def getlocation():
    return folder_location

def setlocation(location):
    global folder_location
    folder_location = location
    return