import sys
#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import cv2
import math
import os

class ControlWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.cap = None
        self.filename=None
        self.magnification=1
        
        font=QtGui.QFont()
        font.setBold(True)
        
        self.resize(500, 1000)
        self.setWindowTitle('Open Field analysis: Activity')
        
        layout = QtGui.QGridLayout(self)
        self.setLayout(layout)

        self.LableMag = QtGui.QLineEdit(self)
        self.LableMag.setEnabled(False)
        self.LableMag.setGeometry(QtCore.QRect(800, 30, 80, 20))
        self.LableMag.setFrame(False)
        self.LableMag.setText("Video mag.:")
        
        self.videoSize = QtGui.QComboBox(self)
        self.videoSize.addItem("1X")
        self.videoSize.addItem("1.5X")
        self.videoSize.addItem("2X")
        self.videoSize.addItem("3X")
        self.videoSize.addItem("4X")
        self.videoSize.setCurrentIndex(0)
        self.videoSize.setEnabled(True)
        self.videoSize.activated.connect(self.magnific)
        self.videoSize.setGeometry(QtCore.QRect(675, 30, 50, 20))

        self.LablePath = QtGui.QLineEdit(self)
        self.LablePath.setEnabled(False)
        self.LablePath.setGeometry(QtCore.QRect(90, 10, 641, 20))
        self.LablePath.setFrame(False)
                     
        self.open_button = QtGui.QPushButton(self)
        self.open_button.setText("Open Video")
        self.open_button.clicked.connect(self.getfile)
        self.open_button.setGeometry(QtCore.QRect(9, 9, 75, 23)) 
       
        self.save_button = QtGui.QPushButton(self)
        self.save_button.setText("Save data")
        self.save_button.clicked.connect(self.handleSave)
        self.save_button.setGeometry(QtCore.QRect(850, 450, 80, 30))
        self.save_button.setEnabled(False)
        
        self.play_button = QtGui.QPushButton(self)
        self.play_button.setText("Analyze")
        self.play_button.clicked.connect(self.AnalyzeBtn)
        self.play_button.setGeometry(QtCore.QRect(760, 450, 80, 30))
        self.play_button.setEnabled(False)
        
        self.roi_button = QtGui.QPushButton(self)
        self.roi_button.setText("Save Roi")
        self.roi_button.clicked.connect(self.roi_box)
        self.roi_button.setGeometry(QtCore.QRect(670, 450, 80, 30))
                    
        self.pg2_label=QtGui.QLineEdit(self)
        self.pg2_label.setGeometry(QtCore.QRect(650, 10, 320, 20))
        self.pg2_label.setFrame(False)
        self.pg2_label.setEnabled(False)
        self.pg2_label.setText("Tracking:")
        self.pg2_label.setFont(font)
               
        self.pg2 = pg.GraphicsLayoutWidget(self)
        self.pg2.setGeometry(QtCore.QRect(650, 40, 280, 200))
        self.pg2.setBackground(None)
        self.roi2= pg.RectROI([200, 200], [200, 200], pen=(0,9), 
                              movable=False,centered=True, sideScalers=False)     
        self.w1=self.pg2.addPlot()
        self.plot=pg.PlotDataItem(size=3,connect="all", symbolSize=3)
        self.w1.invertY()
        self.w1.addItem(self.plot)
        self.w1.addItem(self.roi2)
        self.roi3=  pg.RectROI([200, 200], [200, 200], pen=(2,9), 
                              movable=False,centered=True, sideScalers=False)
        self.w1.addItem(self.roi3)
        
        self.Options_label=QtGui.QLineEdit(self)
        self.Options_label.setGeometry(QtCore.QRect(670, 270, 320, 20))
        self.Options_label.setFrame(False)
        self.Options_label.setEnabled(False)
        self.Options_label.setText("Options:")
        self.Options_label.setFont(font)
        
        self.proBar_label=QtGui.QLineEdit(self)
        self.proBar_label.setGeometry(QtCore.QRect(670, 500, 320, 20))
        self.proBar_label.setFrame(False)
        self.proBar_label.setEnabled(False)
        self.proBar_label.setText("Progress:")
        self.proBar=QtGui.QProgressBar(self)
        self.proBar.setGeometry(QtCore.QRect(670, 520, 280, 20))
        
        self.sl = QtGui.QSlider(self)
        self.sl.setOrientation(QtCore.Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(255)
        self.sl.setValue(200)
        self.sl.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl.setTickInterval(10)
        self.sl.setGeometry(QtCore.QRect(750, 340, 180, 20))
        self.sl.valueChanged.connect(self.selectionchange)
        self.sl.setEnabled(False)
        
        self.sl_brigth = QtGui.QSlider(self)
        self.sl_brigth.setOrientation(QtCore.Qt.Horizontal)
        self.sl_brigth.setMinimum(0)
        self.sl_brigth.setMaximum(50)
        self.sl_brigth.setValue(10)
        self.sl_brigth.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_brigth.setTickInterval(10)
        self.sl_brigth.valueChanged.connect(self.selectionchange)
        self.sl_brigth.setGeometry(QtCore.QRect(750, 370, 180, 20))
        
        self.sl_rotation = QtGui.QSlider(self)
        self.sl_rotation.setOrientation(QtCore.Qt.Horizontal)
        self.sl_rotation.setMinimum(-180)
        self.sl_rotation.setMaximum(180)
        self.sl_rotation.setValue(0)
        self.sl_rotation.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_rotation.setTickInterval(20)
        self.sl_rotation.valueChanged.connect(self.selectionchange)
        self.sl_rotation.setGeometry(QtCore.QRect(750, 400, 180, 20))
        
        self.Inner_label = QtGui.QLineEdit(self)
        self.Inner_label.setEnabled(False)
        self.Inner_label.setGeometry(QtCore.QRect(670, 230, 80, 20))
        self.Inner_label.setFrame(False)
        self.Inner_label.setText("Inner box (%):")
        
        self.Inner = QtGui.QLineEdit(self)
        self.Inner.setEnabled(True)
        self.Inner.setText("45")
        self.Inner.setGeometry(QtCore.QRect(760, 230, 40, 20))
        self.Inner.setFrame(True)
        
        self.BoxW_label = QtGui.QLineEdit(self)
        self.BoxW_label.setEnabled(False)
        self.BoxW_label.setGeometry(QtCore.QRect(690, 290, 80, 20))
        self.BoxW_label.setFrame(False)
        self.BoxW_label.setText("Width (cm):")
        
        self.BoxW = QtGui.QLineEdit(self)
        self.BoxW.setEnabled(True)
        self.BoxW.setText("80")
        self.BoxW.setGeometry(QtCore.QRect(760, 290, 40, 20))
        self.BoxW.setFrame(True)
        
        self.BoxL_label = QtGui.QLineEdit(self)
        self.BoxL_label.setEnabled(False)
        self.BoxL_label.setGeometry(QtCore.QRect(830, 290, 80, 20))
        self.BoxL_label.setFrame(False)
        self.BoxL_label.setText("Long (cm):")
        
        self.BoxL = QtGui.QLineEdit(self)
        self.BoxL.setEnabled(True)
        self.BoxL.setText("100")
        self.BoxL.setGeometry(QtCore.QRect(895, 290, 40, 20))
        self.BoxL.setFrame(True)
        
        self.thresh_label = QtGui.QLineEdit(self)
        self.thresh_label.setEnabled(False)
        self.thresh_label.setGeometry(QtCore.QRect(670, 340, 80, 20))
        self.thresh_label.setFrame(False)
        self.thresh_label.setText("Set threshold:")
        
        self.bright_label = QtGui.QLineEdit(self)
        self.bright_label.setEnabled(False)
        self.bright_label.setGeometry(QtCore.QRect(670, 370, 80, 20))
        self.bright_label.setFrame(False)
        self.bright_label.setText("Set brightness:")
        
        self.rotation_label = QtGui.QLineEdit(self)
        self.rotation_label.setEnabled(False)
        self.rotation_label.setGeometry(QtCore.QRect(670, 400, 80, 20))
        self.rotation_label.setFrame(False)
        self.rotation_label.setText("Rotate image:")
        
        self.btn_refresh= QtGui.QPushButton(self)
        self.btn_refresh.setText("Live")
        self.btn_refresh.clicked.connect(self.Live)
        self.btn_refresh.setGeometry(QtCore.QRect(850, 230, 80, 23))
     
        layout.addWidget(self.open_button, 0,0)
        layout.addWidget(self.LableMag, 0,1)
        layout.addWidget(self.videoSize, 0,2)
        layout.addWidget(self.LablePath, 1,0)
        layout.addWidget(self.pg2_label, 2,0)
        layout.addWidget(self.pg2, 3,0,3,3)
        layout.addWidget(self.btn_refresh, 2,2)
        layout.addWidget(self.Options_label, 7,0)
        layout.addWidget(self.Inner_label, 8,1)
        layout.addWidget(self.Inner, 8,2)
        layout.addWidget(self.BoxW_label, 9,1)
        layout.addWidget(self.BoxW, 9,2)
        layout.addWidget(self.BoxL_label, 10,1)
        layout.addWidget(self.BoxL, 10,2)
        layout.addWidget(self.thresh_label, 12,0)
        layout.addWidget(self.sl, 12,1,1,2)
        layout.addWidget(self.bright_label, 13,0)
        layout.addWidget(self.sl_brigth, 13,1,1,2)
        layout.addWidget(self.rotation_label, 14,0)
        layout.addWidget(self.sl_rotation, 14,1,1,2)
        layout.addWidget(self.roi_button, 16,0)
        layout.addWidget(self.play_button, 16,1)
        layout.addWidget(self.save_button, 16,2)
        layout.addWidget(self.proBar_label, 18,0)
        layout.addWidget(self.proBar, 18,1,1,2)
        
        self.show()

    def startCapture(self):
        if not self.cap:
            if self.filename:
                self.cap = cv2.VideoCapture(self.filename)

                if not self.cap.isOpened(): 
                    print ("could not open :",self.filename)
                    self.getfile()
                    return

                self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.fps=self.cap.get(cv2.CAP_PROP_FPS)
                self.cap.set(cv2.CAP_PROP_FPS,self.fps*4)
                self.proBar.setMinimum(1)
                self.proBar.setMaximum(self.length)
                self.proBar.setValue(0)
                self.videoFrame=videoWindow(500,500)
                self.videoFrame.sl_frame.setMaximum(self.length)
                self.frame_end=self.length
                self.frame_start=1
                duration=int((self.frame_end-self.frame_start)/self.fps/60)
                frames=str(self.frame_start)+"/"+str(self.frame_end)+" ("+str(duration)+" min)"
                self.videoFrame.Lableframe.setText(frames)
                
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
     
        self.valueX=[]
        self.valueY=[]
        self.valueNframe=[]
        self.plot.setData(x=self.valueX,y=self.valueY)
        
        self.t_value=self.sl.value()
        self.roi_box()
        
    def endCapture(self):
        self.cap.release()
        self.cap = None
    
    def magnific(self):
        if self.videoSize.currentText()=='1X':self.magnification=1
        if self.videoSize.currentText()=='1.5X':self.magnification=1.5
        if self.videoSize.currentText()=='2X':self.magnification=2
        if self.videoSize.currentText()=='3X':self.magnification=3
        if self.videoSize.currentText()=='4X':self.magnification=4
        self.selectionchange()
        
    def getfile(self):
        if self.cap:
            self.endCapture()
            
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                        'c:\\',"Video files (*.mp4)")
        self.filename=os.path.abspath(self.filename)
        #self.filename="D:/Google drive/Lab/UofA/videos/Exp5. TAK+LPS/Open field/Intection 1/Pre/P1040224.MP4"
    
        
        self.startCapture()
        self.LablePath.setText(self.filename)
        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.sl.setEnabled(False)
        self.videoFrame.sl_frame.setEnabled(False)

        self.sl_rotation.setValue(0)
        self.sl.setValue(200)
        self.videoFrame.sl_frame.setValue(1)
        self.sl_brigth.setValue(10)
    
        
    def Live(self):
        if (self.btn_refresh.text()=="No live"):
            self.btn_refresh.setText("Live")
        else:
            self.btn_refresh.setText("No live")
            
    def adjust_gamma(self,image, gamma):
        	invGamma = 1.0 / gamma
        	table = np.array([((i / 255.0) ** invGamma) * 255
        		for i in np.arange(0, 256)]).astype("uint8")
         
        	return cv2.LUT(image, table)
            
    def selectionchange(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.videoFrame.sl_frame.value())    
        ret, frame = self.cap.read()
        
        frame= self.adjust_gamma(frame, gamma=float(self.sl_brigth.value())/10)
        frame=cv2.resize(frame,None,fx=self.magnification, fy=self.magnification, interpolation = cv2.INTER_LINEAR)
        
        (h, w) = frame.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, self.sl_rotation.value(), 1.0)
        frame = cv2.warpAffine(frame, M, (w, h))
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (41, 41), 0)    
        
        box_img=np.zeros((h,w), np.uint8)
        cv2.fillConvexPoly(box_img, self.pts, 1)
        
        blur=cv2.bitwise_and(blur, blur, mask=box_img)  
        t = cv2.threshold(blur,self.t_value, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(t, None, iterations=2)
        _,cnts,_= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)         
        if cnts:
            areas = [cv2.contourArea(c) for c in cnts]
            max_index = np.argmax(areas)
            cnt=cnts[max_index]

            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.circle(frame, (cx,cy), 5, (255,0,0), -1)
            cv2.drawContours(frame, cnt, -1, (0,255,0), 3)
            

        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0],QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.videoFrame.video_frame.setPixmap(pix)
        #self.video_frame.setPixmap(pix)
            
        self.valueX=[]
        self.valueY=[]
        self.valueNframe=[]
        self.plot.setData(x=self.valueX,y=self.valueY)
        self.t_value=self.sl.value()
        self.proBar.setValue(self.videoFrame.sl_frame.value())
        self.frame_start=self.videoFrame.sl_frame.value()
        duration=int((self.frame_end-self.frame_start)/self.fps/60)
        frames=str(self.frame_start)+"/"+str(self.frame_end)+" ("+str(duration)+" min)"
        self.videoFrame.Lableframe.setText(frames)
        
    def nextFrameSlot(self):
            
            nframe=self.proBar.value() 
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,nframe)
            grabbed, frame = self.cap.read()
            
            if not grabbed:
                self.AnalyzeBtn()
                self.proBar.setValue(self.length)
                self.btn_refresh.setText("Live")
                self.plot.setData(x=self.valueX,y=self.valueY)
            
            frame= self.adjust_gamma(frame, gamma=float(self.sl_brigth.value())/10)
            frame=cv2.resize(frame,None,fx=self.magnification, fy=self.magnification, interpolation = cv2.INTER_LINEAR)
        
            (h, w) = frame.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, self.sl_rotation.value(), 1.0)
            frame = cv2.warpAffine(frame, M, (w, h))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (41, 41), 0)    
        
            box_img=np.zeros((h,w), np.uint8)
            cv2.fillConvexPoly(box_img, self.pts, 1)
        
            blur=cv2.bitwise_and(blur, blur, mask=box_img)  
            t = cv2.threshold(blur,self.t_value, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(t, None, iterations=2)
            _,cnts,_= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                         cv2.CHAIN_APPROX_SIMPLE)
            if cnts:
                areas = [cv2.contourArea(c) for c in cnts]
                max_index = np.argmax(areas)
                cnt=cnts[max_index]

                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(frame, (cx,cy), 5, (255,0,0), -1)
                
                self.valueX.append(cx-self.Roi_points1.x())
                self.valueY.append(cy-self.Roi_points1.y())
                self.valueNframe.append(nframe+10)
                        
            
            if (self.btn_refresh.text()=="Live"):
                self.plot.setData(x=self.valueX,y=self.valueY)
                img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
                pix = QtGui.QPixmap.fromImage(img)
                self.videoFrame.video_frame.setPixmap(pix)
                self.videoFrame.sl_frame.setValue(nframe)
            
            if nframe<(self.frame_end-10):
                self.proBar.setValue(nframe+10)
            else:
                self.proBar.setValue(self.frame_end)
                self.AnalyzeBtn()
            
    def SlideFrame(self):
        
        if (self.play_button.text()=="Analyze"):
            self.selectionchange()
        
    def start(self):
        self.timer.start()
   
    def roi_box(self):

        self.Roi_points=self.videoFrame.roi.getSceneHandlePositions()
        
        self.Roi_points1=self.Roi_points[0][1]
        self.Roi_points1=self.Roi_points1.toPoint()
        self.Roi_points2=self.Roi_points[1][1]
        self.Roi_points2=self.Roi_points2.toPoint()
        self.Roi_points3=self.Roi_points[2][1]
        self.Roi_points3=self.Roi_points3.toPoint()
        self.Roi_points4=self.Roi_points[3][1]
        self.Roi_points4=self.Roi_points4.toPoint()
        
        self.pts = np.array([[self.Roi_points1.x(),self.Roi_points1.y()],
                              [self.Roi_points2.x(),self.Roi_points2.y()],
                               [self.Roi_points3.x(),self.Roi_points3.y()],
                                [self.Roi_points4.x(),self.Roi_points4.y()]], np.int32)
        self.pts = self.pts.reshape((-1,1,2))
        boxPixels_Y=math.sqrt((self.Roi_points1.x() - self.Roi_points2.x())**2 + (self.Roi_points1.y() - self.Roi_points2.y())**2)
        boxPixels_X=math.sqrt((self.Roi_points2.x() - self.Roi_points3.x())**2 + (self.Roi_points2.y() - self.Roi_points3.y())**2)
        self.roi2.setSize([boxPixels_X, boxPixels_Y])
        self.roi2.setPos([0,0])
        
        self.Innerboxdimension=float(self.Inner.text())
        self.size_x=self.roi2.size()[0]*(self.Innerboxdimension/100)
        self.size_y=self.roi2.size()[1]*(self.Innerboxdimension/100)
        self.pos_x=self.roi2.size()[0]*0.5-self.size_x*0.5
        self.pos_y=self.roi2.size()[1]*0.5-self.size_y*0.5
        self.roi3.setPos([self.pos_x, self.pos_y])
        self.roi3.setSize([self.size_x, self.size_y])
        self.roi2.setEnabled(False)
        self.roi3.setEnabled(False)
        
        self.selectionchange()
        self.play_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.sl.setEnabled(True)
        self.videoFrame.sl_frame.setEnabled(True)

    def AnalyzeBtn(self):

        if (self.play_button.text()=="Analyze"):
            self.stop()
            self.play_button.setText("Stop")
            self.start()
        else:
            self.play_button.setText("Analyze")
            self.stop()
            
    def frameslider(self):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.sl_frame.value())
        
    def stop(self):
        self.timer.stop()
    
    def setEnd(self):
        self.frame_end=self.videoFrame.sl_frame.value()
        duration=int((self.frame_end-self.frame_start)/self.fps/60)
        frames=str(self.frame_start)+"/"+str(self.frame_end)+" ("+str(duration)+" min)"
        self.videoFrame.Lableframe.setText(frames)
        self.proBar.setMaximum(self.frame_end)
                
    def Summary(self):
        self.distance=0
        self.Inner_distance=0
        self.Inner_frames=0
        self.duration=(self.frame_end-self.frame_start)/self.fps
        boxPixels_Y=math.sqrt((self.Roi_points1.x() - self.Roi_points2.x())**2 + (self.Roi_points1.y() - self.Roi_points2.y())**2)
        boxPixels_X=math.sqrt((self.Roi_points2.x() - self.Roi_points3.x())**2 + (self.Roi_points2.y() - self.Roi_points3.y())**2)
        
        if (boxPixels_X<=boxPixels_Y):
            cm_px=int(self.BoxL.text())/boxPixels_Y
        else:
            cm_px=int(self.BoxW.text())/boxPixels_Y
            
        roi3_xmin=self.pos_x
        roi3_xmax=self.pos_x+self.size_x
        roi3_ymin=self.pos_y
        roi3_ymax=self.pos_y+self.size_y
        
        for i,v in enumerate(self.valueNframe):
            if i<len(self.valueNframe)-1:
                dist = math.sqrt((self.valueX[i+1] - self.valueX[i])**2 + (self.valueY[i+1] - self.valueY[i])**2)
                self.distance=self.distance+dist
                if (self.valueX[i]>=roi3_xmin and self.valueX[i]<=roi3_xmax):
                    if (self.valueY[i]>=roi3_ymin and self.valueY[i]<=roi3_ymax):
                        self.Inner_distance=self.Inner_distance+dist
                        self.Inner_frames=self.Inner_frames+10
                        
        self.cm_distance=self.distance*cm_px
        self.cm_Inner_distance=self.Inner_distance*cm_px
        self.Inner_time=self.Inner_frames/self.fps
        self.per_Inner_time=(self.Inner_time/self.duration)*100
                            
    def showdialog(self):
       msg = QtGui.QMessageBox()
       msg.setIcon(QtGui.QMessageBox.Information)
    
       msg.setText("The files with the analysis have been created")
       msg.setWindowTitle("File Saved")
       msg.setStandardButtons(QtGui.QMessageBox.Ok)
       msg.exec_()
        
    def handleSave(self):
        self.Summary()
        s = self.filename
        end = s.find(self.filename)-4
        s[0:end]
        filename=s[0:end]
        with open(filename+".txt", "w") as text_file:
            text_file.write("Frame")
            text_file.write("\t")
            text_file.write("Raw X")
            text_file.write("\t")
            text_file.write("Raw Y")
            text_file.write("\t")
            text_file.write("X")
            text_file.write("\t")
            text_file.write("Y")
            text_file.write("\n") 
            
            for i,v in enumerate(self.valueNframe):
                text_file.write(str(self.valueNframe[i]))
                text_file.write("\t")
                text_file.write(str(self.valueX[i]+self.Roi_points1.x()))
                text_file.write("\t")
                text_file.write(str(self.valueY[i]+self.Roi_points1.y()))
                text_file.write("\t")
                text_file.write(str(self.valueX[i]))
                text_file.write("\t")
                text_file.write(str(self.valueY[i]))
                text_file.write("\n")

        filename2=filename+"_S"
        with open(filename2+".txt", "w") as text_file:
            text_file.write("Raw Distance (px): ")
            text_file.write(str(self.distance))
            text_file.write("\n")
            text_file.write("Distance (cm): ")
            text_file.write(str(self.cm_distance))
            text_file.write("\n")
            text_file.write("Inner box dimension (%): ")
            text_file.write(str(self.Innerboxdimension))
            text_file.write("\n")
            text_file.write("Raw Inner Distance (px): ")
            text_file.write(str(self.Inner_distance))
            text_file.write("\n")
            text_file.write("Inner Distance (cm): ")
            text_file.write(str(self.cm_Inner_distance))
            text_file.write("\n")
            text_file.write("Time (s): ")
            text_file.write(str(self.duration))
            text_file.write("\n")
            text_file.write("Inner time (s): ")
            text_file.write(str(self.Inner_time))
            text_file.write("\n")
            text_file.write(" % Inner time (%): ")
            text_file.write(str(self.per_Inner_time))
        self.showdialog()
