


#!/usr/bin/env python

import sys
import time
import uuid
import time
import md5
import string
import random

from SimpleCV import *

global gif_frames # Frames per .gif file
global gif_frameRate # Frame rate for gif playback and gif record 

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # gif frame number and gif frame rate can be provided as arguments
        gif_frames = float(sys.argv[1]) 
        gif_frameRate = float(sys.argv[2])
    else:
        gif_frames = 8.0 
        gif_frameRate = 0.4




class CameraCapture():

    _img_res_width = 320 
    _img_res_height = 240
    _screen_text = "Virtualizing!"

    """
    The images captured by the camera will scale to the resolution provided. 
    """

    def __init__(self,index,width = _img_res_width , height = _img_res_height):
        self.width = width
        self.height = height
        self.cam = Camera(index, prop_set={"width":self.width,"height":self.height})


    def getNewImage(self, image_modifier=None):
        img = self.cam.getImage()
        return img

    def makeGifSet(self):
        self.file_name = uuid.uuid4().hex # make a unique file name
        self.img_set = ImageSet(directory=("output/"+ self.file_name  )) # imageClass.ImageSet()  

    def fillSetThenSave(self, image):
        if self.img_set != None  and len(self.img_set) >= gif_frames:
            self.img_set._write_gif(filename=( "output/"+self.file_name + ".gif"),\
                duration=(gif_frameRate), dither=2) 
            return self.img_set

        if self.img_set != None:
            self.img_set.append(image)
            return None

    def control_generator(self):	

class TimeController(object):
    def __init__(self, interval, occurances=1):
        self.start_time = time.time()
        self.interval = interval
        self.occurances = occurances


    def check_timer(self):
        if self.occurances == 0 or self.occurances ==  None: 
            self.occurances = None
            return self.occurances
        elif time.time() - self.start_time >= self.interval:
            self.occurances -= 1
            self.start_time = time.time()
            return self.occurances
        else:
            return False

    def __repr__(self):
        return self.occurances

# Init camera 
cam1 = CameraCapture(1)

# Init display
# The display resolution should match or fit within your display. The images capture
# by the camera will be scaled to fit the display.
disp = Display(flags=pg.FULLSCREEN , resolution = (1020 , 765))

print("\n >>>Press the ESC key to exit!")
while disp.isNotDone():
    # 1 Get image
    img1 = cam1.getNewImage()
    dwn = disp.leftButtonDownPosition()
    # 2 Record Gif
    if dwn != None :


    if cam1.frameTimer():
        gifSet = cam1.fillSetThenSave(img1)
        if gifSet != None:
            for j in range(0, 3):
                for i in gifSet:
                    i.save(disp)
                    time.sleep(gif_frameRate )
                else:
                    time.sleep(gif_frameRate * 3)
            else:
                print "reset"
                cam1.resetGifSet()
    # 4 Display
    img1.save(disp)

print("\n >>>Program Exitted")
quit()


      #fit* - When fit=False write frame will crop and center the image as best it can.
      #If the image is too big it is cropped and centered. If it is too small
      #it is centered. If it is too big along one axis that axis is cropped and
      #the other axis is centered if necessary."""

    # the gifs should be at 320x240 or 640x480
    # adaptive color palette, a little bit of lossy, and dithering
    # if you can do these things..
    # ideally the GIFs would be < 1 MB
    # about a MB is ok
    # more than that and people wont be able to load them reliably (like on their phones) and it will slow down / fuck up browsers. i mean a lil over a MB is OK but ideally its really no bigger
    # shrug maybe 2 MB would be ok, idk