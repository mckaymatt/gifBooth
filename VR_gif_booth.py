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
    _screen_text = ""

    """
    The images captured by the camera will scale to the resolution provided. 
    """

    def __init__(self,index,width = _img_res_width , height = _img_res_height):
        self.width = width
        self.height = height
        self.cam = Camera(index, prop_set={"width":self.width,"height":self.height})

        self.img_set = None 
        self.start_timer = None
        self.screen_text1 = ""
        self.output_text = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.countdown = None

    def getNewImage(self):
        img = self.cam.getImage()

        img.getDrawingLayer().selectFont("andalemono")
        if self.gifSetExistsBool():
            img.getDrawingLayer().circle(center=(self.width-30, self.height-30), radius=20, color=Color.RED, filled=True, alpha=100, antialias=10)          
        if self.screen_text1 != "":
            self.countdown_function()
            if self.screen_text1 != "":
                img.drawText(text = self.screen_text1, x = 20, y = 10, color = Color.GOLD, fontsize = 24)
        return img

    def makeGifSet(self):
        self.file_name = uuid.uuid4().hex # make a unique file name
        self.img_set = ImageSet(directory=("output/"+ self.file_name  )) # imageClass.ImageSet()  
        self.start_timer = time.time() #assign a value to start_timer

    def resetGifSet(self):
        self.start_timer = None # reassign start_timer and img_set 
        self.img_set = None # 

    def gifSetExistsBool(self):
        if self.img_set == None:
            return False
        else:
            return True

    def fillSetThenSave(self, image):
        if self.img_set != None  and len(self.img_set) >= gif_frames:
            self.img_set._write_gif(filename=( "output/"+self.file_name + ".gif"),\
                duration=(gif_frameRate), dither=2) 
            return self.img_set
        if self.img_set != None:
            self.img_set.append(image)
            return None

    def frameTimer(self):
        if self.start_timer == None:
            return False
        elif self.start_timer != None:
            if time.time() - self.start_timer >= gif_frameRate:
                self.start_timer = time.time()
                return True
            else:
                return False

    def countdown_engage(self, value):
        self.final_text = "VIRTUALIZING"
        value = map(lambda x : str(x), value)
        for i in enumerate(self.final_text):
            stored_char = value[i[0]]
            random_char = random.choice(string.ascii_uppercase)
            if self.output_text[i[0]] == self.final_text[i[0]]:
                continue
            if self.final_text[i[0]] == random_char:
                self.output_text[i[0]] = random_char

            #if self.final_text[i[0]] == random_char:
                #self.output_text[i[0]] = random_char
            #if value[i[0]] in string.ascii_letters:

            #if value[i[0]] == i[1]:
            #    self.output_text[i[0]] = i[1] 
            else:
                self.output_text[i[0]] = value[i[0]]
        if "".join(self.output_text) == self.final_text:
            self.output_text = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            #self.makeGifSet()
            return self.final_text
        else:
            return "".join(self.output_text)

    def countdown_function(self):
        print 1
        if isinstance(self.countdown, TimeController):
            print 2, type(self.countdown.check_timer())
            if type(self.countdown.check_timer()) in [int, bool]:  
                print 3 , str(self.countdown.give_value())
                self.screen_text1 = str(self.countdown.give_value())

            elif self.countdown.check_timer() == None :
                print 4
                self.countdown , self.screen_text1 = None, ""

                return self.makeGifSet()
            else:
                assert 1==2
        else:
            print 5
            self.countdown = TimeController(1, 3)
            self.screen_text1 = str(repr(self.countdown))
            return self.countdown_function()


        # if "<" not in self.screen_text1:
        #     self.screen_text1 = map(lambda x : str(x), self._screen_text)
        #     self.screen_text1.append("<")
        #     return "".join(self.screen_text1)
        # elif self.screen_text1[0] == "<":
        #     self.screen_text1 = self._screen_text
        #     return self.screen_text1
        # else:
        #     self.screen_text1[self.screen_text1.index("<")-1] = "<"
        #     return "".join(self.screen_text1)  

class TimeController():
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

    def give_value(self): 
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
    if dwn != None and cam1.gifSetExistsBool() == False:
        cam1.countdown_function()
        #cam1.makeGifSet() # create file_name, img_set, start_timer  
    # 3 Playback gif
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