class videoWindow:
        def __init__(self, w,h):
            self.window2=QtGui.QWidget()
            self.window2.resize(w, h)
            
            layout = QtGui.QGridLayout()
            self.window2.setLayout(layout)
            
            self.sl_frame = QtGui.QSlider()
            self.sl_frame.setOrientation(QtCore.Qt.Horizontal)
            self.sl_frame.setMinimum(1)
            self.sl_frame.setMaximum(255)
            self.sl_frame.setValue(1)
            self.sl_frame.setTickPosition(QtGui.QSlider.TicksBelow)
            self.sl_frame.setTickInterval(1000)
            self.sl_frame.setGeometry(QtCore.QRect(9, 530, 640, 20))
            self.sl_frame.valueChanged.connect(window.SlideFrame)
            self.sl_frame.setEnabled(False)
            
            self.End_button = QtGui.QPushButton()
            self.End_button.setText("End")
            self.End_button.clicked.connect(window.setEnd)
            self.End_button.setGeometry(QtCore.QRect(600, 530, 50, 23))
            
            self.Lableframe = QtGui.QLineEdit()
            self.Lableframe.setEnabled(False)
            self.Lableframe.setGeometry(QtCore.QRect(419, 530, 170, 20))
            self.Lableframe.setFrame(False)
            
            self.video_frame=QtGui.QLabel()
            self.video_frame.setGeometry(QtCore.QRect(10, 40, 640, 480))
            self.video_frame.setFrameShape(QtGui.QFrame.Box)
            
            self.pg1 = pg.GraphicsView()
            self.pg1.setStyleSheet("background: transparent")
            self.pg1.setGeometry(QtCore.QRect(10, 40, 640, 480))
            self.pg1.setFrameShape(QtGui.QFrame.Box)
            self.pg1.setBackground(None)      
            self.roi=pg.PolyLineROI([[25, 25], [25, 450], [600, 450], [600, 25]], pen=(6,9), closed=True)        
            self.pg1.addItem(self.roi)
            self.roi_h=self.roi.getHandles()
        
            layout.addWidget(self.video_frame, 0,0)
            layout.addWidget(self.pg1, 0,0)
            layout.addWidget(self.sl_frame, 1,0)
            layout.addWidget(self.End_button, 3,0)
            layout.addWidget(self.Lableframe, 2,0)
            self.window2.show()
                
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ControlWindow()
    sys.exit(app.exec_())
