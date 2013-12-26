#!/usr/bin/env python

import sys
import time
import uuid
import time

from SimpleCV import *

global gif_frames
global gif_frameRate 

if __name__ == '__main__':
    if len(sys.argv) == 3:
        gif_frames = float(sys.argv[1])
        gif_frameRate = float(sys.argv[2])
    else:
        gif_frames = 8
        gif_frameRate = 0.4


#class GifPlayback()
  # Initialize the camera 
# screen rez 1280 1024 

class CameraCapture():
        
    _key = True
    _width = 320
    _height = 240

    def __init__(self,index,width = 320 , height = 240):
        self.width = width
        self.height = height
        self.cam = Camera(index, prop_set={"width":self.width,"height":self.height})
        self.img_set = None 
        self.start_timer = None
            
    def setKey(self):
        if(self._key):
            self._key = False
        else:
            self._key = True

    def makeGifSet(self):
        self.file_name = uuid.uuid4().hex # make a unique file name
        self.img_set = ImageSet(directory=("output/"+ self.file_name  )) #init an imageClass.ImageSet()  
        self.start_timer = time.time() #assign a value to start_timer


    def gifSetExistsBool(self):
        if self.img_set == None:
            return False
        else:
            return True
    def fillSetThenSave(self, image):
        if self.img_set != None  and len(self.img_set) >= gif_frames:
            print len(self.img_set)
            self.img_set._write_gif(filename=( "output/"+self.file_name + ".gif"),\
                duration=(gif_frameRate), dither=2) #
            return self.img_set
        if self.img_set != None:
            self.img_set.append(image)
            return None

    #def playFromGif(self, ):
    def resetGifSet(self):
        self.start_timer = None # reassign start_timer and img_set 
        self.img_set = None # 

    def frameTimer(self):
        if self.start_timer == None:
            return False
        elif self.start_timer != None:
            if time.time() - self.start_timer >= gif_frameRate:
                self.start_timer = time.time()
                return True
            else:
                return False

    def getNewImage(self):
        img = self.cam.getImage()

        if(self._key):
            return img
        else:
            img = img - img.colorDistance(Color.RED) #RED SEGMENTATION
            return img



#make camera obj
cam1 = CameraCapture(1)
#width = cam1.width
#height = cam1.height

disp = Display(flags=pg.FULLSCREEN ,title='Enter The Virtuality!' , resolution = (1280 , 1024))

print("\n >>>Right click on the Image to exit!")
while disp.isNotDone():
    img1 = cam1.getNewImage()
    dwn = disp.leftButtonDownPosition()

    if dwn != None and cam1.gifSetExistsBool() == False:
        cam1.makeGifSet() # create file_name, img_set, start_timer  


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

    img1.save(disp)
    #disp.writeFrame(img1, fit=False)

    if disp.mouseRight:
        pass








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