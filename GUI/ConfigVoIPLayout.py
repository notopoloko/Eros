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

class ConfigVoIPLayout(ConfigLayout):
    def __init__(self, uiMainWindow):
        super().__init__(uiMainWindow)

    def functText(self, texto =''):
        print('Uma mensagem de teste: ' + texto)

    def mostraStatVoIP( self, points ):
        medidaTempo = [' milisegundos', ' segundos', ' minutos']
        medidaTaxa = [ ' bits/100 milisegundos', ' bits/segundo', 'bits/minuto' ]
        self.uiMainWindow.analiseEstatVoIP.setVisible(True)
        self.uiMainWindow.mediaViewVoIP.setText('{0:.2f} '.format(mean(points)) + medidaTaxa[self.uiMainWindow.comboBox_2.currentIndex()] )
        if len(points) > 1:
            self.uiMainWindow.desvioViewVoIP.setText('{0:.2f} '.format(stdev(points)) + medidaTaxa[self.uiMainWindow.comboBox_2.currentIndex()])
        else:
            self.uiMainWindow.desvioViewVoIP.setText('Não há desvio para um único tempo')
        self.uiMainWindow.tempoTotalViewVoip.setText(str(len(points) - 1) + medidaTempo[self.uiMainWindow.comboBox_2.currentIndex()])
        if len(points) > 100:
            # diferences = [0]*len(points)
            # # diferences[0] = points[0]
            # for i in range(len(points)):
            #     diferences[i] = points[i] - points[i-1]
                
            H, c, data = compute_Hc(points, kind='change', simplified=False)
            self.uiMainWindow.hurstParameterVoIP.setText('H={:.4f}, c={:.4f}'.format(H,c))
        else:
            self.uiMainWindow.hurstParameterVoIP.setText('Sample com menos de 100 amostras')

    def generateVoipPlot( self ):
        try:
            numeroCargas = 1
            if self.uiMainWindow.numeroCargasVoIP.toPlainText() != '':
                numeroCargas = int(self.uiMainWindow.numeroCargasVoIP.toPlainText())
            tempoMedio = int(self.uiMainWindow.duracao.toPlainText())

            self.uiMainWindow.numeroCargasVoIP.setText('')
            self.uiMainWindow.duracao.setText('')
            self.uiMainWindow.comboBox.setVisible(True)

            voip_charge(tempoMedio, numeroCargas)
            self.uiMainWindow.comboBox.clear()

            for i in range(numeroCargas):
                self.uiMainWindow.comboBox.addItem( 'Carga ' + str(i + 1))

            pointsToPlot = voip_analyser(1)
            self.uiMainWindow.comboBox_2.setCurrentIndex(1)
            self.uiMainWindow.comboBox.setCurrentIndex(0)
            # plotar no canvas
            self.plotOnCanvas(self.uiMainWindow.voipPlotLayout_2, pointsToPlot, 'Plot VoIP', graphicColor='blue')
            self.uiMainWindow.widgetVoIPPlot.setVisible(True)
            self.mostraStatVoIP(pointsToPlot)
            # canvasX.set_xlabel('Segundos')
            # canvasX.set_ylabel('Kbps')
        except ValueError as e:
            self.functText(str(e))

    def mudarEscalaPlot( self, comboIndex ):
        a = [ 10, 1, 1/60 ]
        xLabel = ['100 Milisegundos', 'Segundos', 'Minutos']

        # Problema quando a escala é alterada
        pointsToPlot = voip_analyser(a[comboIndex], self.uiMainWindow.comboBox.currentIndex())

        self.plotOnCanvas( self.uiMainWindow.voipPlotLayout_2, pointsToPlot, 'Plot VoIP', xLabel[comboIndex], graphicColor='blue')

        self.uiMainWindow.widgetVoIPPlot.setVisible(True)
        self.mostraStatVoIP( pointsToPlot)

    def mudaPlot(self, comboIndex):
        self.uiMainWindow.comboBox_2.setCurrentIndex(1)
        pointsToPlot = voip_analyser(1, comboIndex)
        self.plotOnCanvas(self.uiMainWindow.voipPlotLayout_2, pointsToPlot, 'Plot VoIP', graphicColor='blue')
        self.mostraStatVoIP(pointsToPlot)

    def configVoIPTabLayout(self):
        initState = False
        self.uiMainWindow.analiseEstatVoIP.setVisible(initState)
        self.uiMainWindow.widgetVoIPPlot.setVisible(initState)
        # self.uiMainWindow.comboBox.setVisible(initState)
        self.uiMainWindow.comboBox_2.setCurrentIndex(1)

        self.uiMainWindow.pushButtonVoip.clicked.connect( lambda: self.generateVoipPlot( ))

        self.uiMainWindow.comboBox_2.currentIndexChanged.connect(lambda: self.mudarEscalaPlot( self.uiMainWindow.comboBox_2.currentIndex() ))
        self.uiMainWindow.comboBox.currentIndexChanged.connect(lambda: self.mudaPlot( self.uiMainWindow.comboBox.currentIndex() ))
    # UI.comboBox_2.
