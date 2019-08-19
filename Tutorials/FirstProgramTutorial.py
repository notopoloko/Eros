import sys
from PyQt5.QtWidgets import ( QApplication, QWidget, QPushButton, QToolTip, QMessageBox,
                            QDesktopWidget, QMainWindow, QAction, qApp, QMenu, QTextEdit )
from PyQt5.QtGui import QIcon, QFont

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.updateUI()
    
    def updateUI(self):
        QToolTip.setFont(QFont('SansSerif', 8))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50,50)

        qbtn = QPushButton('Exit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50,25)

        self.resize(250, 150)
        self.center()
        self.setWindowTitle('Tooltips')
        self.setWindowIcon(QIcon('Carga_VoIP.PNG'))
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Example1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAct = QAction(QIcon('Carga_VoIP.PNG'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit aplication')
        exitAct.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

        anotherAct = QAction('Some more text here', self)
        anotherAct.setStatusTip('Another lot of text here')
        anotherAct.triggered.connect(self.printMsg)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        menubar = self.menuBar()

        viewMenu = menubar.addMenu('View')

        viewStatAct = QAction('View Statusbar', self, checkable=True)
        viewStatAct.setStatusTip('View Statusbar')
        viewStatAct.setChecked(True)
        viewStatAct.triggered.connect(self.toogleMenu)

        viewMenu.addAction(viewStatAct)

        impMenu = QMenu('Import', self)
        impAct = QAction('Some action here', self, checkable=True)
        impAct.setStatusTip('Some text here')
        impMenu.addAction(impAct)

        newAct = QAction('New', self)
        newAct.triggered.connect(self.printMsg)

        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(newAct)
        fileMenu.addMenu(impMenu)
        fileMenu.addAction(anotherAct)

        self.setGeometry(300,300,250,150)
        self.setWindowTitle('Statusbar')
        self.show()

    def printMsg(self):
        print('Some text here')

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        newAct1 = cmenu.addAction('new')
        openAct = cmenu.addAction('open')
        quitAct = cmenu.addAction('Quit')
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()

    def toogleMenu(self, state):
        if state == False:
            self.statusbar.hide()
        else:
            self.statusbar.show()


class Example2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.textEdit = QTextEdit(self)
        self.textEdit.setText('Something')
        self.setCentralWidget(self.textEdit)

        exitAct = QAction(QIcon('Carga_VoIP.PNG'), 'Exit', self)
        exitAct.setShortcut('Crtl+Q')
        exitAct.setStatusTip('Exit Application')
        exitAct.triggered.connect(self.close)

        printAct = QAction(QIcon('Icons/print.png'), 'Print', self)
        printAct.setToolTip('Print Text on console')
        printAct.triggered.connect(self.printMsg)

        self.statusBar()

        menubar = self.menuBar()
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAct)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)
        toolbar.addAction(printAct)

        self.setGeometry(300,300,700,650)
        self.setWindowTitle('Main window')
        self.show()

    def printMsg(self):
        print(self.textEdit.toPlainText())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = Example()
    # ex1 = Example1()
    ex2 = Example2()
    # w = QWidget()
    # w.resize(250,150)
    # w.move(300,300)
    # w.setWindowTitle('Simple')
    # w.show()

    sys.exit(app.exec_())