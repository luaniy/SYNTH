
# importing libraries
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets as q
import PyQt5.Qt
import PyQt5.QtCore
import sys


class Window(q.QMainWindow):
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
        label = q.QLabel("Synth", self)
        # setting geometry to the label
        label.setGeometry(100, 150, 200, 50)
        sine = q.QAction("Sine")
        if keyPressEvent.key()==Qt.Key_Z:
            sine.triggered.connect(lambda: label.setText("Sine"))

    def keyPressEvent(self, e):
        
        
        square = q.QAction("Square")
        triangle = q.QAction("Triangle")
        sawtooth = q.QAction("Sawtooth")

        

        square.triggered.connect(lambda: label.setText("Square"))

        triangle.triggered.connect(lambda: label.setText("Triangle"))

        sawtooth.triggered.connect(lambda: label.setText("Sawtooth"))


        

# create pyqt5 app
App = q.QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
