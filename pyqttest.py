
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
        
        # creating a label
        self.label = QLabel("Current Soundfont: Sawtooth (Default)", self)
        # setting geometry to the label
        self.label.setGeometry(0, 0,500,50)
        

    def keyPressEvent(self, e:QKeyEvent):
        if e.key()==Qt.Key_F1:
            self.label.setText("Current Soundfont: Sawtooth")
        if e.key()==Qt.Key_F2:
            self.label.setText("Current Soundfont: Square")
        if e.key()==Qt.Key_F3:
            self.label.setText("Current Soundfont: Triangle")
        if e.key()==Qt.Key_F4:
            self.label.setText("Current Soundfont: Cosine")


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
