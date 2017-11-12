from PIL import *
from PIL import Image
from PIL import ImageFilter


#im = Image.open('test.jpg')
#blurImage = im.filter(ImageFilter.BLUR)

print("Image Processing...")



'''
밝기 조절
out = im.point(lambda i : i * 2)
'''

# img = Image.open('test.jpg')
# GreyScale(img)
def GreyScale(ImgObj):
    return ImgObj.convert(mode='L')


def Brightness(ImgObj, scale):
    return ImgObj.point(lambda i : i * scale)


def make_linear_ramp(white):
    # putpalette expects [r,g,b,r,g,b,...]
    ramp = []
    r, g, b = white
    for i in range(255):
        ramp.extend((int(r*i/255), int(g*i/255), int(b*i/255)))
    return ramp


# make sepia ramp (tweak color as necessary)
sepia = make_linear_ramp((255, 240, 190))

im = Image.open("test.jpg")

# convert to grayscale
if im.mode != "L":
    im = im.convert("L")


# apply sepia palette
im.putpalette(sepia)

# convert back to RGB so we can save it as JPEG
# (alternatively, save it in PNG or similar)
im = im.convert("RGB")

im.save("file.jpg")


print("Done")




