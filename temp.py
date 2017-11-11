import controller.controller as controller
from ard_serial.ard_serial import *
import sonic.sonic as sonic
import camera.camera as camera
import RPi.GPIO as GPIO

# global varialble init
distance = sonic.distance()
passport = True
stop = True
gdir = '0'

def check_direction(controlId, value):
    global gdir
    # up
    if(controlId == 1 and value > 0):
        gdir = 'u'
        return 'u'

    # down
    elif(controlId == 1 and value < 0):
        gdir = 'd'
        return 'd'

    # left
    elif(controlId == 3 and value > 0):
        gdir = 'l'
        return 'l'

    # right
    elif(controlId == 3 and value < 0):
        gdir = 'r'
        return 'r'

    else:
        gdir = '0'
        return '0'


def check_speed(value):
    value = abs(value)
    if(value < 50):
        return 100

    elif(value >= 50):
        return value * 2.2


def controlCallBack(controlId, value):
    # use passport as global variable
    global passport
    global distance
    global stop

    # check user control
    if(controlId == 1 or controlId == 3):
        direction = check_direction(controlId, value)

        #stop condition 
        if (stop):
            print("distance : {} \t blocking".format(distance))

            if(passport == True):
                passport = False
                camera.screenshot()

            direction = '0' 
            speed = str(round(check_speed(value)))
            temp = 'x' + str(direction) + str(speed)
            print(temp)
            data = '{}\n'.format(temp)
            serialArduino.write(bytes(data, 'UTF-8'))

        #go condition
        else:
            print("distance : {} \t pass".format(distance))
            speed = str(round(check_speed(value)))
            temp = 'x' + str(direction) + str(speed)
            print(temp)
            data = '{}\n'.format(temp)
            serialArduino.write(bytes(data, 'UTF-8'))
            passport = True

    serialArduino.flushInput()


# main function
if __name__ == '__main__':
    # construct controller class instance
    mypad = controller.XboxController(controlCallBack, deadzone = 30, scale = 100, invertYAxis = True)

    try:
        mypad.start()
        print("xbox/ds4 controller running(threading)")

        while True:
            time.sleep(0.1)
            distance = sonic.distance()
            if (distance < 30 and gdir == 'u'):
                stop = True
                speed = str(100)
                temp = 'x' + '0' + str(speed)
                data = '{}\n'.format(temp)
                print("stop function activated")
                serialArduino.write(bytes(data, 'UTF-8'))
                serialArduino.flushInput()
            else:
                stop = False


    except KeyboardInterrupt:
        print("User Canceled(Ctrl-C)")

    # normal exit
    finally:
        mypad.stop()
        GPIO.cleanup()

