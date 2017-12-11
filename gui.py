import os
import sys
import shutil
import datetime
import threading
import picamera

from ctypes import * # for error handling
from time import gmtime, strftime, sleep
from guizero import *
from PIL import Image

# user module
#import cloud_speech
import Filter
import pi_readqueue


#######################################################
# Global Objects initialization
#######################################################
photoOutput = str()
latestPhoto = os.getcwd() + '/latest.gif'
im = Image.open(latestPhoto)
tempImg = Image.open(latestPhoto) 


#######################################################
# function for disabling ALSA warning
#######################################################
def py_error_handler(filename, line, function, err, fmt):
    pass

if(sys.platform == 'linux'):
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, 
            c_char_p, c_int, c_char_p)

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)


#######################################################
# PiCamera setting
#######################################################
camera = picamera.PiCamera()
camera.resolution = (800, 480)
#camera.rotation = 180
#camera.hflip = True


#######################################################
# Functions for PhotoBooth
####################################################### 
def TakePicture():
    global photoOutput
    global latestPhoto
    global im
    global tempImg

    # take a picture
    photoOutput = datetime.datetime.now().strftime('%y%m%d-%H%M%s') + '.jpg'
    camera.capture(photoOutput)

    # jpg->gif conversion
    #thumbnailSize = (400, 400)
    gif_img = Image.open(photoOutput)
    #gif_img.thumbnail(thumbnailSize, Image.ANTIALIAS)
    gif_img.save(latestPhoto, 'gif')
    guiPictureBefore.set(latestPhoto)

    im = Image.open(photoOutput)
    im.save('temp.jpg')
    tempImg = im


#######################################################
# Gui Menu CallBack Function
#######################################################
def NewPicture():
    global camera
    camera.start_preview()
    camera.preview.window = (500, 500, 800, 480)
    camera.preview.fullscreen = False

    # count down
    sleep(1)
    camera.annotate_text = '5'
    sleep(1)
    camera.annotate_text = '4'
    sleep(1)
    camera.annotate_text = '3'
    sleep(1)
    camera.annotate_text = '2'
    sleep(1)
    camera.annotate_text = '1'
    sleep(1)
    camera.annotate_text = ''

    TakePicture()
    camera.stop_preview()


def Filter_Back():
    global im
    global tempImg
    global latestPhoto

    # image restore
    im = tempImg
    im.save('temp.jpg')
    guiPictureBefore.set(latestPhoto)


def SendEmail():
    info("Success", "sended")
    pass


def UploadToServer():
    savename = datetime.datetime.now().strftime('%y%m%d-%H%M%s') + '.jpg'
    shutil.copyfile('temp.jpg', 
            '/home/pi/HW8_PhotoBooth/ImageStorage/' + savename)
    print("Upload Success"


def PhotoPrinter():
    printer_cmd = "lp -d Canon_SELPHY_CP1200 " + os.getcwd() + "/temp.jpg"
    os.system(printer_cmd)


#######################################################
# Functions For Filtering
#######################################################
def Sepia():
    global im
    global tempImg

    Filter_Back()

    # back up original image
    tempImg = im

    # Filtering
    im = Filter.SepiaFilter(im)
    im.save('temp.jpg')

    # gui rendering
    im.save('rendering.gif', 'gif')
    guiPictureBefore.set('rendering.gif')


def Gray():
    global im
    global tempImg

    Filter_Back()

    # back up original image
    tempImg = im

    # Filtering
    im = Filter.GrayScale(im)
    im.save('temp.jpg')

    # gui rendering
    im.save('rendering.gif', 'gif')
    guiPictureBefore.set('rendering.gif')


#######################################################
# Voice Recognition Methods
#######################################################
call_list = {
        "picture": NewPicture,
        "shutter": NewPicture,
        "take picture": NewPicture,
        "take a picture": NewPicture,
        "filter": Filter_Back,
        "undo": Filter_Back,
        "first filter": Sepia,
        "sepia": Sepia,
        "second filter": Gray,
        "gray": Gray,
        "grey": Gray,
        "upload": UploadToServer,
        "upload picture": UploadToServer,
        "upload a picture": UploadToServer,
        "upload the picture": UploadToServer,
        "print": PhotoPrinter,
        "printer": PhotoPrinter,
        "photo printer": PhotoPrinter,
        "email": SendEmail,
        "send": SendEmail
        }


def message_selection(cmd):
    global call_list

    if cmd in call_list:
        call_list[cmd]()

    else:
        print("Try Again")


# Google Cloud Speech
'''
def call_cloud_speech():
    print("initializaing Google Cloud Speech")
    while True:
        print("listening...")
        cmd = cloud_speech.main().lower()
        print("speech was {}".format(cmd))
        message_selection(cmd)
'''


# Amazon ALEXA
def call_alexa():
    print("initializaing Amazon ALEXA")
    while True:
        sleep(0.5)
        print("listening...")
        cmd = pi_readqueue.message_handler().lower()
        print("speech was {}".format(cmd))
        message_selection(cmd)


if __name__ == '__main__':
    #######################################################
    # multi-threading for voice recognization
    #######################################################
    #t1 = threading.Thread(target=call_cloud_speech)
    t2 = threading.Thread(target=call_alexa)
    #t1.start()
    t2.start()


    #######################################################
    # Gui Setting
    #######################################################
    # gui init
    app = App(title = "PHOTOBOOTH", height = 800, width = 800, layout = 'grid')

    # message rendering
    message1 = Text(app, "Picture", grid = [3,0])
    message2 = Text(app, "Filter Effect", grid = [1,0])

    # button rendering : main menu
    box = Box(app, layout="grid", grid=[0,0])
    ButtonForCapture = PushButton(box, NewPicture, 
            text="New Picture", grid = [0,0])
    ButtonForFilter = PushButton(box, Filter_Back, 
            text="Filter", grid = [0,1])
    #ButtonForDropbox = PushButton(box, SendEmail, 
    #        text="Send to Email", grid = [0,2])
    ButtonForWebServer = PushButton(box, UploadToServer, 
            text="Upload to WebServer", grid = [0,3])
    ButtonForPrint = PushButton(box, PhotoPrinter, 
            text="Print", grid = [0,4])

    # button rendering : Filter Effect menu
    box2 = Box(app, layout="grid", grid=[2,0])
    ButtonTemp1 = PushButton(box2, Sepia, text="Sepia", grid = [0,0])
    ButtonTemp2 = PushButton(box2, Gray, text="GrayScale", grid = [0,1])

    # picture rendering
    #guiPictureBefore = Picture(app, 'init.gif', grid = [4,0])
    guiPictureBefore = Picture(app, 'latest.gif', grid = [4,0])

    # gui display start
    app.display()
