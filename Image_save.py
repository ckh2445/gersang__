import threading
import pygetwindow as gw
import numpy as np
from PIL import ImageGrab
import cv2
import time

class Image_Save_Thread(threading.Thread):
    def __init__(self):
        super().__init__()
        #self.update()
        self.i=0
        
    def update(self):
        while 1:
            self.var = gw.getWindowsWithTitle('Gersang')[0] # Gersang 창 
            #90 180 960 610
            self.bx= self.var.left
            self.by= self.var.top
            
            self.bbox1 = (self.bx+90,self.by+180,self.bx+960,self.by+610) #image box
            self.img = np.array(ImageGrab.grab(self.bbox1))
            self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

            cv2.imwrite('images/' + str(self.i) + '.jpg', self.img)
            self.i += 1
            time.sleep(1)
            
if __name__ == '__main__':
    Image_save_thread = Image_Save_Thread()
    Image_save_thread.update()