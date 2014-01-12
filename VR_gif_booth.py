#!/usr/bin/env python

import sys
import time
import uuid
import time
import string 
import argparse
from SimpleCV import *


parser = argparse.ArgumentParser()
parser.add_argument("-frames", "--gif_frames", help="How many frames to record per animated gif.", default=16)
parser.add_argument("-speed" , "--gif_frameSpeed", help="How long between each gif frame in seconds.", default=0.4)
parser.add_argument("-resolution", "--video_resolution", help="""The video feed is downsampled to this resolution. Gifs are saved at this resolution! Format="[width,height]" """, default=[320,240])
parser.add_argument("-camera", "--camera_selector", help="This selects which camera to use on setups with more than one camera device. Requires initiger.", default=0)
parser.add_argument("-display, --display_resolution", help="""The resolution of the display. The video feed will attemp to scale to this resolution. Value can be less than physical display resolution. It's a very good idea to match the aspect ratio of the of the video feed! Format="[width,height]" """, default=[1000,750])
parser.add_argument("-output", "--gif_output_directory", help="Where to save gifs.")


args = parser.parse_args()





if __name__ == '__main__':
    print "herrro"

# Init camera 
cam1 = CameraCapture(index=args.camera_selector, width=args.video_resolution[0], height=args.video_resolution[1], gif_frameSpeed=args.gif_frameSpeed)

# Init display
# The display resolution should match or fit within your display. The images capture
# by the camera will be scaled to fit the display.
disp = Display(flags=pg.FULLSCREEN , resolution = (args.display_resolution[0] , args.display_resolution[1]))

class CameraCapture():

    """
    The images captured by the camera will scale to the resolution provided. 
    """

    def __init__(self, index, width, height, gif_frameSpeed):
        self.width = width
        self.height = height
        self.cam = Camera(index, prop_set={"width":self.width,"height":self.height})
        self.gif_frameSpeed = gif_frameSpeed

        self.img_set = None 
        self.start_timer = None
        self.screen_text1 = ""
        self.countdown = None
        self._fr_disp = None # when in use this will contain a tuple that contains and timevalue and function to evaluate whether a preassigned amount of time has passed
        self.framerate_option_list = [0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
        self.replay_mode = False

    def getNewImage(self):
        img = self.cam.getImage()

        img.getDrawingLayer().selectFont("andalemono")
        if self._fr_disp != None and self._fr_disp[1](self._fr_disp[0]):
            img.drawText(text = "gif record time = %s seconds." % (gif_frames*self.gif_frameSpeed ), x = 8, y = 8, color =Color.IVORY, fontsize = 10)


        if self.gifSetExistsBool() and self.replay_mode == False:
            img.getDrawingLayer().circle(center=(self.width-30, self.height-30), radius=20, color=Color.RED, filled=True, alpha=100, antialias=10)          
        if self.screen_text1 != "":
            self.countdown_function()
            if self.screen_text1 != "":
                img.drawText(text = self.screen_text1, x = 20, y = 10, color = Color.GOLD, fontsize = 24)
        return img
    def replayToggle(self, a_bool):
        self.replay_mode = a_bool

    def makeGifSet(self):   
        self.file_name = uuid.uuid4().hex # make a unique file name
        self.img_set = ImageSet(directory=("output/"+ self.file_name  )) # imageClass.ImageSet()  
        self.start_timer = time.time() #assign a value to start_timer

    def resetGifSet(self):
        self.start_timer = None # reassign start_timer and img_set 
        self.img_set = None # 
        self.replay_mode = False

    def gifSetExistsBool(self):
        if self.img_set == None:
            return False
        else:
            return True

    def fillSetThenSave(self, image):
        if self.img_set != None  and len(self.img_set) >= gif_frames:
            self.img_set._write_gif(filename=( "output/"+time.strftime("%Y-%m-%d-%H-%M-%S.gif")),\
                duration=(self.gif_frameSpeed), dither=2) 
            #copy_img_set = copy(self.img_set)
            #self.img_set = None
            #return copy_img_set
            return self.img_set
        if self.img_set != None:
            self.img_set.append(image)
            return None

    def frameTimer(self):
        if self.start_timer == None:
            return False
        elif self.start_timer != None:
            if time.time() - self.start_timer >= self.gif_frameSpeed:
                self.start_timer = time.time()
                return True
            else:
                return False

    def frameSelector(self):
        self._fr_disp = (time.time() , lambda x : x + 1.2 > time.time() )
        if self.gif_frameSpeed > max(self.framerate_option_list) or self.gif_frameSpeed not in self.framerate_option_list:
            self.gif_frameSpeed = self.framerate_option_list[0]
        else:
            while self.framerate_option_list[0] != self.gif_frameSpeed:
                self.framerate_option_list.append(self.framerate_option_list[0]) ; del self.framerate_option_list[0]
            self.framerate_option_list.append(self.framerate_option_list[0]) ; del self.framerate_option_list[0]
            self.gif_frameSpeed = self.framerate_option_list[0]

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
        if isinstance(self.countdown, TimeController):
            if type(self.countdown.check_timer()) in [int, bool]:  
                self.screen_text1 = str(self.countdown.give_value())

            elif self.countdown.check_timer() == None :
                self.countdown , self.screen_text1 = None, ""
                return self.makeGifSet()
            else:
                raise
        else:
            self.countdown = TimeController(1, 3)
            self.screen_text1 = str(repr(self.countdown))
            return self.countdown_function()

    def give_frame_time(self):
        return self.gif_frameSpeed  

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



print("\n >>>Press the ESC key to exit!")
while disp.isNotDone():
    # 1 Get image
    img1 = cam1.getNewImage()   
    mouse2 = disp.rightButtonDownPosition()

    if mouse2 and cam1.gifSetExistsBool() == False:
        cam1.frameSelector()

    dwn = disp.leftButtonDownPosition()
    # 2 Record Gif
    if dwn != None and cam1.gifSetExistsBool() == False:
        cam1.countdown_function()
        #cam1.makeGifSet() # create file_name, img_set, start_timer  
    # 3 Playback gif
    if cam1.frameTimer():
        gifSet = cam1.fillSetThenSave(img1)
        if gifSet != None:
            cam1.replayToggle(True)
            if cam1.give_frame_time() > 1:
                replays = 2
            else:
                replays = 3
            for j in range(0, replays):
                for i in gifSet:
                    i.save(disp)
                    time.sleep(cam1.give_frame_time() )
                else:
                    time.sleep(cam1.give_frame_time()* 2)
            else:
                del gifSet
                print "reset"
                cam1.resetGifSet()
    # 4 Display
    img1.save(disp)

print("\n >>>Program Exitted")
quit()
