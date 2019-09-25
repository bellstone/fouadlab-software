import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import cv2
import math

class ControlWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.cap = None
        self.filename=None
        
        font=QtGui.QFont()
        font.setPixelSize(15)
        
        self.resize(950, 560)
        self.setWindowTitle('Open Field analysis: Activity')

        self.LablePath = QtGui.QLineEdit(self)
        self.LablePath.setEnabled(False)
        self.LablePath.setGeometry(QtCore.QRect(90, 10, 641, 20))
        self.LablePath.setFrame(False)
                     
        self.open_button = QtGui.QPushButton(self)
        self.open_button.setText("Open Video")
        self.open_button.clicked.connect(self.getfile)
        self.open_button.setGeometry(QtCore.QRect(9, 9, 75, 23))
        
        self.End_button = QtGui.QPushButton(self)
        self.End_button.setText("End")
        self.End_button.clicked.connect(self.setEnd)
        self.End_button.setGeometry(QtCore.QRect(600, 530, 50, 23))
        
        self.Lableframe = QtGui.QLineEdit(self)
        self.Lableframe.setEnabled(False)
        self.Lableframe.setGeometry(QtCore.QRect(419, 530, 170, 20))
        self.Lableframe.setFrame(False)
        
        self.save_button = QtGui.QPushButton(self)
        self.save_button.setText("Save data")
        self.save_button.clicked.connect(self.handleSave)
        self.save_button.setGeometry(QtCore.QRect(850, 470, 80, 30))
        self.save_button.setFont(font)
        self.save_button.setEnabled(False)
        
        self.play_button = QtGui.QPushButton(self)
        self.play_button.setText("Analyze")
        self.play_button.clicked.connect(self.AnalyzeBtn)
        self.play_button.setGeometry(QtCore.QRect(760, 470, 80, 30))
        self.play_button.setFont(font)
        self.play_button.setEnabled(False)
        
        self.roi_button = QtGui.QPushButton(self)
        self.roi_button.setText("Save Roi")
        self.roi_button.clicked.connect(self.roi_box)
        self.roi_button.setGeometry(QtCore.QRect(670, 470, 80, 30))
        
        self.sl_frame = QtGui.QSlider(self)
        self.sl_frame.setOrientation(QtCore.Qt.Horizontal)
        self.sl_frame.setMinimum(1)
        self.sl_frame.setMaximum(255)
        self.sl_frame.setValue(1)
        self.sl_frame.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_frame.setTickInterval(1000)
        self.sl_frame.setGeometry(QtCore.QRect(9, 530, 400, 20))
        self.sl_frame.valueChanged.connect(self.selectionchange)
        self.sl_frame.setEnabled(True)
                
        self.video_frame=QtGui.QLabel(self)
        self.video_frame.setGeometry(QtCore.QRect(10, 40, 640, 480))
        self.video_frame.setFrameShape(QtGui.QFrame.Box)
        
        self.pg1 = pg.GraphicsView(self)
        self.pg1.setStyleSheet("background: transparent")
        self.pg1.setGeometry(QtCore.QRect(10, 40, 640, 480))
        self.pg1.setFrameShape(QtGui.QFrame.Box)
        self.pg1.setBackground(None)      
        self.roi=pg.PolyLineROI([[65, 221], [65, 271], [240, 271], [240, 221]], pen=(6,9), closed=True)        
        self.roi_2=pg.PolyLineROI([[263, 18], [263, 218], [313, 218], [313, 18]], pen=(0,9), closed=True)        
        self.roi_3=pg.PolyLineROI([[383, 225], [383, 275], [583, 275], [583, 225]], pen=(6,9), closed=True)        
        self.roi_4=pg.PolyLineROI([[255, 267], [255, 467], [305, 467], [305, 267]], pen=(0,9), closed=True)                
        self.pg1.addItem(self.roi)
        self.pg1.addItem(self.roi_2)
        self.pg1.addItem(self.roi_3)
        self.pg1.addItem(self.roi_4)
        self.img = pg.ImageItem(border='w')
        self.img.rotate(90)
        self.pg1.addItem(self.img)
             
        self.pg2_label=QtGui.QLineEdit(self)
        self.pg2_label.setGeometry(QtCore.QRect(650, 10, 320, 20))
        self.pg2_label.setFrame(False)
        self.pg2_label.setEnabled(False)
        self.pg2_label.setText("Tracking:")
               
        self.pg2 = pg.GraphicsLayoutWidget(self)
        self.pg2.setGeometry(QtCore.QRect(650, 40, 280, 200))
        self.pg2.setBackground(None)   
        self.w1=self.pg2.addPlot()
        self.plot=pg.PlotDataItem(size=3,connect="all", symbolSize=3)
        self.w1.invertY()
        self.w1.addItem(self.plot)
        
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
        self.sl.setGeometry(QtCore.QRect(750, 400, 180, 20))
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
        self.sl_brigth.setGeometry(QtCore.QRect(750, 270, 180, 20))
        
        self.sl_brigth2 = QtGui.QSlider(self)
        self.sl_brigth2.setOrientation(QtCore.Qt.Horizontal)
        self.sl_brigth2.setMinimum(0)
        self.sl_brigth2.setMaximum(50)
        self.sl_brigth2.setValue(10)
        self.sl_brigth2.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_brigth2.setTickInterval(10)
        self.sl_brigth2.valueChanged.connect(self.selectionchange)
        self.sl_brigth2.setGeometry(QtCore.QRect(750, 300, 180, 20))
        
        self.sl_brigth3 = QtGui.QSlider(self)
        self.sl_brigth3.setOrientation(QtCore.Qt.Horizontal)
        self.sl_brigth3.setMinimum(0)
        self.sl_brigth3.setMaximum(50)
        self.sl_brigth3.setValue(10)
        self.sl_brigth3.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_brigth3.setTickInterval(10)
        self.sl_brigth3.valueChanged.connect(self.selectionchange)
        self.sl_brigth3.setGeometry(QtCore.QRect(750, 330, 180, 20))
        
        self.sl_brigth4 = QtGui.QSlider(self)
        self.sl_brigth4.setOrientation(QtCore.Qt.Horizontal)
        self.sl_brigth4.setMinimum(0)
        self.sl_brigth4.setMaximum(50)
        self.sl_brigth4.setValue(10)
        self.sl_brigth4.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_brigth4.setTickInterval(10)
        self.sl_brigth4.valueChanged.connect(self.selectionchange)
        self.sl_brigth4.setGeometry(QtCore.QRect(750, 360, 180, 20))
        
        self.sl_rotation = QtGui.QSlider(self)
        self.sl_rotation.setOrientation(QtCore.Qt.Horizontal)
        self.sl_rotation.setMinimum(-180)
        self.sl_rotation.setMaximum(180)
        self.sl_rotation.setValue(0)
        self.sl_rotation.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sl_rotation.setTickInterval(20)
        self.sl_rotation.valueChanged.connect(self.selectionchange)
        self.sl_rotation.setGeometry(QtCore.QRect(750, 430, 180, 20))

        self.thresh_label = QtGui.QLineEdit(self)
        self.thresh_label.setEnabled(False)
        self.thresh_label.setGeometry(QtCore.QRect(670, 400, 80, 20))
        self.thresh_label.setFrame(False)
        self.thresh_label.setText("Set threshold:")
        
        self.bright_label = QtGui.QLineEdit(self)
        self.bright_label.setEnabled(False)
        self.bright_label.setGeometry(QtCore.QRect(690, 270, 50, 20))
        self.bright_label.setFrame(False)
        self.bright_label.setText("Roi 1:")
        
        self.bright_label = QtGui.QLineEdit(self)
        self.bright_label.setEnabled(False)
        self.bright_label.setGeometry(QtCore.QRect(690, 300, 50, 20))
        self.bright_label.setFrame(False)
        self.bright_label.setText("Roi 2:")
        
        self.bright_label = QtGui.QLineEdit(self)
        self.bright_label.setEnabled(False)
        self.bright_label.setGeometry(QtCore.QRect(690, 330, 50, 20))
        self.bright_label.setFrame(False)
        self.bright_label.setText("Roi 3:")
        
        self.bright_label = QtGui.QLineEdit(self)
        self.bright_label.setEnabled(False)
        self.bright_label.setGeometry(QtCore.QRect(690, 360, 50, 20))
        self.bright_label.setFrame(False)
        self.bright_label.setText("Roi 4:")
        
        self.bright_label = QtGui.QLineEdit(self)
        self.bright_label.setEnabled(False)
        self.bright_label.setGeometry(QtCore.QRect(670, 240, 80, 20))
        self.bright_label.setFrame(False)
        self.bright_label.setText("Set brightness:")
        
        self.rotation_label = QtGui.QLineEdit(self)
        self.rotation_label.setEnabled(False)
        self.rotation_label.setGeometry(QtCore.QRect(670, 430, 80, 20))
        self.rotation_label.setFrame(False)
        self.rotation_label.setText("Rotate image:")
        
        self.btn_refresh= QtGui.QPushButton(self)
        self.btn_refresh.setText("Live")
        self.btn_refresh.clicked.connect(self.Live)
        self.btn_refresh.setGeometry(QtCore.QRect(850, 230, 80, 23))
     
        self.show()

    def startCapture(self):
        if not self.cap:
            if self.filename:
                self.cap = cv2.VideoCapture(str(self.filename))

                if not self.cap.isOpened(): 
                    print "could not open :",self.filename
                    self.getfile()
                    return

                self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.fps=self.cap.get(cv2.CAP_PROP_FPS)
                self.cap.set(cv2.CAP_PROP_FPS,self.fps*4)
                self.proBar.setMinimum(1)
                self.proBar.setMaximum(self.length)
                self.proBar.setValue(0)
                self.sl_frame.setMaximum(self.length)
                
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
     
        self.valueX=[]
        self.valueY=[]
        self.valueNframe=[]
        self.plot.setData(x=self.valueX,y=self.valueY)

        self.t_value=self.sl.value()
        self.frame_end=self.length
        self.roi_box()
        
    def endCapture(self):
        self.cap.release()
        self.cap = None
        
    def getfile(self):
        if self.cap:
            self.endCapture()
            
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                        'c:\\',"Video files (*.mp4)")
        self.filename.replace('/', '\\')
        self.startCapture()
        self.LablePath.setText(self.filename)
        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.sl.setEnabled(False)
        self.sl_rotation.setValue(0)
        self.sl.setValue(200)
        self.sl_frame.setValue(1)
        self.sl_brigth.setValue(10)

        duration=int((self.frame_end-self.frame_start)/self.fps/60)
        frames=str(self.frame_start)+"/"+str(self.frame_end)+" ("+str(duration)+" min)"
        self.Lableframe.setText(frames)
                        
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
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,self.sl_frame.value())
        self.frame_start=self.sl_frame.value()
        duration=int((self.frame_end-self.frame_start)/self.fps/60)
        frames=str(self.frame_start)+"/"+str(self.frame_end)+" ("+str(duration)+" min)"
        self.Lableframe.setText(frames)
        
        ret, frame = self.cap.read()
        
        (h, w) = frame.shape[:2]
        center = (w / 2, h / 2)
        
        M = cv2.getRotationMatrix2D(center, self.sl_rotation.value(), 1.0)
        frame = cv2.warpAffine(frame, M, (w, h))
        
        box_img=np.zeros((h,w), np.uint8)
        cv2.fillConvexPoly(box_img, self.pts, 255)
