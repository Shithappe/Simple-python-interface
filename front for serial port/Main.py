import sys
from random          import randint
from PyQt5.QtWidgets import QApplication, QMainWindow 
from PyQt5.QtCore    import QTimer

from ui import Ui_MainWindow

class Form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.i = 0 

        self.ui.pushButton.clicked.connect(self.startTimer)

        self.timer = QTimer(self)  
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateData)

        self.show()        

    def startTimer(self):  
        if self.ui.pushButton.text() == "Start":
            self.timer.start(1000) 
            self.ui.pushButton.setText("Stop")            
        else:
            self.ui.pushButton.setText("Start")
            self.timer.stop() 

    def updateData(self):
        voltage = randint(90, 260)                  # <--- insert your average voltage here
        self.ui.a1.display(voltage/2) 
        self.ui.a2.display(voltage) 
        self.ui.a3.display(voltage*2) 

        self.ui.b1.display(voltage/2) 
        self.ui.b2.display(voltage+239) 
        self.ui.b3.display(voltage*2)

        self.ui.c1.display(voltage/2-29) 
        self.ui.c2.display(voltage+2) 
        self.ui.c3.display(voltage*2-123)    

        self.ui.d1.display(voltage/2-29) 
        self.ui.d2.display(voltage+2) 
        self.ui.d3.display(voltage*2-123)      


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = Form()
    sys.exit(app.exec_())