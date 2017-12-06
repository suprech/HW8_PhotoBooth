import picamera
import time
import datetime
import os


camera = picamera.PiCamera()
camera.resolution = (1280,720)
camera.rotation = 180
camera.framerate = 24
#camera.start_preview(fullscreen = False, window=(150,50,1920,1080))
camera.start_preview(fullscreen = False)
camera.preview.window = (1000, 100, 800, 480)


def screenshot():
    if __name__ == '__main__':
        current_dir = os.getcwd() + '/screenshot/'

    else:
        # this dir is used when call by main.py
        current_dir = os.getcwd() + '/camera/screenshot/'

    Filename = current_dir+datetime.datetime.now().strftime('%y%m%d-%H%M%S%f') + '.jpg'
    camera.capture(Filename, )
    print("Screenshot Capture : {}".format(Filename))
    time.sleep(0.1)


print("Camera Module Start")


# tests
if __name__ == '__main__':
    while True:
        time.sleep(1)
