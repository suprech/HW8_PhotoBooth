#from PIL import * 
from PIL import Image
from PIL import ImageFilter


##################################################
# Functions 
##################################################

def make_linear_ramp(white):
    # putpalette expects [r,g,b,r,g,b,...]
    ramp = []
    r, g, b = white
    for i in range(255):
        ramp.extend((int(r*i/255), int(g*i/255), int(b*i/255)))
    return ramp


##################################################
# Filter Option
##################################################

# Brightness
def Brightness(ImgObj, scale):
    return ImgObj.point(lambda i : i * scale)


# Blur
def BlurImg(Img):
    return Img.filter(ImageFilter.BLUR)


# GreyScale(img)
def GreyScale(ImgObj):
    return ImgObj.convert(mode='L')


# Sepia Filter
def SepiaFilter(Img):

    # make sepia ramp (tweak color as necessary)
    sepia = make_linear_ramp((255, 240, 190))

    # convert to grayscale
    if Img.mode != "L":
        Img = Img.convert("L")

    # apply sepia palette
    Img.putpalette(sepia)

    # convert back to RGB so we can save it as JPEG
    # (alternatively, save it in PNG or similar)
    Img = Img.convert("RGB")
    #Img.save("file.jpg") # deprecated for gui.py

    return Img



if __name__ == '__main__':
    print("Image Processing...")


    # Sepia Filter
    im = Image.open('test.jpg')
    im = BlurImg(im)

    im.save('file.jpg')

    print("Done")

