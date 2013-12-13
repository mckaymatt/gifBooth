#!/usr/bin/env python

import sys
import time
import uuid
#@PydevCodeAnalysIsIgnore

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
# screen rez 1280 1024 camera rez 1024 768      

class CameraCapture():
                
        _key = True
        _width = 320#800#1280  
        _height = 240#600#1024

        def __init__(self,index,width = 320 , height = 240):
                self.width = width
                self.height = height
                self.cam = Camera(index, prop_set={"width":self.width,"height":self.height})

                self.img_set = None 
                        
        def setKey(self):
                if(self._key):
                        self._key = False
                else:
                        self._key = True

        def makeGifSet(self):
                self.file_name = uuid.uuid4().hex # make a unique folder
                self.img_set = ImageSet(directory=("output/"+ self.file_name  ))
                #ImageSet(directory=("output/" ))#+ self.file_name ))

        def gifOutputImageSetExprs(self):
                return ImageSet(directory=("output/"+ self.file_name  ))


        def gifSetExistsBool(self):
                if self.img_set == None:
                        return False
                else:
                        return True
        def fillSetThenSave(self, image):
                if self.img_set != None and len(self.img_set) >= gif_frames:

                        print len(self.img_set)
                        #self.img_set.save(str("output/"+ self.file_name + ".gif"), dt=gif_frameRate)
                        self.img_set.save(str("output/"+ self.file_name + ".gif"), dt=gif_frameRate)
                        return self.img_set
                        self.img_set = None
                        return ImageSet().load("output/"+ self.file_name + ".gif")
                        #return self.gifOutputImageSetExprs()._read_gif(str(self.file_name + ".gif"))

                        print len(self.img_set), os.path.getsize(str("output/"+ self.file_name + ".gif"))
                        assert len(self.img_set) <= 16 
                        assert os.path.getsize(str("output/"+ self.file_name + ".gif")) < 15427450
                        return self.img_set
                        self.img_set == None
                elif self.img_set != None:
                        print len(self.img_set)
                        self.img_set.append(image)
                        return None

        #def playFromGif(self, ):
        def resetGifSet(self):
                self.img_set = None

        def getNewImage(self):
                img = self.cam.getImage()

                if(self._key):
                        return img
                else:
                        img = img - img.colorDistance(Color.RED) #RED SEGMENTATION
                        return img


#make camera obj
cam1 = CameraCapture(1)


width = cam1.width
height = cam1.height
disp = Display(flags=pg.FULLSCREEN ,title='Enter The Virtuality' , resolution = (width, height))


print("\n >>>Right click on the Image to exit!")
count = 0
while disp.isNotDone():
        count += 1
        #if count > 24*30:

         #       del cam1 ; quit()
        img1 = cam1.getNewImage()
        dwn = disp.leftButtonDownPosition()

        if dwn != None and cam1.gifSetExistsBool() == False:
                cam1.makeGifSet()
                #cam1.setKey()
        #img1.drawText("Camera 1",100,400,fontsize=40,color=Color.BLUE)


        
        if count % 18 == 0:
                gifSet = cam1.fillSetThenSave(img1)
                if gifSet != None:
                        for j in range(0, 3):
                                #quit()
                                for i in gifSet:

                                        i.save(disp)
                                else:
                                        time.sleep(gif_frameRate )
                        else:
                                cam1.resetGifSet()

        img1.save(disp)
        #disp.writeFrame(img1, fit=False)

        if disp.mouseRight:
                del cam1
                break
  #fit* - When fit=False write frame will crop and center the image as best it can.
  #If the image is too big it is cropped and centered. If it is too small
  #it is centered. If it is too big along one axis that axis is cropped and
  #the other axis is centered if necessary."""



print("\n >>>Program Exitted")
quit()


                # if gifSet != None:
                #         print len(gifSet), repr(gifSet) ; quit()
                #         count = 0
                #         for i in gifSet:
                #                 count += 1
                #                 i.save(disp)
                #                 time.sleep(gif_frameRate)
                #                 if count >= gif_frames:
                #                         break
                #         else:
                #                 cam1.resetGifSet()
