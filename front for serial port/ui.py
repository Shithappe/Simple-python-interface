from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(620, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 600, 375))

        # num
        w = 100
        self.a1 = QtWidgets.QLCDNumber(self.groupBox)
        self.a1.setGeometry(QtCore.QRect(w, 20, 151, 41))
        self.a2 = QtWidgets.QLCDNumber(self.groupBox)
        self.a2.setGeometry(QtCore.QRect(w, 65, 151, 41))
        self.a3 = QtWidgets.QLCDNumber(self.groupBox)
        self.a3.setGeometry(QtCore.QRect(w, 110, 151, 41))
        q = 180
        self.b1 = QtWidgets.QLCDNumber(self.groupBox)
        self.b1.setGeometry(QtCore.QRect(w, q+20, 151, 41))
        self.b2 = QtWidgets.QLCDNumber(self.groupBox)
        self.b2.setGeometry(QtCore.QRect(w, q+65, 151, 41))
        self.b3 = QtWidgets.QLCDNumber(self.groupBox)
        self.b3.setGeometry(QtCore.QRect(w, q+110, 151, 41))
        d = 300
        self.c1 = QtWidgets.QLCDNumber(self.groupBox)
        self.c1.setGeometry(QtCore.QRect(w+d, 20, 151, 41))
        self.c2 = QtWidgets.QLCDNumber(self.groupBox)
        self.c2.setGeometry(QtCore.QRect(w+d, 65, 151, 41))
        self.c3 = QtWidgets.QLCDNumber(self.groupBox)
        self.c3.setGeometry(QtCore.QRect(w+d, 110, 151, 41))
        
        self.d1 = QtWidgets.QLCDNumber(self.groupBox)
        self.d1.setGeometry(QtCore.QRect(w+d, q+20, 151, 41))
        self.d2 = QtWidgets.QLCDNumber(self.groupBox)
        self.d2.setGeometry(QtCore.QRect(w+d, q+65, 151, 41))
        self.d3 = QtWidgets.QLCDNumber(self.groupBox)
        self.d3.setGeometry(QtCore.QRect(w+d, q+110, 151, 41))

        # label
        self.la1 = QtWidgets.QLabel(self.groupBox)
        self.la1.setGeometry(QtCore.QRect(20, 8, 150, 50))
        self.la2 = QtWidgets.QLabel(self.groupBox)
        self.la2.setGeometry(QtCore.QRect(20, 50, 150, 50))
        self.la3 = QtWidgets.QLabel(self.groupBox)
        self.la3.setGeometry(QtCore.QRect(20, 95, 150, 50))

        self.lb1 = QtWidgets.QLabel(self.groupBox)
        self.lb1.setGeometry(QtCore.QRect(20, 50+q, 150, 50))
        self.lb2 = QtWidgets.QLabel(self.groupBox)
        self.lb2.setGeometry(QtCore.QRect(20, 8+q, 150, 50))
        self.lb3 = QtWidgets.QLabel(self.groupBox)
        self.lb3.setGeometry(QtCore.QRect(20, 95+q, 150, 50))

        self.lc1 = QtWidgets.QLabel(self.groupBox)
        self.lc1.setGeometry(QtCore.QRect(20+d, 8, 150, 50))
        self.lc2 = QtWidgets.QLabel(self.groupBox)
        self.lc2.setGeometry(QtCore.QRect(20+d, 50, 150, 50))
        self.lc3 = QtWidgets.QLabel(self.groupBox)
        self.lc3.setGeometry(QtCore.QRect(20+d, 95, 150, 50))

        self.ld1 = QtWidgets.QLabel(self.groupBox)
        self.ld1.setGeometry(QtCore.QRect(20+d, 50+q, 150, 50))
        self.ld2 = QtWidgets.QLabel(self.groupBox)
        self.ld2.setGeometry(QtCore.QRect(20+d, 8+q, 150, 50))
        self.ld3 = QtWidgets.QLabel(self.groupBox)
        self.ld3.setGeometry(QtCore.QRect(20+d, 95+q, 150, 50))

        self.pushButton = QtWidgets.QPushButton("pushButton", self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(280, 350, 75, 23))

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "test"))
        self.groupBox.setTitle(_translate("MainWindow", "Data from serial port"))
        self.la1.setText(_translate("MainWindow", "x"))
        self.la2.setText(_translate("MainWindow", "y"))
        self.la3.setText(_translate("MainWindow", "z"))

        self.lb1.setText(_translate("MainWindow", "roll"))
        self.lb2.setText(_translate("MainWindow", "pitch"))
        self.lb3.setText(_translate("MainWindow", "yaw"))

        self.lc1.setText(_translate("MainWindow", "dx"))
        self.lc2.setText(_translate("MainWindow", "dy"))
        self.lc3.setText(_translate("MainWindow", "dx"))

        self.ld1.setText(_translate("MainWindow", "droll"))
        self.ld2.setText(_translate("MainWindow", "dprich"))
        self.ld3.setText(_translate("MainWindow", "dyaw"))
        self.pushButton.setText(_translate("MainWindow", "Start"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())