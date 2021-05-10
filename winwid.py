from multiprocessing import freeze_support
import sys
from PyQt5 import QtWidgets, QtCore,QtGui
from PyQt5.QtWidgets import (QApplication, QFormLayout, QLabel, QRadioButton, QCheckBox,
                             QListWidget, QStackedWidget, QLineEdit,
                             QHBoxLayout, QGridLayout
                             )
from PyQt5.Qt import *
from PyQt5.QtGui import QPixmap, QCursor 
import pyscreenshot as ImageGrab
import pytesseract
from pytesseract import Output
import cv2
# from tkinter import Tk
import pyperclip
import tempfile


class StackedExample(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        # self.resize(300,100)
        self.setGeometry(0,0,1920,1080)

        self.central_widget = QWidget()               # define central widget
        self.setCentralWidget(self.central_widget)    # set QMainWindow.centralWidget
        print (self.geometry(),self.frameSize() )
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.begin=QPoint(0, 0)

        self.end=QSize(0, 0)
        self.show()

    def paintEvent(self, event):
        
        qp = QtGui.QPainter(self)
        pixmap = QPixmap(tempdir +'/scr.png')
        qp.drawPixmap(self.rect(), pixmap)
        
        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40))  
        qp.setBrush(br)   
        qp.drawRect(QtCore.QRect(self.begin ,self.end))  
        self.setCursor(Qt.CrossCursor)
        
        qp.end()     

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()
        # print (type(event.pos()))
        # print (event.pos(),event.localPos())
        global start_x, start_y
        start_x = event.pos().x()+ round(event.pos().x()*0.02)
        start_y = event.pos().y()+ round(event.pos().y()*0.05) #QStyle::PM_TitleBarHeight

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        # print (event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        end_x = event.pos().x()+ round(event.pos().x()*0.02)
        end_y = event.pos().y()+ round(event.pos().y()*0.05) #QStyle::PM_TitleBarHeight
        self.begin = event.pos()
        self.end = event.pos()
        self.update()
        # print (event.pos(),event.localPos())

        print (start_x,start_y,end_x,end_y )

        img = cv2.imread(tempdir +'/scr.png')
        im = img[start_y:end_y, start_x:end_x]
        cv2.imwrite(tempdir +'/scr1.png',im)

        d = pytesseract.image_to_string(im)

        print (d)
        print ('Copying to Clipboard')
        pyperclip.copy(d)

        sys.exit(0)



def main():

    app = QApplication(sys.argv)
    # grab fullscreen
    im = ImageGrab.grab()
    im.save(tempdir +'/scr.png')
    # print('Screenshot Size',im.size)
    ex = StackedExample()

    app.aboutToQuit.connect(app.deleteLater)
    #readtext("/home/selva/projects/scrtext/scr1.png")
    sys.exit(app.exec_())
    print ('after exec_')

if __name__ == '__main__':
    freeze_support()
    start_x,start_y,end_x,end_y = 0,0,0,0
    print ('Temp Dir', tempfile.gettempdir())
    tempdir = tempfile.gettempdir()
    main()
    
