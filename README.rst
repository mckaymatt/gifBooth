gifBooth 
-----------------------------------------
Set up an animated gif photo booth at your next party.

What Is This?
~~~~~
gifBooth uses a computer vision library to record, save and playback, animated gifs. 
The gifs produced by gifBooth can easily be uploaded to the internet.

Hardware Requirements
~~~~~

*  A personal computer
*  Webcam
*  Two-button mouse

Software Requirements
~~~~~
*  SimpleCV - http://www.simplecv.org/
*  Python 2.7

Starting gifBooth
~~~~~

  `$ python gifBooth.py <optional arguments>`

I highly recommend maintaining a consistent aspect ratio between the video feed and the display. For example, I sample the video feed at 320pix * 240pix which has an aspect ratio of 4:3. My monitor is 1920pix * 1080pix so it's native aspect ratio is 16:9. In order to display the video feed without stretching the image, I crop the display to 4:3 by trimming the width down to 1440pix using the arguments `-video 320 240 -display 1440 1080` 

See http://en.wikipedia.org/wiki/File:Vector_Video_Standards4.svg

How Users Interact With gifBooth
~~~~~
`Left Mouse Button` - Record gif. After recording, the gif is played back multiple times.

`Right Mouse Button` - Change time delay between each gif frame. The range of options is between 0.1 seconds (10 FPS) to 1 second (1 FPS). 

`Escape Key` - Exit gifBooth

Notes
~~~~~
Installing SimpleCV, at least on Mac 10.7, was somewhat difficult. If I were doing this again I would have just used OpenCV. That being said, SimpleCV does have some nice features that can make some projects easier. 

Usage
~~~~~

::

    usage: VR_gif_booth.py [-h] [-frames GIF_FRAMES] [-frameSpeed GIF_FRAMESPEED]
                           [-video RESOLUTION_VIDEO [RESOLUTION_VIDEO ...]]
                           [-camera SELECT_CAMERA]
                           [-display RESOLUTION_DISPLAY [RESOLUTION_DISPLAY ...]]
                           [-directory GIF_OUTPUT_DIRECTORY]

    Make a animated gif photo booth.

    optional arguments:
      -h, --help            show this help message and exit
      -frames GIF_FRAMES, --gif_frames GIF_FRAMES
                            How many frames to record per animated gif.
      -frameSpeed GIF_FRAMESPEED, --gif_frameSpeed GIF_FRAMESPEED
                            How long between each gif frame in seconds.
      -video RESOLUTION_VIDEO [RESOLUTION_VIDEO ...], --resolution_video RESOLUTION_VIDEO [RESOLUTION_VIDEO ...]
                            The video feed is down sampled to this resolution.
                            Gifs are saved at this resolution! Format= "width
                            height" w/o quotes
      -camera SELECT_CAMERA, --select_camera SELECT_CAMERA
                            This selects which camera to use on setups with more
                            than one camera device. Requires initeger.
      -display RESOLUTION_DISPLAY [RESOLUTION_DISPLAY ...], --resolution_display RESOLUTION_DISPLAY [RESOLUTION_DISPLAY ...]
                            The resolution of the display. The video feed will
                            attempt to scale to this resolution. Value can be less
                            than physical display resolution. It's a very good
                            idea to match the aspect ratio of the of the video
                            feed! Format= "width height" w/o quotes
      -directory GIF_OUTPUT_DIRECTORY, --gif_output_directory GIF_OUTPUT_DIRECTORY
                            Where to save gifs. Default is a directory called
                            output in the current working directory