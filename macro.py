from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt,QCoreApplication
import sys
from win32api import GetSystemMetrics
import datetime
import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab
import time
import random
from ctypes import windll
from PyQt5.QtCore import pyqtSignal,QThread
import auto_thread

form_class = uic.loadUiType("ui\my_design.ui")[0]

di = windll.LoadLibrary('c:\DD64.dll')

methods = ['cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR_NORMED','cv2.TM_SQDIFF_NORMED']
stylesheet1 = ("color: #dc3545;"
                "border-color: #dc3545;"
                "background-color: whitesmoke;"
                "border-radius: 15px;")
stylesheet2 = ("background-color : rgba(0, 0, 0, 50);"
            "border: 2px solid white;"
            "color: white;"
            "border-radius: 10px;")


#ser = serial.Serial("COM5",9600) #serial 통신

net = cv2.dnn.readNet("Monster_custom_last.weights", "Monster_custom.cfg")
classes = []
with open("classes.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))


class Main_Form(QMainWindow, form_class): #design.Ui_mainWindow
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint) # 윈도우 항상 위에 있고 제목표시줄 수정
        
        stop_signal = pyqtSignal()  #make a stop signal to communicate with the worker in another thread
        #self.text = QPushButton
        #self.text.clear
        
        #Btuuon 리스너
        self.BT_Character_Name_Search.clicked.connect(self.BT_Character_Name_Search_Clicked)
        self.BT_Exit.clicked.connect(QCoreApplication.instance().quit)


        # self.timer = QBasicTimer()
        # self.step = 0
        # self.index = 0
        
        # self.Init() #초기화 함수
        # self.warning = Warning()
        # for x in self.Character_list_dic: #BT_Character들을 dic으로 저장한다
        #     self.Character_list_dic[str(x)].setEnabled(False)
        
        # if self.Characters_info == None:
        #     pass
        # else:
        #     for index,key in enumerate(self.Characters_info):
        #         if index == len(self.Characters_info):
        #             break
        #         self.Character_list_dic[str(index)].setText(str(key) + '\n' + str(self.Characters_info[key]['Lv'])) #Chrarcter_list[index]의 Text를 닉네임과 레벨로 바꿈
        #         self.Character_list_dic[str(index)].setEnabled(True) #dic에 Character_list[index] 활성화
        #         self.Character_list_dic[str(index)].setStyleSheet(stylesheet1)
        #         #self.Characters_form[key] = self.BT_Character_list_create(key)
        #         self.Character_list_dic[str(index)].clicked.connect(lambda _, b= key: self.BT_Character_list_Clicked(b)) #람다식을 이용한 매개변수 전달  (람다를 이용하지 않으면 매개변수 전달이 까다롭다)
    
        # self.thread = QThread()
        # self.auto = Auto()
        # self.stop_signal.connect(self.auto.stop)  # connect stop signal to worker stop method
        # self.auto.moveToThread(self.thread)

        # self.auto.finished.connect(self.thread.quit)  # connect the workers finished signal to stop thread
        # self.auto.finished.connect(self.auto.deleteLater) # connect the workers finished signal to clean up worker
        # self.thread.finished.connect(self.thread.deleteLater) # connect threads finished signal to clean up thread

        # self.thread.started.connect(self.auto.Start_Auto)
        # self.thread.finished.connect(self.auto.stop)
        # self.auto.Auto_running.connect(self.Update_Log)
        # self.thread.start()

        # ##### thread finish and Button Setting 
        # self.thread.finished.connect(
        #     lambda: self.BT_Start_Auto.setEnabled(True)
        # )
        # self.thread.finished.connect(
        #     lambda: self.BT_Start_Auto.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 80); border: 2px solid white; color: white; border-radius: 20px;}')
        # )

        # ##### Log Append 
        # self.Log.append(str(self.Log_Count) + ": " + "Start Auto")
        # self.Log_Count += 1

        # ##### Start Auto Button Setting 
        # self.BT_Start_Auto.setEnabled(False)
        # self.BT_Start_Auto.setStyleSheet('QPushButton {background-color: rgba(0, 0, 0, 200); border: 2px solid white; color: white; border-radius: 20px;}')
        
    def BT_Exit_Clicked(self):
        QApplication.quit()
    #Test  
    
    def Stop_Auto_Clicked(self): #Stop Auto Button Event
        self.stop_signal.emit()  # emit the finished signal on stop

        ##### Log Append
        self.Log.append(str(self.Log_Count) + ": " + "Stop Auto")
        self.Log_Count += 1
        
        ##### Start Auto Button Setting
    def BT_Character_list_Clicked(self,char_str): #버튼 리스너 연결 함수 매개변수로는 str 
        #print(char_str)
        self.char_form = Sub_form.Character_Form(char_str)
        self.char_form = self.char_form.load_data()
        
    #Test End
    def BT_Character_Name_Search_Clicked(self): #BT_Character_Name_Search_Clicked
        self.var = gw.getWindowsWithTitle('Gersang')[0] # Gersang 창 
        #90 180 960 610
        self.bx= self.var.left
        self.by= self.var.top
        
        self.bbox1 = (self.bx+90,self.by+180,self.bx+960,self.by+610) #image box
        self.img = np.array(ImageGrab.grab(self.bbox1))
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)

        height, width, channels = self.img.shape
        
        # Detecting objects
        blob = cv2.dnn.blobFromImage(self.img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # 정보를 화면에 표시
        class_ids = []
        confidences = []
        images_Result = []
        last_result = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.7:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # 좌표
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
            
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.7,0.6)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                last_result.append([x, y, w, h])
                #self.MouseMove(self.position_x,self.position_y)
        #         label = str(classes[class_ids[i]])
        #         color = colors[0]
        #         cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
        #         cv2.putText(self.img, label, (x - 5, y - 10 ), font, 1.5, color, 3)
        # cv2.imshow("Image", self.img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        if len(boxes) > 0:
            x, y, w, h = boxes[0]
            self.position_x = int(x+(w/2))
            self.position_y = int(y+(h/2)+20)
            print(boxes[0])
            try:
                di.DD_mov(int(self.bx+90),int(self.by+180))
                time.sleep(0.2)
                di.DD_movR(int(self.position_x)+20, int(self.position_y)+20)
                time.sleep(0.2)
                di.DD_btn(4)
                time.sleep(0.1)
                di.DD_btn(8)
            except:
                print("error")
            label = str(classes[class_ids[i]])
            color = colors[0]
            cv2.rectangle(self.img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(self.img, label, (x - 5, y - 10 ), font, 1.5, color, 3)
            cv2.circle(self.img, (self.position_x,self.position_y), 5, (0,0,255), -1)
            
        cv2.imshow("Image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
            
    def MouseMove(self,x,y):
        ser.write(str.encode("M"+x+"_"+y))
        time.sleep(0.1)
        ser.write(str.encode("0"))
        
    def keyPressEvent(self, e): #Esc
        if e.key() == Qt.Key_Escape:
            self.close()
    
    def Init(self): # BT_Character의 버튼들을 초기화해준다.
        self.Character_list_dic = {}
        self.Character_list_dic["0"] = self.BT_Character0
        self.Character_list_dic["1"] = self.BT_Character1
        self.Character_list_dic["2"] = self.BT_Character2
        self.Character_list_dic["3"] = self.BT_Character3
        self.Character_list_dic["4"] = self.BT_Character4
        self.Character_list_dic["5"] = self.BT_Character5
        self.Character_list_dic["6"] = self.BT_Character6
        self.Character_list_dic["7"] = self.BT_Character7
        self.Character_list_dic["8"] = self.BT_Character8
        self.Character_list_dic["9"] = self.BT_Character9
        self.Character_list_dic["10"] = self.BT_Character10
        self.Character_list_dic["11"] = self.BT_Character11
        self.Character_list_dic["12"] = self.BT_Character12
        self.Character_list_dic["13"] = self.BT_Character13
        self.Character_list_dic["14"] = self.BT_Character14
        self.Character_list_dic["15"] = self.BT_Character15
        self.Character_list_dic["16"] = self.BT_Character16
        self.Character_list_dic["17"] = self.BT_Character17
        self.Character_list_dic["18"] = self.BT_Character18
        self.Character_list_dic["19"] = self.BT_Character19
        self.Character_list_dic["20"] = self.BT_Character20
        self.Character_list_dic["21"] = self.BT_Character21
        self.Character_list_dic["22"] = self.BT_Character22
        self.Character_list_dic["23"] = self.BT_Character23
        self.Character_list_dic["24"] = self.BT_Character24
        self.Character_list_dic["25"] = self.BT_Character25
        self.Character_list_dic["26"] = self.BT_Character26
        self.Character_list_dic["27"] = self.BT_Character27
        self.Character_list_dic["28"] = self.BT_Character28
        self.Character_list_dic["29"] = self.BT_Character29
            
    def Character_list_dic_Init(self):
        for x in self.Character_list_dic:
            self.Character_list_dic[str(x)].setText("Character" + "_" + str(x))
            self.Character_list_dic[str(x)].setStyleSheet(stylesheet2)
            
            #print(x)
        #self.Character_list_dic.clear()
        
    def timerEvent(self, e): #QBasic 함수
        if self.step >= 100: # ProgressBar가 100% 이상이면 종료 후 아래 코드 실행
            self.timer.stop()
            self.step = 100 
            self.PB_Character.setValue(self.step) # ProgressBar 100% 표시
            self.BT_Character_Name_Search.setText('Search') # BT버튼의 Text를 Search로 바꿈 
            
            #날짜 구하기
            #self.Characters_info["date"] = str(datetime.datetime.now())
            # self.now = datetime.datetime.now()
            # self.next_day = self.now + datetime.timedelta(days=1) #다음날 날짜
            # self.next_day = self.next_day.replace(hour=6, minute=0, second=0, microsecond=0) #시간정리
            # self.Characters_info["next_day"] = str(self.next_day.strftime("%Y-%m-%d %H:%M:%S"))
            
            # self.next_week = str(Cal_Days.GetWeekLastDate())
            # self.next_week = datetime.datetime.strptime(self.next_week, '%Y-%m-%d')
            # self.next_week = self.next_week.replace(hour=6, minute=0, second=0, microsecond=0)
            # self.Characters_info["next_week"] = str(self.next_week)
            
            Save_data(self.Characters_info) #json 저장
                
            #버튼 리스너
            #print(self.Character_list_dic)
            
            for index,key in enumerate(self.Characters_info):
                if index == len(self.Characters_info)-2:
                    break
                try:
                    self.Character_list_dic[str(index)].clicked.disconnect()
                except:
                    pass
                #self.Characters_form[key] = self.BT_Character_list_create(key)
                self.Character_list_dic[str(index)].clicked.connect(lambda _, b= key: self.BT_Character_list_Clicked(b)) #람다식을 이용한 매개변수 전달  (람다를 이용하지 않으면 매개변수 전달이 까다롭다)
            #초기화 시작
            self.BT_Character_Name_Search.setEnabled(True)
            self.Character_list_dic[str(self.index)].setEnabled(False) #마지막 index는 false로 바꿔준다
            self.step = 0
            self.index = 0
            
            self.my_characters.clear()
            #초기화 끝 
            return
        #if self.index == len(self.Characters_info)-2:
        #    self.step = 100
        #print(self.Characters_info)
        #print(self.Character_list_dic[str(self.index)])
        self.Characters_info[self.my_characters[self.index]] = {"Lv" : self.Character.load_level(self.my_characters[self.index])} #변수 index를 따라 모든 캐릭 검색하여 받아옴
        self.Update_str = 'Updating' + '.' * (self.index % 5) # updating... 설정
        self.BT_Character_Name_Search.setEnabled(False) # BT_Searct 버튼 비활성화
        self.BT_Character_Name_Search.setText(self.Update_str) # BT_Search Text변환
        
        #print(self.Characters_info) #캐릭터명 불러오기
        #print(self.Characters_info[self.my_characters[self.index]]) #캐릭터명에 따른 레벨 불러오기
        self.Character_list_dic[str(self.index)].setEnabled(True) #dic에 Character_list[index] 활성화
        self.my_str = str(self.Characters_info[self.my_characters[self.index]]['Lv'])
        self.my_str = self.my_str.replace(",","")
        self.Character_list_dic[str(self.index)].setText(str(self.my_characters[self.index]) + '\n' + self.my_str ) #Chrarcter_list[index]의 Text를 닉네임과 레벨로 바꿈
        self.Character_list_dic[str(self.index)].setStyleSheet(stylesheet1)
        #try:
        #    self.Character_list_dic[str(self.index)].clicked.disconnect() #람다식을 이용한 매개변수 전달  (람다를 이용하지 않으면 매개변수 전달이 까다롭다)
        #except:
        #    pass
        #self.Character_list_dic[str(self.index)].clicked.connect(lambda _, b = self.Character_list_dic[str(self.index)] : self.BT_Character_list_Clicked(b)) #람다식을 이용한 매개변수 전달  (람다를 이용하지 않으면 매개변수 전달이 까다롭다)
        self.index += 1
        self.step = self.step + int(100 / len(self.my_characters)) + 1 #현재 진행상황 구하기
        self.PB_Character.setValue(self.step) #현재 진행상황 표시
        #print(self.Characters_info)

class Logo_Form(QPushButton):
    def __init__(self):
        #self.main_form = main_form
        super().__init__()
        self.btn=QPushButton("Yolo")
        self.btn.resize(40,20)
        self.btn.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.width = int(GetSystemMetrics(0))
        self.btn.move(int(self.width/2),0)
        self.btn.clicked.connect(self.Clicked)
        self.btn.setFont(QFont('Consolas', 11))
        self.btn.setStyleSheet("color: #dc3545;"
                                "border-color: #dc3545;"
                                "background-color: whitesmoke;"
                                "border-radius: 15px;")

        self.btn.show()
        
    def Clicked(self):
        self.window = Main_Form()
        self.window.__init__()
        self.window.show()
        #self.main_form.show()
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = Main_Form()
    btn = Logo_Form()
    
    app.exec_()