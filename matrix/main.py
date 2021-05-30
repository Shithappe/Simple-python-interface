import sys, copy
import numpy as np
from numpy import array, zeros, diag, diagflat, dot, linalg
from numpy import linalg as LA

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

a = []
b = []
c = []
met = "Крамера"
rez = []

def checkmatrix(a):
    d = LA.det(a)
    if (d == 0.0) :
        return '123'
    else : 
        return None

def det(m,n):
    if n==1: return m[0][0]
    z=0
    for r in range(n):
        k=m[:]
        del k[r]
        z+=m[r][0]*(-1)**r*det([p[1:]for p in k],n-1)
    return z

def cramer(a,b):
    w=len(b)
    d=det(a,w)
    checkmatrix(a)
    r=[det([r[0:i]+[s]+r[i+1:]for r,s in zip(a,b)],w)/d for i in range(w)]
    return r

def gauss_jordan_method(a,b):
    a = np.array(a, float)
    b = np.array(b, float)
    n = len(b)
    checkmatrix(a)
    for k in range(n):
        if np.fabs(a[k,k]) < 1.0e-12:
            for i in range(k,n):
                if np.fabs(a[i,k]) > np.fabs(a[k,k]):
                    for j in range (k,n):
                        a[k,j],a[i,j] = a[i,j],a[k,j]
                    b[k],b[i] = b[i],b[k]
                    break
        pivot = a[k,k]
        for j in range(k,n):
            a[k,j] /= pivot
        b[k] /= pivot
        for i in range(n):
            if i==k or a[i,k] == 0: continue
            factor = a[i,k]
            for j in range (k,n):
                a[i,j] -= factor * a[k,j]
            b[i] -= factor * b[k]
    return b

