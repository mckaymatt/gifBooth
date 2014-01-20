#!/usr/bin/env python
import os
import sys
import time
import uuid
import time
import string 
import argparse
import types
from SimpleCV import *


class CameraCapture():

    """
    The images captured by the camera will scale to the resolution provided. 
    """

    def __init__(self, index, width, height, gif_frames, gif_frameSpeed, gif_output_directory):
        self.width = width
        self.height = height
        self.cam = Camera(index, prop_set={"width":self.width,"height":self.height})
        self.gif_frames = gif_frames
        self.gif_frameSpeed = gif_frameSpeed
        self.gif_output_directory = gif_output_directory
        self.framerate_option_list = [0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]

        self.img_set = None 
        self.start_timer = None
        self.screen_text1 = ""
        self.countdown = None
        self._fr_disp = None 

    def getNewImage(self):
        """
        Gets an image from the camera and then applies drawing layers
        """
        img = self.cam.getImage()
        img.getDrawingLayer().selectFont("andalemono")

        if self._fr_disp != None and self._fr_disp[1](self._fr_disp[0]): # Displays frameSelector changes 
            img.drawText(text = "gif record time = %s seconds." % (self.gif_frames*self.gif_frameSpeed ), x = 8, y = 8, color =Color.IVORY, fontsize = 10)

        if self.gifSetExistsBool(): # Displays "Now Recording" indicator
            img.getDrawingLayer().circle(center=(self.width-30, self.height-30), radius=20, color=Color.RED, filled=True, alpha=100, antialias=50)  

        if self.screen_text1 != "": # Displays countdown
            self.countdown_initiate()
            if self.screen_text1 != "":
                img.drawText(text = self.screen_text1, x = 20, y = 10, color = Color.GOLD, fontsize = 24)

        return img

    def makeGifSet(self):   
        """
        creats a file name, image set, and starts a stopwatch obj
        """
        self.filename = os.path.join(self.gif_output_directory, time.strftime("%Y-%m-%d-%H-%M-%S.gif"))
        self.img_set = ImageSet(directory=self.filename)
        self.start_timer = TimeController(self.gif_frameSpeed, self.gif_frames+1) 

    def resetGifSet(self):
        """
        reassigns objects back to none which are 
        """
        self.start_timer = None # reassign start_timer and img_set 
        self.img_set = None 

    def gifSetExistsBool(self):
        if self.img_set != None: 
            return True

    def fillSetThenSave(self, image):
        if self.img_set != None  and len(self.img_set) >= self.gif_frames:
            self.img_set._write_gif(filename=(self.filename), duration=(self.gif_frameSpeed), dither=2) 
            return self.img_set

        if self.img_set != None:
            image.clearLayers()
            self.img_set.append(image)
            return None

    def frameTimer(self):
        if self.start_timer == None:
            return None
        elif type(self.start_timer.check_timer()) == int:
            return True
        else:
            False


    def frameSelector(self):
        """
        Method for changing the gif frame rate. This allows users to control how long a gif records.
        Allows for continuity between a custom framespeed that was provided as an argument and is outside the range of framerate_option_list, and predefined framerate_option_list. 
        """ 
        self._fr_disp = (time.time() , lambda x : x + 1.2 > time.time()) # list containing value and function equivilant to [time at creation , lambda function that returns true if 1.2 seconds have passed since object creation]. Used to control how long the new framepeed should be displayed to users. 
        if self.gif_frameSpeed not in self.framerate_option_list: #   
            self.gif_frameSpeed = self.framerate_option_list[0]
        else:
            while self.framerate_option_list[0] != self.gif_frameSpeed: 
                self.framerate_option_list.append(self.framerate_option_list.pop(0)) # cycle framerate list until the current item is found
            self.framerate_option_list.append(self.framerate_option_list.pop(0)) # advance the list once
            self.gif_frameSpeed = self.framerate_option_list[0] # reassign gif framespeed

    def countdown_initiate(self): 
        """
        Controls a timed countdown that is sent to the display. 
        Initiate gif creation upon compleation. 
        """

        if isinstance(self.countdown, TimeController):
            if type(self.countdown.check_timer()) in [int, bool]:  
                self.screen_text1 = str(self.countdown.give_value())

            elif self.countdown.check_timer() in [None, 0] :
                self.countdown , self.screen_text1 = None, ""
                return self.makeGifSet()

        else:
            self.countdown = TimeController(1, 3)
            return self.countdown_initiate()

    def give_frameSpeed(self):
        return self.gif_frameSpeed  

