import sys
import matplotlib.pyplot as plt
from threading import Timer,Thread,Event

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QDial

x = [0]
y = [0]

tfinal = 2500
T = 1
q = int(tfinal/T)

# Regulator PD
Kr = 5
Td = 20
Tg = 2
v = 50

y = []
t = []
x = []
v1 = []

for i in range(q+1):
    if i<10:
        v1.append(0)
    else:
        v1.append(v)

# Initializare y, t, x
y.append(0)
t.append(0)
x.append(0)

class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event
        self.time = 2
        self.k=0
    
    def callback(self):
        if self.k >= q:
            self.stopped.set()
        else:
            self.calculatePD()
            plt.clf()
            plt.plot(t,y)
            plt.draw()

    def calculatePD(self):
        x.append((x[self.k] - T/Tg*x[self.k] + Kr*T/Tg*(1-Td/Tg)*v))
        y.append(x[self.k] + Kr*Td/Tg*v)
        t.append(self.k*T)
        self.k = self.k+1

    def run(self):
        while not self.stopped.wait(self.time):
            self.callback()

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.stopFlag = Event()

        self.setWindowTitle('Timer')
        self.setFixedSize(250, 200)

        self.start_btn = QPushButton(self)
        self.start_btn.setText("Start")
        self.start_btn.clicked.connect(self.start_clicked)
        layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton(self)
        self.stop_btn.setText("Stop")
        self.stop_btn.clicked.connect(self.stop_clicked)
        layout.addWidget(self.stop_btn)

        self.dial = QDial()
        self.dial.setMinimum(1)
        self.dial.setMaximum(10)
        self.dial.setValue(2)
        self.dial.valueChanged.connect(self.sliderMoved)
        layout.addWidget(self.dial)

    def sliderMoved(self):
        print("Dial value = %i" % (self.dial.value()))
        self.thread.time = self.dial.value()

    def startThread(self):
        self.stopFlag.clear()
        self.thread = MyThread(self.stopFlag)
        self.thread.start()
        self.showPlot()

    def showPlot(self):
        _,ax=plt.subplots()
        ax.scatter(t,y)
        plt.show()
        plt.draw()

    def start_clicked(self):
        print("Start clicked")
        self.startThread()

    def stop_clicked(self):
        print("Stop clicked")   
        self.stopFlag.set()

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
