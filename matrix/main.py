import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import numpy as np
from numpy import array, zeros, diag, diagflat, dot, linalg

ITERATION_LIMIT = 1000

a = []
b = []
c = []
met = "Крамера"
rez = []

def determinantOfMatrix(mat):
 
    ans = (mat[0][0] * (mat[1][1] * mat[2][2] -
                        mat[2][1] * mat[1][2]) -
           mat[0][1] * (mat[1][0] * mat[2][2] -
                        mat[1][2] * mat[2][0]) +
           mat[0][2] * (mat[1][0] * mat[2][1] -
                        mat[1][1] * mat[2][0]))
    return ans

def checkmatrix(a,b):

    a = np.array(a, float)
    b = np.array(b, float)

    d = [[a[0][0], a[0][1], a[0][2]],
         [a[1][0], a[1][1], a[1][2]],
         [a[2][0], a[2][1], a[2][2]]]

    d1 = [[b[0], a[0][1], a[0][2]],
          [b[1], a[1][1], a[1][2]],
          [b[2], a[2][1], a[2][2]]]
     
    d2 = [[a[0][0], b[0], a[0][2]],
          [a[1][0], b[1], a[1][2]],
          [a[2][0], b[2], a[2][2]]]

    d3 = [[a[0][0], a[0][1], b[0]],
          [a[1][0], a[1][1], b[1]],
          [a[2][0], a[2][1], b[2]]]

    D = determinantOfMatrix(d)
    D1 = determinantOfMatrix(d1)
    D2 = determinantOfMatrix(d2)
    D3 = determinantOfMatrix(d3) 
    
    if (D != 0):
        return
    else:
        if (D1 == 0 and D2 == 0 and D3 == 0):
            return 'Бесконечно решений'
            
        elif (D1 != 0 or D2 != 0 or D3 != 0):
            return 'Нет решения'

def gauss_jordan_method(a,b):
    a = np.array(a, float)
    b = np.array(b, float)
    n = len(b)
    checkmatrix(a,b)

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

