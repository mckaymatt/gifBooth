#!/usr/bin/env python
import os
import sys
import time
import uuid
import time
import string 
import argparse
from SimpleCV import *

parser = argparse.ArgumentParser(description='Make a animated gif photo booth.')
parser.add_argument("-frames", "--gif_frames", type=float, default=16, help="How many frames to record per animated gif.")
parser.add_argument("-speed" , "--gif_frameSpeed", type=float, default=0.4, help="How long between each gif frame in seconds.")
parser.add_argument("-video", "--resolution_video",type=int, nargs='+', default=[320,240], help="""The video feed is downsampled to this resolution. Gifs are saved at this resolution! Format= "width height" w/o quotes""")
parser.add_argument("-camera", "--camera_selector", type=int, default=0, help="This selects which camera to use on setups with more than one camera device. Requires initeger.")
parser.add_argument("-display", "--display_size", type=int, nargs='+', default=[1000,750], help="""The resolution of the display. The video feed will attemp to scale to this resolution. Value can be less than physical display resolution. It's a very good idea to match the aspect ratio of the of the video feed! Format= "width height" w/o quotes """)
parser.add_argument("-output", "--gif_output_directory", default=os.path.abspath("output"), help="Where to save gifs.")


args = parser.parse_args()

print args


if __name__ == '__main__':
    print "herrro"

if args.gif_output_directory != os.path.abspath("output") or not os.path.isdir(args.gif_output_directory):
    try:
        os.mkdir(args.gif_output_directory)
    except OSError:
        print "The output directory provided appears to be invalid. Enter a valid path to an existing directory."
        quit()
assert os.path.isdir(args.gif_output_directory)

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
            img.drawText(text = "gif record time = %s seconds." % (self.gif_frames*self.gif_frameSpeed ), x = 8, y = 8, color =Color.IVORY, fontsize = 10)

        if self.gifSetExistsBool():
            img.getDrawingLayer().circle(center=(self.width-30, self.height-30), radius=20, color=Color.RED, filled=True, alpha=100, antialias=10)          
        if self.screen_text1 != "":
            self.countdown_initiate()
            if self.screen_text1 != "":
                img.drawText(text = self.screen_text1, x = 20, y = 10, color = Color.GOLD, fontsize = 24)
        return img

    def makeGifSet(self):   
        self.filename = os.path.join(self.gif_output_directory, time.strftime("%Y-%m-%d-%H-%M-%S.gif"))
        self.img_set = ImageSet(directory=self.filename)
        #(os.join(self.gif_output_directory, uuid.uuid4().hex))) # imageClass.ImageSet()  
        self.start_timer = time.time() #assign a value to start_timer

    def resetGifSet(self):
        self.start_timer = None # reassign start_timer and img_set 
        self.img_set = None # 
        self.replay_mode = False

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

    def countdown_initiate(self):
        if isinstance(self.countdown, TimeController):
            if type(self.countdown.check_timer()) in [int, bool]:  
                self.screen_text1 = str(self.countdown.give_value())

            elif self.countdown.check_timer() == None :
                self.countdown , self.screen_text1 = None, ""
                return self.makeGifSet()

        else:
            self.countdown = TimeController(1, 3)
            self.screen_text1 = str(repr(self.countdown))
            return self.countdown_initiate()

    def give_frame_time(self):
        return self.gif_frameSpeed  

class TimeController():
    """
    Stopwatch Object
    
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
            return self.occurances
        else:
            return False

    def give_value(self): 
        return self.occurances

# Init camera 
cam1 = CameraCapture(index=args.camera_selector, 
    width=args.resolution_video[0], 
    height=args.resolution_video[1], 
    gif_frames=args.gif_frames, 
    gif_frameSpeed=args.gif_frameSpeed, 
    gif_output_directory=args.gif_output_directory)

# Init display
# The display resolution should match or fit within your display. The images capture
# by the camera will be scaled to fit the display.
disp = Display(flags=pg.FULLSCREEN , 
    resolution = (args.display_size[0] , args.display_size[1]))


print("\n >>>Press the ESC key to exit!")

while disp.isNotDone():

    # 1 Get image from camera
    img1 = cam1.getNewImage()   

    # 2 User interface - Select gif frame speed
    mouse2 = disp.rightButtonDownPosition()
    if mouse2 and not cam1.gifSetExistsBool() :
        cam1.frameSelector()

    # 3 User interface - Begin reecording gif
    dwn = disp.leftButtonDownPosition()
    if  dwn and not cam1.gifSetExistsBool():
        cam1.countdown_initiate()
 
    # 4 Send image to display
    img1.save(disp)  

    # 5 Load gif image into gif set. When set is full, save gif file, then return image set. 
    if cam1.frameTimer():
        gifSet = cam1.fillSetThenSave(img1)

    # 6 When an image set is present, sent it to display.
    if gifSet != None:  
        if cam1.give_frame_time() > 0.7:
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
            gifSet = None
            cam1.resetGifSet()


print("\n >>>Program Exitted")
quit()



