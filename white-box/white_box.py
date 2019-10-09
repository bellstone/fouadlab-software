import sys
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

		self.resize(500, 300)
		self.setWindowTitle('White box entrance analysis')

		layout = QtGui.QGridLayout(self)
		self.setLayout(layout)


		self.LablePath = QtGui.QLineEdit(self)
		self.LablePath.setEnabled(False)
		self.LablePath.setGeometry(QtCore.QRect(90, 10, 641, 20))
		self.LablePath.setFrame(False)

		self.LableRaw = QtGui.QLineEdit(self)
		self.LableRaw.setEnabled(False)
		self.LableRaw.setGeometry(QtCore.QRect(90, 10, 641, 20))
		self.LableRaw.setFrame(False)

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

		self.open_button = QtGui.QPushButton(self)
		self.open_button.setText("Open Video")
		self.open_button.clicked.connect(self.getfile)
		self.open_button.setGeometry(QtCore.QRect(9, 9, 75, 23))

		self.Results_label=QtGui.QLineEdit(self)
		self.Results_label.setGeometry(QtCore.QRect(670, 270, 320, 20))
		self.Results_label.setFrame(False)
		self.Results_label.setEnabled(False)
		self.Results_label.setText("Results:")
		self.Results_label.setFont(font)

		self.time_label=QtGui.QLineEdit(self)
		self.time_label.setGeometry(QtCore.QRect(670, 500, 320, 20))
		self.time_label.setFrame(False)
		self.time_label.setEnabled(False)
		self.time_label.setText("Time (s):")

		self.LableTime = QtGui.QLineEdit(self)
		self.LableTime.setEnabled(False)
		self.LableTime.setGeometry(QtCore.QRect(90, 10, 641, 20))
		self.LableTime.setFrame(False)

		self.entries_label=QtGui.QLineEdit(self)
		self.entries_label.setGeometry(QtCore.QRect(670, 500, 320, 20))
		self.entries_label.setFrame(False)
		self.entries_label.setEnabled(False)
		self.entries_label.setText("# entries:")

		self.LableEntries = QtGui.QLineEdit(self)
		self.LableEntries.setEnabled(False)
		self.LableEntries.setGeometry(QtCore.QRect(90, 10, 641, 20))
		self.LableEntries.setFrame(False)

		self.play_button = QtGui.QPushButton(self)
		self.play_button.setText("Analyze")
		self.play_button.clicked.connect(self.AnalyzeBtn)
		self.play_button.setGeometry(QtCore.QRect(760, 450, 80, 30))
		self.play_button.setEnabled(False)

		self.roi_button = QtGui.QPushButton(self)
		self.roi_button.setText("Save Roi")
		self.roi_button.clicked.connect(self.roi_box)
		self.roi_button.setGeometry(QtCore.QRect(670, 450, 80, 30))


		self.proBar_label=QtGui.QLineEdit(self)
		self.proBar_label.setGeometry(QtCore.QRect(670, 500, 320, 20))
		self.proBar_label.setFrame(False)
		self.proBar_label.setEnabled(False)
		self.proBar_label.setText("Progress:")
		self.proBar=QtGui.QProgressBar(self)
		self.proBar.setGeometry(QtCore.QRect(670, 520, 280, 20))

		self.sl_brigth = QtGui.QSlider(self)
		self.sl_brigth.setOrientation(QtCore.Qt.Horizontal)
		self.sl_brigth.setMinimum(0)
		self.sl_brigth.setMaximum(50)
		self.sl_brigth.setValue(10)
		self.sl_brigth.setTickPosition(QtGui.QSlider.TicksBelow)
		self.sl_brigth.setTickInterval(10)
		self.sl_brigth.valueChanged.connect(self.selectionchange)
		self.sl_brigth.setGeometry(QtCore.QRect(750, 370, 180, 20))


		self.bright_label = QtGui.QLineEdit(self)
		self.bright_label.setEnabled(False)
		self.bright_label.setGeometry(QtCore.QRect(670, 370, 80, 20))
		self.bright_label.setFrame(False)
		self.bright_label.setText("Set brightness:")

		self.sensitivity_label = QtGui.QLineEdit(self)
		self.sensitivity_label.setEnabled(False)
		self.sensitivity_label.setGeometry(QtCore.QRect(670, 230, 80, 20))
		self.sensitivity_label.setFrame(False)
		self.sensitivity_label.setText("Threshold (0-1):")

		self.sensitivity = QtGui.QLineEdit(self)
		self.sensitivity.setEnabled(True)
		self.sensitivity.setText("0.25")
		self.sensitivity.setGeometry(QtCore.QRect(760, 230, 40, 20))
		self.sensitivity.setFrame(True)


		layout.addWidget(self.open_button, 0,0)
		layout.addWidget(self.LableMag,0,1)
		layout.addWidget(self.videoSize,0,2)
		layout.addWidget(self.LablePath, 1,0)
		layout.addWidget(self.bright_label, 13,0)
		layout.addWidget(self.sl_brigth, 13,1,1,2)
		layout.addWidget(self.sensitivity_label, 14,0,1,2)
		layout.addWidget(self.sensitivity, 14,1)
		layout.addWidget(self.roi_button, 16,0)
		layout.addWidget(self.play_button, 16,1)
		layout.addWidget(self.proBar_label, 18,0)
		layout.addWidget(self.proBar, 18,1,1,2)
		layout.addWidget(self.LableRaw, 19,1)
		layout.addWidget(self.Results_label,20,0)
		layout.addWidget(self.time_label,21,1)
		layout.addWidget(self.LableTime,21,2)
		layout.addWidget(self.entries_label,22,1)
		layout.addWidget(self.LableEntries,22,2)

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

		self.valueTime=[]
		self.valueNframe=[]
		self.roi_box()

	def endCapture(self):
		self.cap.release()
		self.cap = None

	def getfile(self):
		if self.cap:
			self.endCapture()

		name = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
						'c:\\',"Video files (*.mp4)")
		self.filename = name[0]
		print (self.filename)
		self.filename=os.path.abspath(self.filename)

		self.startCapture()
		self.LablePath.setText(self.filename)
		self.play_button.setEnabled(False)
		self.videoFrame.sl_frame.setEnabled(False)

		self.videoFrame.sl_frame.setValue(1)
		self.sl_brigth.setValue(10)

	def magnific(self):
		if self.videoSize.currentText()=='1X':self.magnification=1
		if self.videoSize.currentText()=='1.5X':self.magnification=1.5
		if self.videoSize.currentText()=='2X':self.magnification=2
		if self.videoSize.currentText()=='3X':self.magnification=3
		if self.videoSize.currentText()=='4X':self.magnification=4
		self.selectionchange()

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
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		(h, w) = frame.shape[:2]
		center = (w / 2, h / 2)

		box_img=np.zeros((h,w), np.uint8)
		cv2.fillConvexPoly(box_img, self.pts, 1)

		gray=cv2.bitwise_and(gray, gray, mask=box_img)
		t = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
			cv2.THRESH_BINARY_INV,11,2)
		self.initialGrayValue=float(np.mean(t.ravel()))
		self.LableRaw.setText(str(round(self.initialGrayValue,3)))

		img = QtGui.QImage(frame, frame.shape[1], frame.shape[0],QtGui.QImage.Format_RGB888)
		pix = QtGui.QPixmap.fromImage(img)
		self.videoFrame.video_frame.setPixmap(pix)

		self.counter=0
		self.xT=0
		self.nentries=0
		self.valueTime=[]
		self.valueNframe=[]
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
				self.plot.setData(x=self.valueX,y=self.valueY)

			frame= self.adjust_gamma(frame, gamma=float(self.sl_brigth.value())/10)
			frame=cv2.resize(frame,None,fx=self.magnification, fy=self.magnification, interpolation = cv2.INTER_LINEAR)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			(h, w) = frame.shape[:2]
			center = (w / 2, h / 2)

			box_img=np.zeros((h,w), np.uint8)
			cv2.fillConvexPoly(box_img, self.pts, 255)

			gray=cv2.bitwise_and(gray, gray, mask=box_img)
			t = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
				cv2.THRESH_BINARY_INV,11,2)


			if np.mean(t.ravel())/self.initialGrayValue > (1+float(self.sensitivity.text())):
				self.videoFrame.LableInOut.setStyleSheet("background-color: green")
				self.valueTime.append(1)
				self.xT+=10
				if len(self.valueTime)>1:
					if self.valueTime[len(self.valueTime)-2]==self.valueTime[len(self.valueTime)-1]:
						self.counter+=1
			else:
				self.videoFrame.LableInOut.setStyleSheet("background-color: red")
				self.valueTime.append(0)

			if len(self.valueTime)>1:
				if self.valueTime[len(self.valueTime)-2]==0 and self.valueTime[len(self.valueTime)-1]==1:
					if self.counter>=5:
						print(self.counter)
						self.nentries+=1
						self.counter=0

			self.LableRaw.setText(str(round(np.mean(t.ravel()),3)))

			self.valueNframe.append(nframe+10)
			self.LableTime.setText(str(round(self.xT/self.fps,3)))
			self.LableEntries.setText(str(self.nentries))

			self.valueNframe.append(nframe+10)
			img = QtGui.QImage(frame, frame.shape[1], frame.shape[0],QtGui.QImage.Format_RGB888)
			pix = QtGui.QPixmap.fromImage(img)
			self.videoFrame.video_frame.setPixmap(pix)

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
		self.selectionchange()
		self.play_button.setEnabled(True)
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

			self.LableInOut = QtGui.QLineEdit()
			self.LableInOut.setEnabled(False)
			self.LableInOut.setGeometry(QtCore.QRect(419, 530, 170, 20))
			self.LableInOut.setFrame(False)
			self.LableInOut.setStyleSheet("background-color: red");

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

			layout.addWidget(self.LableInOut)
			layout.addWidget(self.video_frame, 1,0)
			layout.addWidget(self.pg1, 1,0)
			layout.addWidget(self.sl_frame, 2,0)
			layout.addWidget(self.End_button, 4,0)
			layout.addWidget(self.Lableframe, 3,0)
			self.window2.show()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = ControlWindow()
	sys.exit(app.exec_())