def gauss_seidel_method(a, b, ITERATION_LIMIT):
    a = np.array(a, float)
    b = np.array(b, float)
    checkmatrix(a,b)
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
    checkmatrix(a,b)
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
    checkmatrix(a,b)
    n = len(a)
    M = a

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

 
# This function finds the solution of system of
# linear equations using cramer's rule
def findSolution(a,b):
    checkmatrix(a,b)
    a = np.array(a, float)
    b = np.array(b, float)
    # Matrix d using a as given in
    # cramer's rule
    d = [[a[0][0], a[0][1], a[0][2]],
         [a[1][0], a[1][1], a[1][2]],
         [a[2][0], a[2][1], a[2][2]]]
     
    # Matrix d1 using a as given in
    # cramer's rule
    d1 = [[b[0], a[0][1], a[0][2]],
          [b[1], a[1][1], a[1][2]],
          [b[2], a[2][1], a[2][2]]]
     
    # Matrix d2 using a as given in
    # cramer's rule
    d2 = [[a[0][0], b[0], a[0][2]],
          [a[1][0], b[1], a[1][2]],
          [a[2][0], b[2], a[2][2]]]
     
    # Matrix d3 using a as given in
    # cramer's rule
    d3 = [[a[0][0], a[0][1], b[0]],
          [a[1][0], a[1][1], b[1]],
          [a[2][0], a[2][1], b[2]]]
 
    # Calculating Determinant of Matrices
    # d, d1, d2, d3
    D = determinantOfMatrix(d)
    D1 = determinantOfMatrix(d1)
    D2 = determinantOfMatrix(d2)
    D3 = determinantOfMatrix(d3) 
    # Case 1
    if (D != 0):
       
        # Coeff have a unique solution.
        # Apply Cramer's Rule
        x = D1 / D
        y = D2 / D
         
        z = D3 / D 
         
        return [x,y,z]
    else:
        return [["Нет решения"], [], []]

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
        self.button.move(85, 130)
        self.button.clicked.connect(self.on_click)

        self.buttonF = QPushButton('Решить с файла', self)
        self.buttonF.move(200, 130)
        self.buttonF.clicked.connect(self.on_clickF)

        # 3x3
        self.a1 = QLineEdit("", self)
        self.a1.setGeometry(50, 50, 50, 20)

        self.a2 = QLineEdit("", self)
        self.a2.setGeometry(120, 50, 50, 20)

        self.a3 = QLineEdit("", self)
        self.a3.setGeometry(190, 50, 50, 20)


        self.b1 = QLineEdit("", self)
        self.b1.setGeometry(50, 75, 50, 20)

        self.b2 = QLineEdit("", self)
        self.b2.setGeometry(120,75, 50, 20)

        self.b3 = QLineEdit("", self)
        self.b3.setGeometry(190, 75, 50, 20)

        
        self.c1 = QLineEdit("", self)
        self.c1.setGeometry(50, 100, 50, 20)

        self.c2 = QLineEdit("", self)
        self.c2.setGeometry(120, 100, 50, 20)

        self.c3 = QLineEdit("", self)
        self.c3.setGeometry(190, 100, 50, 20)

        # =x3
        equally1 = QLabel("=", self)
        equally1.move(250, 50)
        equally2 = QLabel("=", self)
        equally2.move(250, 75)
        equally3 = QLabel("=", self)
        equally3.move(250, 100)

        self.x1 = QLineEdit("", self)
        self.x1.setGeometry(270, 50, 50, 20)
        self.x2 = QLineEdit("", self)
        self.x2.setGeometry(270, 75, 50, 20)
        self.x3 = QLineEdit("", self)
        self.x3.setGeometry(270, 100, 50, 20)

        self.combo = QComboBox(self)
        self.combo.addItems(["Крамера", "Гаусса", "Зейделя", "Гаусса-Жордана", "Якоби"])
        self.combo.move(55, 10)

        self.combo.activated.connect(self.handleActivated)

        self.label_a = QLabel('                                                                                                                ', self)
        self.label_a.move(10, 170)
        self.label_b = QLabel('                                                                                                                ', self)
        self.label_b.move(10, 190)
        self.label_c = QLabel('                                                                                                                ', self)
        self.label_c.move(10, 210)

    def handleActivated(self, index):
        global met
        met = self.combo.itemText(index)
        
    @pyqtSlot()
    def on_clickF(self):
        A = []
        x = []
        file = open("data.txt", "r")
        line = file.readline()
        for i in range(len(line)):
            if not line[i].isspace():
                A.append(float(line[i]))

        a = [A[0], A[1], A[2]]        
        b = [A[3], A[4], A[5]]    
        c = [A[6], A[7], A[8]]    
        A = [a, b, c]

        line = file.readline()
        for i in range(len(line)):
            if not line[i].isspace():
                x.append(float(line[i]))
 
        file.close

        print(A, x)

        if checkmatrix(A ,x) == None:

            if met == "Крамера":
                rez = findSolution(A, x)

            if met == "Гаусса":
                rez = gauss_method(A, x)

            if met == "Зейделя":    
                rez = gauss_seidel_method(A, x, 15)   
    
            if met == "Гаусса-Жордана":
                rez = gauss_jordan_method(A, x)

            if met == "Якоби":
                rez = jacobi_method(A, x)

            self.label_a.setText("a = " + str(rez[0]))
            self.label_b.setText("b = " + str(rez[1]))
            self.label_c.setText("c = " + str(rez[2]))

        else:
            rez = checkmatrix(A ,x)
            self.label_a.setText(rez)

        print(rez)



    def on_click(self):
        a.append(self.a1.text())
        a.append(self.a2.text())
        a.append(self.a3.text())
        b.append(self.b1.text())
        b.append(self.b2.text())
        b.append(self.b3.text())
        c.append(self.c1.text())
        c.append(self.c2.text())
        c.append(self.c3.text())
        x = [self.x1.text(), self.x2.text(), self.x3.text()]


        A = [a, b, c]        
        

        if checkmatrix(A ,x) == None:

            if met == "Крамера":
                rez = findSolution(A, x)

            if met == "Гаусса":
                rez = gauss_method(A, x)

            if met == "Зейделя":    
                rez = gauss_seidel_method(A, x, 15)   
    
            if met == "Гаусса-Жордана":
                rez = gauss_jordan_method(A, x)

            if met == "Якоби":
                rez = jacobi_method(A, x)

            self.label_a.setText("a = " + str(rez[0]))
            self.label_b.setText("b = " + str(rez[1]))
            self.label_c.setText("c = " + str(rez[2]))

        else:
            rez = checkmatrix(A ,x)
            self.label_a.setText(rez)
    
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())