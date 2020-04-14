import matplotlib.backends.backend_qt5agg as backQt5
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
import numpy as np
from statistics import mean, stdev
from hurst import compute_Hc

from charge_generator import web_charge, voip_charge, video_stream_charge
from traffic_analyser import voip_analyser, video_stream_analyser, web_analyser
from GUI.ConfigLayout import ConfigLayout

class ConfigWEBLayout(ConfigLayout):
    def __init__(self, uiMainWindow):
        super().__init__(uiMainWindow)

    def functText(self, texto =''):
        print('Uma mensagem de teste: ' + texto)

    def mostraStatWEB( self, points ):
        medidaTempo = [' milisegundos', ' segundos', ' minutos']
        medidaTaxa = [ ' byts/100 milisegundos', ' bytes/segundo', 'byts/minuto' ]
        self.uiMainWindow.analiseEstatWeb.setVisible(True)
        self.uiMainWindow.mediaViewWEB.setText('{0:.2f} '.format(mean(points)) + medidaTaxa[1] )
        if len(points) > 1:
            self.uiMainWindow.desvioViewWEB.setText('{0:.2f} '.format(stdev(points)) + medidaTaxa[1])
        else:
            self.uiMainWindow.desvioViewWEB.setText('Não há desvio para um único tempo')
        self.uiMainWindow.tempoTotalViewWEB.setText(str(len(points)) + medidaTempo[self.uiMainWindow.comboBox_2.currentIndex()])
        if len(points) > 100:
            # diferences = [0]*len(points)
            # # diferences[0] = points[0]
            # for i in range(len(points)):
            #     diferences[i] = points[i] - points[i-1]
            H, c, data = compute_Hc(points, kind='change', simplified=False)
            self.uiMainWindow.HurstViewWEB.setText('H={:.4f}, c={:.4f}'.format(H,c))
        else:
            self.uiMainWindow.HurstViewWEB.setText('Sample com menos de 101 amostras')

    def generateWEBPlot( self ):
        try:
            self.numeroCargas = 1
            if self.uiMainWindow.numeroCargsWeb.toPlainText() != '':
                self.numeroCargas = int(self.uiMainWindow.numeroCargsWeb.toPlainText())
            tempoMedio = int(self.uiMainWindow.tempoCargaWeb.toPlainText())

            self.uiMainWindow.numeroCargsWeb.setText('')
            self.uiMainWindow.tempoCargaWeb.setText('')
            # self.uiMainWindow.comboBox.setVisible(True)

            web_charge(tempoMedio, self.numeroCargas)
            self.uiMainWindow.numeroCargaWEB.clear()

            for i in range(self.numeroCargas):
                self.uiMainWindow.numeroCargaWEB.addItem( 'Carga ' + str(i + 1))

            pointsToPlot = web_analyser(0)
            # self.uiMainWindow.comboBox_2.setCurrentIndex(1)
            self.uiMainWindow.numeroCargaWEB.setCurrentIndex(0)
            # plotar no canvas
            self.plotOnCanvas(self.uiMainWindow.webPlotLayout, pointsToPlot, 'Plot WEB')
            self.uiMainWindow.widgetWEB.setVisible(True)
            self.mostraStatWEB(pointsToPlot)
            # canvasX.set_xlabel('Segundos')
            # canvasX.set_ylabel('Kbps')
        except ValueError as e:
            self.functText(str(e))

    def mudarEscalaPlot( self, comboIndex ):
        a = [ 10, 1, 1/60 ]
        xLabel = ['100 Milisegundos', 'Segundos', 'Minutos']

        # Problema quando a escala é alterada
        pointsToPlot = web_analyser(a[comboIndex], self.uiMainWindow.comboBox.currentIndex())

        self.plotOnCanvas(self.uiMainWindow.webPlotLayout, pointsToPlot, 'Plot WEB', xLabel[comboIndex] )

        self.uiMainWindow.widgetVoIPPlot.setVisible(True)
        self.mostraStatWEB( pointsToPlot)

    def mudaPlot(self, comboIndex):
        # self.uiMainWindow.comboBox_2.setCurrentIndex(1)
        if comboIndex < 0:
            return
        pointsToPlot = web_analyser(1, comboIndex)
        self.plotOnCanvas(self.uiMainWindow.webPlotLayout, pointsToPlot, 'Plot WEB')
        self.mostraStatWEB(pointsToPlot)

    def configWEBTabLayout(self):
        initState = False
        self.uiMainWindow.analiseEstatWeb.setVisible(initState)
        self.uiMainWindow.widgetWEB.setVisible(initState)
        # self.uiMainWindow.comboBox.setVisible(initState)
        self.uiMainWindow.escalaWEB.setCurrentIndex(1)

        self.uiMainWindow.pushButtonWeb.clicked.connect( lambda: self.generateWEBPlot( ))

        # self.uiMainWindow.comboBox_2.currentIndexChanged.connect(lambda: self.mudarEscalaPlot( self.uiMainWindow.comboBox_2.currentIndex() ))
        self.uiMainWindow.numeroCargaWEB.currentIndexChanged.connect(lambda: self.mudaPlot( self.uiMainWindow.numeroCargaWEB.currentIndex() ))
    # UI.comboBox_2.

