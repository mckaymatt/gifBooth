#!/usr/bin/env python
import os
import sys
import time
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

        # Apply frameSelector changes
        if self._fr_disp != None and self._fr_disp[1](self._fr_disp[0]):  
            img.drawText(text = "gif record time = %s seconds." % (self.gif_frames*self.gif_frameSpeed ), x = 8, y = 8, color =Color.IVORY, fontsize = 10)

        # Apply "Now Recording" indicator
        if self.gifSetExistsBool(): 
            img.getDrawingLayer().circle(center=(self.width-30, self.height-30), radius=20, color=Color.RED, filled=True, alpha=100, antialias=50)  

        # Apply countdown
        if self.screen_text1 != "": 
            self.countdown_initiate()
            if self.screen_text1 != "":
                img.drawText(text = self.screen_text1, x = 20, y = 10, color = Color.GOLD, fontsize = 24)

        #return img
        return img

    def makeGifSet(self):   
        """
        creats a file name, image set, and stopwatch. 
        An ImageSet is an image handling SimpleCV class that inherits from the list class. 
        """
        self.filename = os.path.join(self.gif_output_directory, time.strftime("%Y-%m-%d-%H-%M-%S.gif"))
        self.img_set = ImageSet(directory=self.filename)
        self.start_timer = TimeController(self.gif_frameSpeed, self.gif_frames+1) 

    def frame_timeGifFrames(self):
        """
        Uses instance of type TimeController to regulate when images are passed to makeGifSet.
        """

        if self.start_timer == None:
            return None
        elif type(self.start_timer.check_timer()) == int:
            return True
        else:
            False

    def frame_fillImageSetThenSave(self, image):
        """
        Used to save images for the gif. This method takes an image and append it to an ImageSet. 
        An ImageSet has the data structure of a Python list, but it can store images. 
        Once the length of the ImageSet equals the predefined number of gif frames, the ImageSet is saved as a gif, and then the ImageSet is returned. 
        """
        if self.img_set != None  and len(self.img_set) >= self.gif_frames:
            self.img_set._write_gif(filename=(self.filename), duration=(self.gif_frameSpeed), dither=2) 
            return self.img_set

        if self.img_set != None:
            image.clearLayers()
            self.img_set.append(image)
            return None

    def gifSetExistsBool(self):
        """
        If gif set exists than user interface should be disabled. This method returns True if the gif_set exists.
        """
        if self.img_set != None: 
            return True

    def resetGifSet(self):
        """
        Sets timer and img_set back to None.
        """
        self.start_timer = None # reassign start_timer and img_set 
        self.img_set = None 

    def frameSelector(self):
        """
        Method for changing the gif frame rate. This allows users to control how long a gif records.
        Allows for continuity between a custom framespeed that was provided as an argument and is outside the range of framerate_option_list, and predefined framerate_option_list. 
        """ 
        self._fr_disp = (time.time() , lambda x : x + 1.2 > time.time()) # list containing value and function equivalent to [time at creation , lambda function that returns true if 1.2 seconds have passed since object creation]. Used to control how long the new framepeed should be displayed to users. 
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
        Initiate gif creation upon completion. 
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
        """
        return framespeed
        """
        return self.gif_frameSpeed  

class TimeController():
    """
    Create a stopwatch object
    
    check_timer behavior:
    Returns integer (remaining occurrences) if the timer is active and the predefined interval has elapsed.
    Returns False if the timer is active but the predefined interval has not elapsed.
    Returns None if the timer is no longer active.
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

def main():
    """
    Launches gif booth
    """

    # Make locate output directory. Attempt to make it if it doesn't exist.
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

    while disp.isNotDone(): 
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

        # 5 Once the ImageSet has been created, start loading it with images. 
        if cam1.gifSetExistsBool():
            if cam1.frame_timeGifFrames() == True: # Controls the interval at which images are sent to ImageSet
                ImageSet_for_replay = cam1.frame_fillImageSetThenSave(img1) # will return an ImageSet once the ImageSet contains predefined number of frames

        # 6 When an ImageSet is present, replay it to the display.
                if ImageSet_for_replay != None:  
                    if cam1.give_frameSpeed() > 0.7: # Only replay a gif twice if it is longer.
                        replays = 2 
                    else:
                        replays = 3
                    for j in range(0, replays): 
                        for i in ImageSet_for_replay:
                            i.save(disp)
                            time.sleep(cam1.give_frameSpeed())
                        else:
                            time.sleep(cam1.give_frameSpeed() * 2) # pause between replays
                    else:
                        ImageSet_for_replay = None
                        cam1.resetGifSet() 

    print("\n >>>Program Exitted")
    quit()

if __name__ == '__main__':
    # Create argument parser
    parser = argparse.ArgumentParser(description='Make a animated gif photo booth.')
    parser.add_argument("-frames", "--gif_frames", type=float, default=16, help="How many frames to record per animated gif.")
    parser.add_argument("-frameSpeed" , "--gif_frameSpeed", type=float, default=0.4, help="How long between each gif frame in seconds.")
    parser.add_argument("-video", "--resolution_video",type=int, nargs='+', default=[320,240], help="""The video feed is down sampled to this resolution. Gifs are saved at this resolution! Format= "width height" w/o quotes""")
    parser.add_argument("-camera", "--select_camera", type=int, default=0, help="This selects which camera to use on setups with more than one camera device. Requires initeger.")
    parser.add_argument("-display", "--resolution_display", type=int, nargs='+', default=[1000,750], help="""The resolution of the display. The video feed will attempt to scale to this resolution. Value can be less than physical display resolution. It's a very good idea to match the aspect ratio of the of the video feed! Format= "width height" w/o quotes """)
    parser.add_argument("-directory", "--gif_output_directory", default=os.path.abspath("output"), help="Where to save gifs. Default is a directory called output in the current working directory")
    # assign arguments
    args = parser.parse_args()

    main()
