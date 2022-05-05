from PyQt5.QtCore import pyqtSignal,QObject

class Auto(QObject): #Auto Thread
    finished = pyqtSignal() # give worker class a finished signal
    Auto_running = pyqtSignal(str) #
    
    def __init__(self, parent = None):
        QObject.__init__(self, parent = parent)
        self.continue_run = True     ##### provide a bool run condition for the class
    
    def stop(self):
        self.continue_run = False # set the run condition to false on stop
        
    def Start_Auto(self):
        self.i = 3
        while self.continue_run:     ##### give the loop a stoppable condition