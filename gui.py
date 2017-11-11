from guizero import *
from time import gmtime, strftime
from PIL import Image
import datetime
import picamera
import os


#######################################################
# Objects initialization
#######################################################
photoOutput = str()
latestPhoto = os.getcwd() + '/latest.gif'



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

    # take a picture
    photoOutput = datetime.datetime.now().strftime('%y%m%d-%H%M%s') + '.jpg'
    camera.capture(photoOutput)

    # jpg->gif conversion
    thumbnailSize = (400, 400)
    gif_img = Image.open(photoOutput)
    gif_img.thumbnail(thumbnailSize, Image.ANTIALIAS)
    gif_img.save(latestPhoto,'gif')
    guiPictureBefore.set(latestPhoto)



def Func():
    print("Hello World")


#######################################################
# Gui Menu CallBack Function
#######################################################
def NewPicture():
    TakePicture()


def Filter():
    pass


def UploadDropbox():
    info("Upload Success", "uploaded")
    pass


def UploadServer():
    pass


def PrintPicture():
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
    ButtonForFilter = PushButton(box, Filter, text="Filter", grid = [0,1])
    ButtonForDropbox = PushButton(box, UploadDropbox, text="Dropbox", grid = [0,2])
    ButtonForWebServer = PushButton(box, UploadServer, text="Upload to WebServer", grid = [0,3])
    ButtonForPrint = PushButton(box, PrintPicture, text="Print", grid = [0,4])


    # button rendering : Filter Effect menu
    box2 = Box(app, layout="grid", grid=[2,0])
    ButtonTemp1 = PushButton(box2, Func, text="Option 1", grid = [0,0])
    ButtonTemp2 = PushButton(box2, Func, text="Option 2", grid = [0,1])


    # picture rendering
    guiPictureBefore = Picture(app, 'init.gif', grid = [4,0])
    #guiPictureAfter = Picture(app, 'init.gif', grid = [3,1])


    app.display()

