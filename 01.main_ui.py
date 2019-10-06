#Note: Keep the UI file in the same directory where .py script is there.

import sys, os
from PyQt5 import uic
from PyQt5.QtTest import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtTest
from FARO_UI import *
import math
import object_detection 

def start():
    signal = 1 #To start video processing.
    ui.message.setText('Object detection is in progress.')
    object_detection.objectdetection(ip_filename[0],mode,signal)
    ui.message.setText('Object detection has been stopped.')
    
def cancel():
    signal = 0 #To stop video processing.
    ui.message.setText('Object detection has been stopped.')
    objectdetection,object_detection(ip_filename[0],mode,signal)
     
def inputfilename():
    
    # This enables file browsing dialog and gets file name.
    global ip_filename
    ip_filename = QFileDialog.getOpenFileName(window, 'Select Input Video File',filter = ("Videos(*.mp4)")) 
    print(ip_filename[0])
    ui.ip_filename.setText(ip_filename[0])
    
def outputfolderlocation():
    
    global op_folder
    #op_folder = QFileDialog.getExistingDirectory(None, 'Select Output path ')
    #print(op_folder)
    ui.op_filename.setText('Output file will be stored in same location.')

def selection():
    #This selects mode input from webcam or video file. 
    global mode
    
    if ui.input_webcam.isChecked() == True:
        mode = 'webcam'
        ui.text.setText('Object detection using Webcam will start.')
    
    elif ui.input_file.isChecked() == True: 
        mode = 'video'
        ui.text.setText('Object detection using Input Video file will start.')
        
    #elif (ui.input_file.isChecked() == True) and (ui.input_webcam.isChecked() == True):
        #ui.process_button.setDisabled(True)
        #ui.text.setText('Kindly select any one mode to proceed.')
    else:
        ui.text.setText('Kindly select input mode (file or webcam).')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    ip_filename = ''
    mode = ''
    ui.text.setText('Kindly select input mode (file or webcam).')
    ui.ip_button.clicked.connect(inputfilename)
    ui.op_button.clicked.connect(outputfolderlocation)
    ui.input_webcam.toggled.connect(selection)
    ui.input_file.toggled.connect(selection)
    ui.process_button.clicked.connect(start)
    ui.cancel_button.clicked.connect(cancel)
    window.show()
    sys.exit(app.exec())
    