#        box_img_inv=cv2.bitwise_not(box_img)
        frame_1=self.adjust_gamma(frame, gamma=float(self.sl_brigth.value())/10)
        frame_1=cv2.bitwise_and(frame_1, frame_1, mask=box_img)
        
        box_img_2=np.zeros((h,w), np.uint8)
        cv2.fillConvexPoly(box_img_2, self.pts_2, 255)
        frame_2=self.adjust_gamma(frame, gamma=float(self.sl_brigth2.value())/10)
        frame_2=cv2.bitwise_and(frame_2, frame_2, mask=box_img_2)
        
        box_img_3=np.zeros((h,w), np.uint8)
        cv2.fillConvexPoly(box_img_3, self.pts_3, 255)
        frame_3=self.adjust_gamma(frame, gamma=float(self.sl_brigth3.value())/10)
        frame_3=cv2.bitwise_and(frame_3, frame_3, mask=box_img_3)
        
        box_img_4=np.zeros((h,w), np.uint8)
        cv2.fillConvexPoly(box_img_4, self.pts_4, 255)
        frame_4=self.adjust_gamma(frame, gamma=float(self.sl_brigth4.value())/10)
        frame_4=cv2.bitwise_and(frame_4, frame_4, mask=box_img_4)

        img_fg=frame_1+frame_2+frame_3+frame_4
        
        mask=box_img+box_img_2+box_img_3+box_img_4
        mask2=cv2.bitwise_not(mask)
        img_bg=cv2.bitwise_and(frame, frame, mask=mask2)
        
        img=cv2.add(img_fg, img_bg)
        
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (1, 1), 0)
        blur=cv2.bitwise_and(blur, blur, mask=mask)
            
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
            cv2.circle(img, (cx,cy), 5, (255,0,0), -1)
            cv2.drawContours(img, cnt, -1, (0,255,0), 3)
            
       
        img2 = QtGui.QImage(img, img.shape[1], img.shape[0],QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img2)
        self.video_frame.setPixmap(pix)
            
        self.valueX=[]
        self.valueY=[]
        self.valueNframe=[]
        self.plot.setData(x=self.valueX,y=self.valueY)
        self.t_value=self.sl.value()
        self.proBar.setValue(self.sl_frame.value())
        
    def nextFrameSlot(self):
            nframe=self.proBar.value() 
            self.cap.set(cv2.CAP_PROP_POS_FRAMES,nframe)
            grabbed, frame = self.cap.read()
            
            if nframe<(self.length-10):
                self.proBar.setValue(nframe+10)
                (h, w) = frame.shape[:2]
                center = (w / 2, h / 2)
            
                M = cv2.getRotationMatrix2D(center, self.sl_rotation.value(), 1.0)
                frame = cv2.warpAffine(frame, M, (w, h))
                
                box_img=np.zeros((h,w), np.uint8)
                cv2.fillConvexPoly(box_img, self.pts, 255)
        #        box_img_inv=cv2.bitwise_not(box_img)
                frame_1=self.adjust_gamma(frame, gamma=float(self.sl_brigth.value())/10)
                frame_1=cv2.bitwise_and(frame_1, frame_1, mask=box_img)
                
                box_img_2=np.zeros((h,w), np.uint8)
                cv2.fillConvexPoly(box_img_2, self.pts_2, 255)
                frame_2=self.adjust_gamma(frame, gamma=float(self.sl_brigth2.value())/10)
                frame_2=cv2.bitwise_and(frame_2, frame_2, mask=box_img_2)
                
                box_img_3=np.zeros((h,w), np.uint8)
                cv2.fillConvexPoly(box_img_3, self.pts_3, 255)
                frame_3=self.adjust_gamma(frame, gamma=float(self.sl_brigth3.value())/10)
                frame_3=cv2.bitwise_and(frame_3, frame_3, mask=box_img_3)
                
                box_img_4=np.zeros((h,w), np.uint8)
                cv2.fillConvexPoly(box_img_4, self.pts_4, 255)
                frame_4=self.adjust_gamma(frame, gamma=float(self.sl_brigth4.value())/10)
                frame_4=cv2.bitwise_and(frame_4, frame_4, mask=box_img_4)
        
                img_fg=frame_1+frame_2+frame_3+frame_4
                
                mask=box_img+box_img_2+box_img_3+box_img_4
                mask2=cv2.bitwise_not(mask)
                img_bg=cv2.bitwise_and(frame, frame, mask=mask2)
                
                img=cv2.add(img_fg, img_bg)
                
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (1, 1), 0)
                blur=cv2.bitwise_and(blur, blur, mask=mask)
                
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
                    cv2.circle(img, (cx,cy), 5, (255,0,0), -1)
                    
                    self.valueX.append(cx)
                    self.valueY.append(cy)
                    self.valueNframe.append(nframe+10)
                            
                
                if (self.btn_refresh.text()=="Live"):
                    self.plot.setData(x=self.valueX,y=self.valueY)
                    img2 = QtGui.QImage(img, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
                    pix = QtGui.QPixmap.fromImage(img2)
                    self.video_frame.setPixmap(pix)
            else:
                self.proBar.setValue(self.length)
                self.AnalyzeBtn()
                self.btn_refresh.setText("Live")
                self.plot.setData(x=self.valueX,y=self.valueY)

    def start(self):
        self.timer.start()
   
    def roi_box(self):

        self.Roi_points=self.roi.getSceneHandlePositions()
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
        
        self.Roi_points_2=self.roi_2.getSceneHandlePositions()
        self.Roi_points_21=self.Roi_points_2[0][1]
        self.Roi_points_21=self.Roi_points_21.toPoint()
        self.Roi_points_22=self.Roi_points_2[1][1]
        self.Roi_points_22=self.Roi_points_22.toPoint()
        self.Roi_points_23=self.Roi_points_2[2][1]
        self.Roi_points_23=self.Roi_points_23.toPoint()
        self.Roi_points_24=self.Roi_points_2[3][1]
        self.Roi_points_24=self.Roi_points_24.toPoint()
        
        self.pts_2 = np.array([[self.Roi_points_21.x(),self.Roi_points_21.y()],
                              [self.Roi_points_22.x(),self.Roi_points_22.y()],
                               [self.Roi_points_23.x(),self.Roi_points_23.y()],
                                [self.Roi_points_24.x(),self.Roi_points_24.y()]], np.int32)
        self.pts_2 = self.pts_2.reshape((-1,1,2))             
        
        self.Roi_points_3=self.roi_3.getSceneHandlePositions()
        self.Roi_points_31=self.Roi_points_3[0][1]
        self.Roi_points_31=self.Roi_points_31.toPoint()
        self.Roi_points_32=self.Roi_points_3[1][1]
        self.Roi_points_32=self.Roi_points_32.toPoint()
        self.Roi_points_33=self.Roi_points_3[2][1]
        self.Roi_points_33=self.Roi_points_33.toPoint()
        self.Roi_points_34=self.Roi_points_3[3][1]
        self.Roi_points_34=self.Roi_points_34.toPoint()
        
        self.pts_3 = np.array([[self.Roi_points_31.x(),self.Roi_points_31.y()],
                              [self.Roi_points_32.x(),self.Roi_points_32.y()],
                               [self.Roi_points_33.x(),self.Roi_points_33.y()],
                                [self.Roi_points_34.x(),self.Roi_points_34.y()]], np.int32)
        self.pts_3 = self.pts_3.reshape((-1,1,2)) 
        
        self.Roi_points_4=self.roi_4.getSceneHandlePositions()
        self.Roi_points_41=self.Roi_points_4[0][1]
        self.Roi_points_41=self.Roi_points_41.toPoint()
        self.Roi_points_42=self.Roi_points_4[1][1]
        self.Roi_points_42=self.Roi_points_42.toPoint()
        self.Roi_points_43=self.Roi_points_4[2][1]
        self.Roi_points_43=self.Roi_points_43.toPoint()
        self.Roi_points_44=self.Roi_points_4[3][1]
        self.Roi_points_44=self.Roi_points_44.toPoint()
        
        self.pts_4 = np.array([[self.Roi_points_41.x(),self.Roi_points_41.y()],
                              [self.Roi_points_42.x(),self.Roi_points_42.y()],
                               [self.Roi_points_43.x(),self.Roi_points_43.y()],
                                [self.Roi_points_44.x(),self.Roi_points_44.y()]], np.int32)
        self.pts_4 = self.pts_4.reshape((-1,1,2))

#        boxPixels_Y=math.sqrt((self.Roi_points1.x() - self.Roi_points2.x())**2 + (self.Roi_points1.y() - self.Roi_points2.y())**2)
#        boxPixels_X=math.sqrt((self.Roi_points2.x() - self.Roi_points3.x())**2 + (self.Roi_points2.y() - self.Roi_points3.y())**2)

        self.selectionchange()
        self.play_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.sl.setEnabled(True)
        self.sl_frame.setEnabled(True)
        
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
        self.frame_end=self.sl_frame.value()
        duration=int((self.frame_end-self.frame_start)/self.fps/60)
        frames=str(self.frame_start)+"/"+str(self.frame_end)+" ("+str(duration)+" min)"
        self.Lableframe.setText(frames)
        self.proBar.setMaximum(self.frame_end)
        
    def Summary(self):
        self.distance=0
        self.raw_time_open=0
        self.raw_time_close=0

        roiShape = self.roi.mapToView(self.roi.shape())
        roi_2Shape = self.roi.mapToView(self.roi_2.shape())
        roi_3Shape = self.roi.mapToView(self.roi_3.shape())
        roi_4Shape = self.roi.mapToView(self.roi_4.shape())

        pt=QtCore.QPointF()
        for i,v in enumerate(self.valueNframe):
            if i<len(self.valueNframe)-1:
                dist = math.sqrt((self.valueX[i+1] - self.valueX[i])**2 + (self.valueY[i+1] - self.valueY[i])**2)
                self.distance=self.distance+dist
                pt.setX(self.valueX[i])
                pt.setY(self.valueY[i])
                if roiShape.contains(pt) or roi_3Shape.contains(pt):
                    self.raw_time_close=self.raw_time_close+10
                if roi_2Shape.contains(pt) or roi_4Shape.contains(pt):
                    self.raw_time_open=self.raw_time_open+10
                        
        self.time_open=self.raw_time_open/self.fps
        self.time_close=self.raw_time_close/self.fps
        
    def handleSave(self):
        self.Summary()
        s = str(self.filename)
        end = s.find(self.filename)-4
        s[0:end]
        filename=s[0:end]
        with open(filename+".txt", "w") as text_file:
            text_file.write("Frame")
            text_file.write("\t")
            text_file.write("Raw X")
            text_file.write("\t")
            text_file.write("Raw Y")
            text_file.write("\n") 
            
            for i,v in enumerate(self.valueNframe):
                text_file.write(str(self.valueNframe[i]))
                text_file.write("\t")
                text_file.write(str(self.valueX[i]+self.Roi_points1.x()))
                text_file.write("\t")
                text_file.write(str(self.valueY[i]+self.Roi_points1.y()))
                text_file.write("\n")

        filename2=filename+"_S"
        with open(filename2+".txt", "w") as text_file:
            text_file.write("Raw Time open (frames): ")
            text_file.write(str(self.raw_time_open))
            text_file.write("\n")
            text_file.write("Raw Time close (frames): ")
            text_file.write(str(self.raw_time_close))
            text_file.write("\n")
            text_file.write("Time open (seconds): ")
            text_file.write(str(self.time_open))
            text_file.write("\n")
            text_file.write("Time close (seconds): ")
            text_file.write(str(self.time_close))
            text_file.write("\n")
            text_file.write("Distance (px): ")
            text_file.write(str(self.distance))
            text_file.write("\n")
            
                
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ControlWindow()
    sys.exit(app.exec_())
