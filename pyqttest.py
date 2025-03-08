import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('PyQt events with keyboard') 
        self.show()
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Z:
            self.close()
    def dialog():
        mbox = QMessageBox()

        mbox.setText("Your allegiance has been noted")
        mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                
        mbox.exec_()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())



# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox

# def dialog():
#     mbox = QMessageBox()

#     mbox.setText("Your allegiance has been noted")
#     mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
#     mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
#     mbox.exec_()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = QWidget()
#     w.resize(300,300)
#     w.setWindowTitle("Guru99")
    
#     label = QLabel(w)
#     label.setText("Behold the Guru, Guru99")
#     label.move(100,130)
#     label.show()

#     btn = QPushButton(w)
#     btn.setText('Beheld')
#     btn.move(110,150)
#     btn.show()
#     btn.clicked.connect(dialog)

    
#     w.show()
#     sys.exit(app.exec_())