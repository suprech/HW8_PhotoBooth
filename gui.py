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
import voice_recog
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
camera.rotation = 180
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
    gif_img.save(latestPhoto,'gif')
    guiPictureBefore.set(latestPhoto)


    im = Image.open(photoOutput)
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
    info("Upload Success", "uploaded")
    pass


def UploadToServer():
    savename = datetime.datetime.now().strftime('%y%m%d-%H%M%s') + '.jpg'

    shutil.copyfile('temp.jpg', 
            '/home/pi/HW8_PhotoBooth/ImageStorage/' + savename)

    #info("Upload Success", "uploaded")


def PhotoPrinter():
    pass


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
# Voice Recognition
#######################################################
def message_selection(cmd):
    pass


# Google Cloud Speech
def call_cloud_speech():
    while True:
        print("listening...")
        cmd = voice_recog.main().lower()
        print("speech was {}".format(cmd))

        if(cmd == "picture" or cmd == "take a picture"):
            NewPicture()

        elif(cmd == "filter"):
            Filter_Back()

        elif(cmd == "first filter" or cmd == "sepia"):
            Sepia()

        elif(cmd == "second filter" or cmd == "grey"):
            Grey()

        elif(cmd == "upload picture"):
            UploadToServer()

        elif(cmd == "print"):
            PhotoPrinter()

        elif(cmd == "email"):
            SendEmail()

        else:
            print("Try Again")
            continue


# Amazon ALEXA
def call_alexa():
    cmd = pi_readqueue.message_handler()
    message_selection(cmd)


if __name__ == '__main__':
    #######################################################
    # multi-threading for voice recognization
    #######################################################
    t = threading.Thread(target=call_cloud_speech)
    #t.start()


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
    ButtonForDropbox = PushButton(box, SendEmail, 
            text="Send to Email", grid = [0,2])
    ButtonForWebServer = PushButton(box, UploadToServer, 
            text="Upload to WebServer", grid = [0,3])
    ButtonForPrint = PushButton(box, PhotoPrinter, 
            text="Print", grid = [0,4])

    # button rendering : Filter Effect menu
    box2 = Box(app, layout="grid", grid=[2,0])
    ButtonTemp1 = PushButton(box2, Sepia, text="Sepia", grid = [0,0])
    ButtonTemp2 = PushButton(box2, Grey, text="GreyScale", grid = [0,1])
    ButtonTemp3 = PushButton(box2, Grey, text="Filter 3", grid = [0,2])
    ButtonTemp4 = PushButton(box2, Grey, text="Filter 4", grid = [0,3])

    # picture rendering
    guiPictureBefore = Picture(app, 'init.gif', grid = [4,0])

    # gui display start
    app.display()
