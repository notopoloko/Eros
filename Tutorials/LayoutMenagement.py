import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QAction, QMenu, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QTextEdit

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        quitAction = QAction('Close Window', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.triggered.connect(self.closeWindow)

        self.addAction(quitAction)

        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15, 10)

        lbl2 = QLabel('tutorial', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for programers', self)
        lbl3.move(55, 70)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Absolute')
        self.show()

    def closeWindow(self):
        print('Closing. Bye, bye.')

class Example1(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        ok_button = QPushButton('OK')
        cancel_button = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addWidget(cancel_button)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox.addWidget(QPushButton('Something here'))
        hbox.addWidget(QPushButton('Another here'))

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addLayout(hbox1)

        allbox = QVBoxLayout()
        allbox.addStretch(2)
        allbox.addLayout(vbox)
        allbox.addLayout(vbox1)

        self.setLayout(allbox)
        

        self.setGeometry(300,300,300,150)
        self.setWindowTitle('Buttons')
        self.show()


class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']

        positions = [(i,j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

        self.move(300,150)
        self.setWindowTitle('Calculator')
        self.show()

class Example3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QEdi


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # ex = Example()
    # ex1 = Example1()
    ex2 = Example2()
    sys.exit(app.exec_())