class TimeController():
    """
    Create a stopwatch object
    
    check_timer behavior:
    Returns integer (remaining occurances) if the timer is active and the predefined interval has ellapsed.
    Returns False if the timer is acitive but the predefined interval has not ellapsed.
    Returns None if the timer is no longer active
    """
    def __init__(self, interval, occurances=1):
        self.start_time = time.time()
        self.interval = interval - 0.005 # very scientific fudge factor 
        self.occurances = occurances

    def check_timer(self):
        if not self.occurances: 
            return 
        elif time.time() - self.start_time >= self.interval:
            self.occurances -= 1
            self.start_time = time.time()
            return int(self.occurances)
        else:
            return False

    def give_value(self): 
        return self.occurances

# Create argument parser
parser = argparse.ArgumentParser(description='Make a animated gif photo booth.')
parser.add_argument("-frames", "--gif_frames", type=float, default=16, help="How many frames to record per animated gif.")
parser.add_argument("-frameSpeed" , "--gif_frameSpeed", type=float, default=0.4, help="How long between each gif frame in seconds.")
parser.add_argument("-video", "--resolution_video",type=int, nargs='+', default=[320,240], help="""The video feed is downsampled to this resolution. Gifs are saved at this resolution! Format= "width height" w/o quotes""")
parser.add_argument("-camera", "--select_camera", type=int, default=0, help="This selects which camera to use on setups with more than one camera device. Requires initeger.")
parser.add_argument("-display", "--resolution_display", type=int, nargs='+', default=[1000,750], help="""The resolution of the display. The video feed will attemp to scale to this resolution. Value can be less than physical display resolution. It's a very good idea to match the aspect ratio of the of the video feed! Format= "width height" w/o quotes """)
parser.add_argument("-directory", "--gif_output_directory", default=os.path.abspath("output"), help="Where to save gifs. Default is a directory called output in the current working directory")


args = parser.parse_args()
print args

if args.gif_output_directory != os.path.abspath("output") or not os.path.isdir(args.gif_output_directory):
    try:
        os.mkdir(args.gif_output_directory)
    except OSError:
        print "The output directory provided appears to be invalid. Enter a valid path to an existing directory."
        quit()



# Init camera 
cam1 = CameraCapture(index=args.select_camera, 
    width=args.resolution_video[0], 
    height=args.resolution_video[1], 
    gif_frames=args.gif_frames, 
    gif_frameSpeed=args.gif_frameSpeed, 
    gif_output_directory=args.gif_output_directory)

# Init display
# The display resolution should match or fit within your display. The images capture
# by the camera will be scaled to fit the display.
disp = Display(flags=pg.FULLSCREEN , 
    resolution = (args.resolution_display[0] , args.resolution_display[1]))


print("\n >>>Press the ESC key to exit!")
countFR = [float(time.time()) , lambda x : (x + 1.0) < time.time(), 0]
count = 0
count_of_counts = 0
overall_count = float(time.time())
while disp.isNotDone(): 
    count += 1
     


    if countFR[1](countFR[0]) == True:
        print count - countFR[2] 
        countFR[0] = float(time.time())
        countFR[2] = count
        count_of_counts += 1
         

    # 1 Get image from camera
    img1 = cam1.getNewImage()   

    # 2 User interface - Select gif frame speed with left mouse
    mouse2 = disp.rightButtonDownPosition()
    if mouse2 and not cam1.gifSetExistsBool() :
        cam1.frameSelector()

    # 3 User interface - Record gif after displaying a countdown with right mouse
    dwn = disp.leftButtonDownPosition()
    if  dwn and not cam1.gifSetExistsBool():
        cam1.countdown_initiate()
 
    # 4 Send image to display
    img1.save(disp)  

    # 5 Load gif images into gif set. When set is full, save gif file, then return image set. 
    gifSet = None
    if cam1.frameTimer() == True:
        gifSet = cam1.fillSetThenSave(img1)

    # 6 When an image set is present, replay it to the display.
    if gifSet != None:  
        if cam1.give_frameSpeed() > 0.7: # Only replay a gif twice if it is longer.
            replays = 2 
        else:
            replays = 3
        for j in range(0, replays): 
            for i in gifSet:
                i.save(disp)
                time.sleep(cam1.give_frameSpeed())
            else:
                time.sleep(cam1.give_frameSpeed() * 2) # pause between replays
        else:
            gifSet = None
            cam1.resetGifSet() 


print("\n >>>Program Exitted")
print count_of_counts
print time.time() - overall_count
quit()



