import camera.camera as camera
import RPi.GPIO as GPIO




if __name__ == '__main__':
    print("HW Team #8 - PhotoBooth")


    '''
    a : capture
    b : Image Filtering By Open CV
    c : Print
    d : 
    e :
    '''
    while(True):
        select = input("press any key:")

        if(select == 'a'):
            camera.screenshot()

        elif(select == 'b'):
            print("asdf")
            pass

        else:
            print("Bye")
            break








