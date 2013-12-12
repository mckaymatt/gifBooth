'''
Created on Dec 8, 2013

@author: mattmckay
'''
import sys
import time
import uuid
#@PydevCodeAnalysIsIgnore

from SimpleCV import *
# Initialize the camera 
# screen rez 1280 1024 camera rez 1024 768

class CameraCapture():
                
        _key = True
        _width = 1280  
        _height = 1024


        def __init__(self,index,width = 1280, height = 1024):
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
                self.folder_name = uuid.uuid4().hex # make a unique folder
                self.img_set = ImageSet(directory=str("/output/" + self.folder_name))

        def gifSetExistsBool(self):
                if self.img_set == None:
                        return False
                else:
                        return True

        def fillSetThenSave(self, image):
                if self.img_set != None and len(self.img_set) == 8:
                        self.img_set.save(str("output/"+ self.folder_name + ".gif"), dt=0.4)
                        return self.img_set._read_gif(str(self.folder_name + ".gif"))
                        
                        self.img_set = None
                elif self.img_set != None:
                        self.img_set.append(image)
                        return None

        def makeVirtualCamAndDisplay(self):
                pass


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
disp = Display(flags=pg.FULLSCREEN,title='Enter The Virtuality')


print("\n >>>Right click on the Image to exit!")
count = 0
while disp.isNotDone():
        count += 1
        if count == 9999:
                count = 0
        # if count == 500:
        #         print "Time's Up!"
        #         break

        img1 = cam1.getNewImage()

        dwn = disp.leftButtonDownPosition()

        if dwn != None and cam1.gifSetExistsBool() == False:
                cam1.makeGifSet()
                #cam1.setKey()
        #img1.drawText("Camera 1",100,400,fontsize=40,color=Color.BLUE)


        img1.save(disp)
        if count % 11 == 0:
                returnVal = cam1.fillSetThenSave(img1)
                if returnVal != None:
                        for i in returnVal:
                                i.save(disp)
                                time.sleep(0.4)



        if disp.mouseRight:
                break
print("\n >>>Program Exitted")
quit()

