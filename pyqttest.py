
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # setting title
        self.setWindowTitle("The Synthetizers' Synth")
        # setting geometry
        self.setGeometry(100, 100, 500, 400)
        # calling method
        self.UiComponents()
        # showing all the widgets
        self.show()


    # method for components
    def UiComponents(self):
        #labels
        self.soundfont = QLabel("Current Soundfont: Sawtooth (Default)", self)
        self.soundfont.setGeometry(0, 0,300,50)
        self.record = QLabel("Recording: Off", self)
        self.record.setGeometry(0, 14,200,50)
        self.playback = QLabel("Playback: Off", self)
        self.playback.setGeometry(0, 28,200,50)
        self.hints = QLabel("Hints:\n"
                "Soundfonts\n"
                "F1: Sawtooth, F2: Square, F3: Triangle, F4: Cosine\n"
                "Recording Related\n"
                "F5: Recording On/Off, F6: Playback Start, F7: Playback Stop and Reset",self)
        self.hints.setGeometry(0, 50,1000,100)
        

    def keyPressEvent(self, e:QKeyEvent):
        if e.key()==Qt.Key_F1:
            self.soundfont.setText("Current Soundfont: Sawtooth")
        if e.key()==Qt.Key_F2:
            self.soundfont.setText("Current Soundfont: Square")
        if e.key()==Qt.Key_F3:
            self.soundfont.setText("Current Soundfont: Triangle")
        if e.key()==Qt.Key_F4:
            self.soundfont.setText("Current Soundfont: Cosine")
        
        if e.key() == Qt.Key_F5:
            if "Off" in str(self.record.text()):
                self.record.setText("Recording: On")
            else:
                self.record.setText("Recording: Off")

        if e.key() == Qt.Key_F6:
            self.playback.setText("Playback: On")
        if e.key() == Qt.Key_F7:
            self.playback.setText("Playback: Off")



# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of Window
window = Window()

# start the app
sys.exit(App.exec())

'''
f1 - f4 soundfonts
f5 start/stop recording
f6 playback
f7 reset
'''