def gauss_seidel_method(a, b, ITERATION_LIMIT = 5):
    a = np.array(a, float)
    b = np.array(b, float)
    checkmatrix(a)
    for i in range(a.shape[0]):
        row = ["{0:3g}*x{1}".format(a[i, j], j + 1) for j in 
    range(a.shape[1])]
    x = np.zeros_like(b)
    for it_count in range(1, ITERATION_LIMIT):
        x_new = np.zeros_like(x)
        for i in range(a.shape[0]):
            s1 = np.dot(a[i, :i], x_new[:i])
            s2 = np.dot(a[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s1 - s2) / a[i, i]
        if np.allclose(x, x_new, rtol=1e-8):
            break
        x = x_new
    return x

def jacobi_method(a, b, ITERATION_LIMIT = 5):
    a = np.array(a, float)
    b = np.array(b, float)
    checkmatrix(a)
    for i in range(a.shape[0]):
        row = ["{}*x{}".format(a[i, j], j + 1) for j in 
    range(a.shape[1])]
    x = np.zeros_like(b)
    for it_count in range(ITERATION_LIMIT):
        x_new = np.zeros_like(x)
        for i in range(a.shape[0]):
            s1 = np.dot(a[i, :i], x[:i])
            s2 = np.dot(a[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s1 - s2) / a[i, i]
            if x_new[i] == x_new[i-1]:
                break
        if np.allclose(x, x_new, atol=1e-10, rtol=0.):
            break
        x = x_new
    return x
    
def gauss_method(a,b):
    checkmatrix(a)
    n = len(a)
    M = copy.deepcopy(a)
    i = 0
    for x in M:
        x.append(b[i])
        i += 1
    for k in range(n):
        for i in range(k,n):
            if abs(M[i][k]) > abs(M[k][k]):
                M[k], M[i] = M[i],M[k]
            else:
                pass
        for j in range(k+1,n):
            q = float(M[j][k]) / M[k][k]
            for m in range(k, n+1):
                M[j][m] -=  q * M[k][m]
    x = [0 for i in range(n)]
    x[n-1] = float(M[n-1][n])/M[n-1][n-1]
    for i in range (n-1,-1,-1):
        z = 0
        for j in range(i+1,n):
            z = z  + float(M[i][j])*x[j]
        x[i] = float(M[i][n] - z)/M[i][i]
    return x

def checkanswer(a,b,rez):
    a = np.array(a, float)
    b = np.array(b, float)
    if len(rez) == 2:
        tmp1 = a[0][0]*rez[0]+a[0][1]*rez[1]
        tmp2 = a[1][0]*rez[0]+a[1][1]*rez[1]
        if round(tmp1) == b[0] and round(tmp2) == b[1]: return True 
        else: return False
    if len(rez) == 3:
        tmp1 = a[0][0]*rez[0]+a[0][1]*rez[1]+a[0][2]*rez[2]
        tmp2 = a[1][0]*rez[0]+a[1][1]*rez[1]+a[1][2]*rez[2]
        tmp3 = a[2][0]*rez[0]+a[2][1]*rez[1]+a[2][2]*rez[2]
        if round(tmp1) == b[0] and round(tmp2) == b[1] and round(tmp3) == b[2]:
            return True 
        else:
            return False
    if len(rez) == 4:
        tmp1 = a[0][0]*rez[0]+a[0][1]*rez[1]+a[0][2]*rez[2]+a[0][3]*rez[3]
        tmp2 = a[1][0]*rez[0]+a[1][1]*rez[1]+a[1][2]*rez[2]+a[1][3]*rez[3]
        tmp3 = a[2][0]*rez[0]+a[2][1]*rez[1]+a[2][2]*rez[2]+a[2][3]*rez[3]
        tmp4 = a[3][0]*rez[0]+a[3][1]*rez[1]+a[3][2]*rez[2]+a[3][3]*rez[3]
        if round(tmp1) == b[0] and round(tmp2) == b[1] and round(tmp3) == b[2] and round(tmp4) == b[3]:
            return True 
        else:
            return False
        a = np.array(a, float)
        b = np.array(b, float)

        if len(rez) == 2:
            tmp1 = a[0][0]*rez[0]+a[0][1]*rez[1]
            tmp2 = a[1][0]*rez[0]+a[1][1]*rez[1]
            if round(tmp1) == b[0] and round(tmp2) == b[1]:
                return True 
            else:
                return False
        if len(rez) == 3:
            tmp1 = a[0][0]*rez[0]+a[0][1]*rez[1]+a[0][2]*rez[2]
            tmp2 = a[1][0]*rez[0]+a[1][1]*rez[1]+a[1][2]*rez[2]
            tmp3 = a[2][0]*rez[0]+a[2][1]*rez[1]+a[2][2]*rez[2]
            if round(tmp1) == b[0] and round(tmp2) == b[1] and round(tmp3) == b[2]:
                return True 
            else:
                return False
        if len(rez) == 4:
            tmp1 = a[0][0]*rez[0]+a[0][1]*rez[1]+a[0][2]*rez[2]+a[0][3]*rez[3]
            tmp2 = a[1][0]*rez[0]+a[1][1]*rez[1]+a[1][2]*rez[2]+a[1][3]*rez[3]
            tmp3 = a[2][0]*rez[0]+a[2][1]*rez[1]+a[2][2]*rez[2]+a[2][3]*rez[3]
            tmp4 = a[3][0]*rez[0]+a[3][1]*rez[1]+a[3][2]*rez[2]+a[3][3]*rez[3]
            if round(tmp1) == b[0] and round(tmp2) == b[1] and round(tmp3) == b[2] and round(tmp4) == b[3]:
                return True 
            else:
                return False

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'CLAY)'
        self.left = 500
        self.top = 200
        self.width = 520
        self.height = 300
    
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        label = QLabel('Метод', self)
        label.move(10, 10)
        
        self.button = QPushButton('Решить', self)
        self.button.move(85, 155)
        self.button.clicked.connect(self.on_click)

        self.buttonF = QPushButton('Решить с файла', self)
        self.buttonF.move(200, 155)
        self.buttonF.clicked.connect(self.on_clickF)

        self.a1 = QLineEdit("", self)
        self.a1.setGeometry(50, 50, 50, 20)
        self.a2 = QLineEdit("", self)
        self.a2.setGeometry(120, 50, 50, 20)
        self.a3 = QLineEdit("", self)
        self.a3.setGeometry(190, 50, 50, 20)
        self.a4 = QLineEdit("", self)
        self.a4.setGeometry(260, 50, 50, 20)

        self.b1 = QLineEdit("", self)
        self.b1.setGeometry(50, 75, 50, 20)
        self.b2 = QLineEdit("", self)
        self.b2.setGeometry(120,75, 50, 20)
        self.b3 = QLineEdit("", self)
        self.b3.setGeometry(190, 75, 50, 20)
        self.b4 = QLineEdit("", self)
        self.b4.setGeometry(260, 75, 50, 20)

        self.c1 = QLineEdit("", self)
        self.c1.setGeometry(50, 100, 50, 20)
        self.c2 = QLineEdit("", self)
        self.c2.setGeometry(120, 100, 50, 20)
        self.c3 = QLineEdit("", self)
        self.c3.setGeometry(190, 100, 50, 20)
        self.c4 = QLineEdit("", self)
        self.c4.setGeometry(260, 100, 50, 20)

        self.d1 = QLineEdit("", self)
        self.d1.setGeometry(50, 125, 50, 20)
        self.d2 = QLineEdit("", self)
        self.d2.setGeometry(120, 125, 50, 20)
        self.d3 = QLineEdit("", self)
        self.d3.setGeometry(190, 125, 50, 20)
        self.d4 = QLineEdit("", self)
        self.d4.setGeometry(260, 125, 50, 20)

        equally1 = QLabel("=", self)
        equally1.move(325, 50)
        equally2 = QLabel("=", self)
        equally2.move(325, 75)
        equally3 = QLabel("=", self)
        equally3.move(325, 100)
        equally4 = QLabel("=", self)
        equally4.move(325, 125)

        self.x1 = QLineEdit("", self)
        self.x1.setGeometry(350, 50, 50, 20)
        self.x2 = QLineEdit("", self)
        self.x2.setGeometry(350, 75, 50, 20)
        self.x3 = QLineEdit("", self)
        self.x3.setGeometry(350, 100, 50, 20)
        self.x4 = QLineEdit("", self)
        self.x4.setGeometry(350, 125, 50, 20)

        self.combo = QComboBox(self)
        self.combo.addItems(["Крамера", "Гаусса", "Зейделя", "Гаусса-Жордана", "Якоби"])
        self.combo.move(55, 10)
        self.combo.activated.connect(self.handleActivated)

        self.label_a = QLabel('                                                                                                                ', self)
        self.label_a.move(10, 190)
        self.label_b = QLabel('                                                                                                                ', self)
        self.label_b.move(10, 210)
        self.label_c = QLabel('                                                                                                                ', self)
        self.label_c.move(10, 230)
        self.label_d = QLabel('                                                                                                                ', self)
        self.label_d.move(10, 250)

    def handleActivated(self, index):
        global met
        met = self.combo.itemText(index)
        
    @pyqtSlot()
    def on_clickF(self):
        A = [[]]
        x = []

        self.a1.setText("")
        self.a2.setText("")
        self.a3.setText("")
        self.a4.setText("")
        self.b1.setText("")
        self.b2.setText("")
        self.b3.setText("")
        self.b4.setText("")
        self.c1.setText("")
        self.c2.setText("")
        self.c3.setText("")
        self.c4.setText("")
        self.d1.setText("")
        self.d2.setText("")
        self.d3.setText("")
        self.d4.setText("")
        self.x1.setText("")
        self.x2.setText("")
        self.x3.setText("")
        self.x4.setText("")
        file = open("data.txt", "r")

        line = file.readline().split()
        if len(line) == 2:
            A = [[], []]
            self.a1.setText(line[0])
            self.a2.setText(line[1])
            for i in range(len(line)): A[0].append(float(line[i]))
            line = file.readline().split()
            self.b1.setText(line[0])
            self.b2.setText(line[1])
            for i in range(len(line)): A[1].append(float(line[i]))

        if len(line) == 3:
            A = [[], [], []]
            self.a1.setText(line[0])
            self.a2.setText(line[1])
            self.a3.setText(line[2])
            for i in range(len(line)): A[0].append(float(line[i]))
            line = file.readline().split()
            self.b1.setText(line[0])
            self.b2.setText(line[1])
            self.b3.setText(line[2])
            for i in range(len(line)): A[1].append(float(line[i]))
            line = file.readline().split()
            self.c1.setText(line[0])
            self.c2.setText(line[1])
            self.c3.setText(line[2])
            for i in range(len(line)): A[2].append(float(line[i]))

        if len(line) == 4:
            A = [[], [], [], []]
            self.a1.setText(line[0])
            self.a2.setText(line[1])
            self.a3.setText(line[2])
            self.a4.setText(line[3])
            for i in range(len(line)): A[0].append(float(line[i]))
            line = file.readline().split()
            self.b1.setText(line[0])
            self.b2.setText(line[1])
            self.b3.setText(line[2])
            self.b4.setText(line[3])
            for i in range(len(line)): A[1].append(float(line[i]))
            line = file.readline().split()
            self.c1.setText(line[0])
            self.c2.setText(line[1])
            self.c3.setText(line[2])
            self.c4.setText(line[3])
            for i in range(len(line)): A[2].append(float(line[i]))
            line = file.readline().split()
            self.d1.setText(line[0])
            self.d2.setText(line[1])
            self.d3.setText(line[2])
            self.d4.setText(line[3])
            for i in range(len(line)): A[3].append(float(line[i]))

        line = file.readline().split()
        self.x1.setText(line[0])
        self.x2.setText(line[1])
        if len(line) >= 3: self.x3.setText(line[2])
        if len(line) == 4: self.x4.setText(line[3])
        for i in range(len(line)): x.append(float(line[i]))

        file.close

        if checkmatrix(A) == None:
            if met == "Крамера": rez = cramer(A, x)
            if met == "Гаусса": rez = gauss_method(A, x)
            if met == "Зейделя": rez = gauss_seidel_method(A, x)   
            if met == "Гаусса-Жордана": rez = gauss_jordan_method(A, x)
            if met == "Якоби": rez = jacobi_method(A, x)

            if checkanswer(A,x,rez):
                self.label_a.setText("x1 = " + str(rez[0]))
                self.label_b.setText("x2 = " + str(rez[1]))
                if len(line) >= 3: self.label_c.setText("x3 = " + str(rez[2]))
                if len(line) == 4: self.label_d.setText("x4 = " + str(rez[3]))
            else:
                self.label_a.setText("Что то пошло не так :(")
                self.label_b.setText("")
                self.label_c.setText("")
                self.label_d.setText("")

        else:
            rez = checkmatrix(A)
            self.label_a.setText(rez)
            self.label_b.setText("")
            self.label_c.setText("")
            self.label_d.setText("")

    def on_click(self):
        A = []
        a = []
        b = []
        c = []
        d = []
        x = []
        #for 2x2
        a.append(float(self.a1.text()))
        a.append(float(self.a2.text()))
        b.append(float(self.b1.text()))
        b.append(float(self.b2.text()))

        x.append(float(self.x1.text()))
        x.append(float(self.x2.text()))

        if not self.c1.text() == "":
            a.append(float(self.a3.text()))
            b.append(float(self.b3.text()))
            c.append(float(self.c1.text()))
            c.append(float(self.c2.text()))
            c.append(float(self.c3.text()))

            x.append(float(self.x3.text()))

        if not self.d1.text() == "":
            a.append(float(self.a4.text()))
            b.append(float(self.b4.text()))
            c.append(float(self.c4.text()))
            d.append(float(self.d1.text()))
            d.append(float(self.d2.text()))
            d.append(float(self.d3.text()))
            d.append(float(self.d4.text()))

            x.append(float(self.x4.text()))

        A = [a, b, c, d]     
        if not A[3]: A.pop(3)
        if not A[2]: A.pop(2)
        print(A)
        print(x)

        if checkmatrix(A) == None:
            if met == "Крамера": rez = cramer(A, x)
            if met == "Гаусса": rez = gauss_method(A, x)
            if met == "Зейделя": rez = gauss_seidel_method(A, x)   
            if met == "Гаусса-Жордана": rez = gauss_jordan_method(A, x)
            if met == "Якоби": rez = jacobi_method(A, x)

            if checkanswer(A,x,rez):
                self.label_a.setText("x1 = " + str(rez[0]))
                self.label_b.setText("x2 = " + str(rez[1]))
                if self.c1.text(): self.label_c.setText("x3 = " + str(rez[2]))
                if self.d1.text(): self.label_d.setText("x4 = " + str(rez[3]))
            else:
                self.label_a.setText("Что то пошло не так :(")
                self.label_b.setText("")
                self.label_c.setText("")
                self.label_d.setText("")

        else:
            rez = checkmatrix(A ,x)
            self.label_a.setText(rez)
            self.label_b.setText("")
            self.label_c.setText("")
            self.label_d.setText("")
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
