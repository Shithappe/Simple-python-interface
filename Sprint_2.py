import sys, math
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot


def midpoint_rectangle_rule(func, a, b, n):
    result = 0.0
    h = (b - a) / n
    for i in range(0, n):
        result += func(a + h * (i + 0.5))
    result *= h
    return result

def right_rectangle_rule(func, a, b, n):
    result = 0.0
    h = (b - a) / n
    for i in range(0, n):
        result += func((a+h) + h * i)
    result *= h
    return result

def left_rectangle_rule(func, a, b, n):
    result = 0.0
    h = (b - a) / n
    for i in range(0, n):
        result += func(a + h * i)
    result *= h
    return result

def simpson(f, a, b, n):
    h=(b-a)/n
    k=0.0
    x=a + h
    for i in range(1,n//2 + 1):
        k += 4*f(x)
        x += 2*h

    x = a + 2*h
    for i in range(1,n//2):
        k += 2*f(x)
        x += 2*h
    return (h/3)*(f(a)+f(b)+k)

def Trapezoidal(f, a, b, n):
    h = (b-a)/float(n)
    s = 0.5*(f(a) + f(b))
    for i in range(1,n,1):
        s = s + f(a + i*h)
    return h*s


def euler_method(func, a, b, y0, N):
    step = (b - a) / N
    arr = np.array(range(N+1), float)
    arr.fill(0)
    arr[0] = y0
    for i in range(N):
        arr[i+1] = arr[i] + step * func(a,arr[i])
        a = a + step
    return arr

def runge_kuta_2(func, a, b, y0, N):
    step = float((b - a) / N)
    arr = np.array(range(N+1), float)
    arr.fill(0.0)
    arr[0] = y0
    for i in range(N):
        arr[i+1] = arr[i] + step/2 * (func(a,arr[i]) + func(a+step,arr[i]+step*func(a,arr[i])))
        a+=step
    return arr

def runge_kuta_3(func, a, b, y0, N):
    step = float((b - a) / N)
    arr = np.array(range(N+1), float)
    arr.fill(0)
    arr[0] = y0
    for i in range(N):
        arr[i+1] = arr[i] + (step/6) * (func(a, arr[i]) + 
                    4 * func(a + step/2, arr[i] + step * func(a, arr[i])/2) +
                    func(a + step, arr[i] + 2 * step * func(a + step/2, arr[i] + step * func(a, arr[i])/2) - step * func(a, arr[i])))
        a+=step
    return arr

def runge_kuta_4(func, a, b, y0, N):
    step = (b - a) / N
    arr = np.array(range(N+1), float)
    arr.fill(0)
    arr[0] = y0
    for i in range(N):
        k1 = step * func(a, arr[i])
        k2 = step * func(a + step/2, arr[i] + k1/2)
        k3 = step * func(a + step/2, arr[i] + k2/2)
        k4 = step * func(a + step, arr[i] + k3)
        arr[i+1] = arr[i] + (k1 + 2*k2 + 2*k3 + k4)/6
        a= a + step
    return arr

met = "Левых прямоугольников"
DM = "Эйлера"
Func = "f(x)=expf0(-x)"

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Sprint_2)'
        self.left = 500
        self.top = 200
        self.width = 450
        self.height = 500
    
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.layout = QFormLayout(self)
		# Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(450, 400)

		# Add tabs
        self.tabs.addTab(self.tab1, "Интегралы")
        self.tabs.addTab(self.tab2, "Дифузы")

		# Create first tab
        self.tab1.layout = QGridLayout(self)
        self.tab2.layout = QGridLayout(self)

        self.label = QLabel()
        self.label.setText("Функция ")
        self.label1 = QLabel()
        self.label1.setText("Метод ")

        self.comboDM = QComboBox(self)
        self.comboDM.addItems(["Эйлера", "Рунге-Кутта второго порядка", "Рунге-Кутта третьего порядка", "Рунге-Кутта четвертого порядка"])
        self.comboDM.activated.connect(self.handleActivatedDM)

        self.label_a = QLabel('a:', self)
        self.label_b = QLabel('b:', self)
        self.label_h = QLabel('шаг:', self)
        self.label_aDM = QLabel('a:', self)
        self.label_bDM = QLabel('b:', self)
        self.label_hDM = QLabel('шаг:', self)
        self.label_yDM = QLabel('y:', self)

        self.comboF = QComboBox(self)
        self.comboF.addItems(["f(x)=expf0(-x)", "f(x)=sin(x)", "f(x)=expf0(x^2)", "f(x)=expf0(-4-x^3)"])
        self.comboF.activated.connect(self.handleActivatedF)
        self.comboFDM = QComboBox(self)
        self.comboFDM.addItems(["y'=-xy", "y'=y+x", "y'=(3x-12x^2)y"])
        self.comboFDM.activated.connect(self.handleActivatedFDM)

        self.a = QLineEdit("", self)
        self.b = QLineEdit("", self)
        self.h = QLineEdit("100", self)
        self.aDM = QLineEdit("", self)
        self.bDM = QLineEdit("", self)
        self.hDM = QLineEdit("10", self)
        self.yDM = QLineEdit("", self)

        self.button = QPushButton('Решить', self)
        self.button.clicked.connect(self.on_click)
        self.buttonDMT = QPushButton('Решить в таблицу', self)
        self.buttonDMT.clicked.connect(self.on_clickDMT)
        self.buttonDMG = QPushButton('Решить в график', self)
        self.buttonDMG.clicked.connect(self.on_clickDMG)

        self.label_ans = QLabel('                                                                                                   ', self)
        self.label_ansDM = QLabel('                                                                                                   ', self)

        self.view = view = pg.PlotWidget()
        self.curve = view.plot(name="Line")

        self.tab1.layout.addWidget(self.label, 0, 0)
        self.tab1.layout.addWidget(self.comboF, 0, 1)
        self.tab1.layout.addWidget(self.label_a)
        self.tab1.layout.addWidget(self.a)
        self.tab1.layout.addWidget(self.label_b)
        self.tab1.layout.addWidget(self.b)
        self.tab1.layout.addWidget(self.label_h)
        self.tab1.layout.addWidget(self.h)
        self.tab1.layout.addWidget(self.button, 4, 0, 4, 2)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout.addWidget(self.label1, 0, 0)
        self.tab2.layout.addWidget(self.comboDM, 0, 1)
        self.tab2.layout.addWidget(self.comboFDM, 1, 0, 1, 2)
        self.tab2.layout.addWidget(self.label_aDM)
        self.tab2.layout.addWidget(self.aDM)
        self.tab2.layout.addWidget(self.label_bDM)
        self.tab2.layout.addWidget(self.bDM)
        self.tab2.layout.addWidget(self.label_yDM)
        self.tab2.layout.addWidget(self.yDM)
        self.tab2.layout.addWidget(self.label_hDM)
        self.tab2.layout.addWidget(self.hDM)
        self.tab2.layout.addWidget(self.buttonDMT, 6, 0)
        self.tab2.layout.addWidget(self.buttonDMG, 6, 1)
        self.tab2.setLayout(self.tab2.layout)

		# Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def handleActivated(self, index):
        global met
        met = self.combo.itemText(index)
        print(met)

    def handleActivatedDM(self, index):
        global DM
        DM = self.comboDM.itemText(index)
        print(DM)

    def handleActivatedF(self, index):
        global Func
        Func = self.comboF.itemText(index)
        print(Func)

        if Func == "f(x)=sin(x)":
            Func = lambda x: math.sin(x)

        if Func == "f(x)=expf0(x^2)":
            Func = lambda x: math.e ** (-x **2)

        if Func == "f(x)=expf0(-4-x^3)":
            Func = lambda x: math.e ** (-4*x-x**3)

    def handleActivatedFDM(self, index):
        global Func
        Func = self.comboFDM.itemText(index)
        print(Func)

        if Func == "y'=-xy":
            Func = lambda x, y: -y*x

        if Func == "y'=y+x":
            Func = lambda x, y: y + x

        if Func == "y'=(3x-12x^2)y":
            Func = lambda x, y: (3*x-12*x*x)*y


    @pyqtSlot()
    def on_click(self):        
        global Func
        if Func == "f(x)=expf0(-x)":
            Func = lambda x: math.e ** (-x)
        
        rez = [left_rectangle_rule(Func, int(self.a.text()), int(self.b.text()), int(self.h.text())),
        midpoint_rectangle_rule(Func, int(self.a.text()), int(self.b.text()), int(self.h.text())),
        right_rectangle_rule(Func, int(self.a.text()), int(self.b.text()), int(self.h.text())),
        Trapezoidal(Func, int(self.a.text()), int(self.b.text()), int(self.h.text())),
        simpson(Func, int(self.a.text()), int(self.b.text()), int(self.h.text()))]

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(2)

        HH = ["Левых прямоугольников", "Центральных прямоугольников", "Правых прямоугольников", "Трапеций", "Симпсона"]

        for i in range(5):
            self.tableWidget.setItem(i,0, QTableWidgetItem(HH[i]))
            self.tableWidget.setItem(i,1, QTableWidgetItem(str(rez[i])))

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tab1.layout.addWidget(self.tableWidget, 12, 0, 12, 2)
        self.tab1.setLayout(self.tab1.layout)

    def on_clickDMG(self):        

        global Func
        if Func == "f(x)=expf0(-x)": #
            Func = lambda x, y: -y*x

        if DM == "Эйлера":
            rez = euler_method(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))

        if DM == "Рунге-Кутта второго порядка":
            rez = runge_kuta_2(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))

        if DM ==  "Рунге-Кутта третьего порядка":
            rez = runge_kuta_3(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))

        if DM == "Рунге-Кутта четвертого порядка":
            rez = runge_kuta_4(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))


        self.curve.setData(rez)
        self.tab2.layout.addWidget(self.view, 12, 0, 12, 2)
        self.tab2.setLayout(self.tab2.layout)

    def on_clickDMT(self):

        global Func
        if Func == "f(x)=expf0(-x)": #
            Func = lambda x, y: -y*x

        if DM == "Эйлера":
            rez = euler_method(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))

        if DM == "Рунге-Кутта второго порядка":
            rez = runge_kuta_2(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))

        if DM ==  "Рунге-Кутта третьего порядка":
            rez = runge_kuta_3(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))

        if DM == "Рунге-Кутта четвертого порядка":
            rez = runge_kuta_4(Func, int(self.aDM.text()), int(self.bDM.text()), int(self.yDM.text()), int(self.hDM.text()))
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(rez))
        self.tableWidget.setColumnCount(1)

        HH = []
        for i in range(len(rez)):
            HH.append(str(i))
        self.tableWidget.setVerticalHeaderLabels(HH)

        for i in range(len(rez)):
            self.tableWidget.setItem(0,i, QTableWidgetItem(str(rez[i])))

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tab2.layout.addWidget(self.tableWidget, 12, 0, 12, 2)
        self.tab2.setLayout(self.tab2.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())