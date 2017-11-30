import os

import datetime
from time import gmtime, strftime

import picamera
from guizero import *

import Filter
from PIL import Image


#######################################################
# Objects initialization
#######################################################
photoOutput = str()
latestPhoto = os.getcwd() + '/latest.gif'
im = Image.open(latestPhoto)
tempImg = Image.open(latestPhoto) 



#######################################################
# PiCamera setting
#######################################################
camera = picamera.PiCamera()
camera.resolution = (800, 480)
#camera.hflip = True

camera.start_preview()
camera.preview.window = (500, 500, 800, 480)
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



def Func():
    print("Hello World")


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

    guiPictureBefore.set(latestPhoto)


def SendEmail():
    info("Upload Success", "uploaded")
    pass


def UploadToServer():





    info("Upload Success", "uploaded")
    pass


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
    im.save('temp.gif', 'gif')
    guiPictureBefore.set('temp.gif')


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
    im.save('temp.gif', 'gif')
    guiPictureBefore.set('temp.gif')


    #######################################################
    # Filtering
    #######################################################
    def Sepia(self):
        im = Filter.SepiaFilter(self.im)
        self.SaveImg()
        self.Rendering()
        


    def Grey(self):
        pass


if __name__ == '__main__':

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
    ButtonTemp3 = PushButton(box2, TASD.TestFunc, text="ClassTest", grid = [0,2])


    # picture rendering
    guiPictureBefore = Picture(app, 'init.gif', grid = [4,0])
    #guiPictureAfter = Picture(app, 'init.gif', grid = [3,1])


    app.display()



