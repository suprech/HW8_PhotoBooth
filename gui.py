import os
import sys
from ctypes import * # for error handling
import shutil
import datetime
from time import gmtime, strftime, sleep
import threading

import voice_recog

import picamera
from guizero import *
import Filter
from PIL import Image


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
    ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

    c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)


#######################################################
# PiCamera setting
#######################################################
camera = picamera.PiCamera()
camera.resolution = (800, 480)
#camera.hflip = True

camera.start_preview()
camera.preview.window = (1000, 100, 800, 480)
camera.preview.fullscreen = False


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
    TakePicture()


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

    shutil.copyfile('temp.jpg', '/home/pi/HW8_PhotoBooth/ImageStorage/' + savename)

    info("Upload Success", "uploaded")


def PhotoPrinter():
    pass


#######################################################
# Filtering
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


def Grey():
    global im
    global tempImg

    Filter_Back()

    # back up original image
    tempImg = im

    # Filtering
    im = Filter.GreyScale(im)
    im.save('temp.jpg')

    # gui rendering
    im.save('rendering.gif', 'gif')
    guiPictureBefore.set('rendering.gif')


#######################################################
# Voice Recognition (Google Cloud Speech)
#######################################################
def voice():
    while True:
        print("listening...")
        #sleep(1)
        cmd = voice_recog.main().lower()
        print("speech was {}".format(cmd))

        if(cmd == "picture" or cmd == "take a picture"):
            NewPicture()

        elif(cmd == "filter"):
            Filter_Back()

        elif(cmd == "first filter"):
            Sepia()

        elif(cmd == "second filter"):
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


if __name__ == '__main__':
    #######################################################
    # multi-threading for voice recognization
    #######################################################
    t = threading.Thread(target=voice)
    t.start()


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
    ButtonForCapture = PushButton(box, NewPicture, text="New Picture", grid = [0,0])
    ButtonForFilter = PushButton(box, Filter_Back, text="Filter", grid = [0,1])
    ButtonForDropbox = PushButton(box, SendEmail, text="Send to Email", grid = [0,2])
    ButtonForWebServer = PushButton(box, UploadToServer, text="Upload to WebServer", grid = [0,3])
    ButtonForPrint = PushButton(box, PhotoPrinter, text="Print", grid = [0,4])

    # button rendering : Filter Effect menu
    box2 = Box(app, layout="grid", grid=[2,0])
    ButtonTemp1 = PushButton(box2, Sepia, text="Sepia", grid = [0,0])
    ButtonTemp2 = PushButton(box2, Grey, text="GreyScale", grid = [0,1])

    # picture rendering
    guiPictureBefore = Picture(app, 'init.gif', grid = [4,0])

    # gui display start
    app.display()
