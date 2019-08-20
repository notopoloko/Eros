import matplotlib.backends.backend_qt5agg as backQt5
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from hurst import compute_Hc
from statistics import mean, stdev
from itertools import groupby

from charge_generator import iot_charge
from traffic_analyser import IOT_analyser
from GUI.ConfigLayout import ConfigLayout

class ConfigIOTLayout(ConfigLayout):
    def __init__(self, uiMainWindow):
        super().__init__(uiMainWindow)

    def configIOTLayout(self):
        self.uiMainWindow.widget_4.setVisible(False)
        self.uiMainWindow.analiseEstatIOT.setVisible(False)

        self.uiMainWindow.pushButtonIOT.clicked.connect( lambda: self.gerarTrafegoIOT() )
        self.uiMainWindow.escalaIOT.currentIndexChanged.connect( lambda: self.mudaEscala(self.uiMainWindow.escalaIOT.currentIndex()) )
        self.uiMainWindow.numeroCargaIOT.currentIndexChanged.connect( lambda: self.mudaCarga(self.uiMainWindow.numeroCargaIOT.currentIndex()) )

    def gerarTrafegoIOT(self):
        numberOfCharges = 1
        if self.uiMainWindow.numeroDispositivos.toPlainText() != '':
            numberOfCharges = int(self.uiMainWindow.numeroDispositivos.toPlainText())
            
        try:
            tamanhoMensagem = int(self.uiMainWindow.tamanhoMensagem.toPlainText())
            tempoMensagem = int(self.uiMainWindow.tempoMensagem.toPlainText())
            iot_charge(tamanhoMensagem, numberOfCharges, tempoMensagem)

            self.uiMainWindow.tamanhoMensagem.setText('')
            self.uiMainWindow.numeroDispositivos.setText('')
            self.uiMainWindow.tempoMensagem.setText('')

            self.uiMainWindow.numeroCargaIOT.clear()
            for i in range(numberOfCharges):
                self.uiMainWindow.numeroCargaIOT.addItem('Carga ' + str(i))

            pointsToPlot = IOT_analyser(1)
            self.uiMainWindow.widget_4.setVisible(True)
            # self.plotOnCanvas( self.uiMainWindow.IOTPlotLayout, pointsToPlot, 'Plot vídeo sob demanda', graphicColor='indigo' )
            self.plotOnCanvas( pointsToPlot )
            self.mostraIOTStat( pointsToPlot )
        except ValueError as ve:
            print('Erro ao criar carga', str(ve))

    # TODO: Arrumar método
    def plotOnCanvas(self, pointsToPlot, xLabel='Minutos', yLabel="bytes"):
        if self.canvasX is None:
            canvas = backQt5.FigureCanvasQTAgg(Figure((5,3)))
            navi_bar = NavigationToolbar( canvas, self.uiMainWindow.widget_4 )
            self.uiMainWindow.IOTPlotLayout.addWidget(canvas)
            self.uiMainWindow.IOTPlotLayout.addWidget(navi_bar)
            self.canvasX = canvas.figure.subplots()
        else:
            self.canvasX.clear()
        heigth = { key: len(list(group))*pointsToPlot[1] for key, group in groupby(pointsToPlot[0]) }
        self.canvasX.set_title('Plot vídeo sob demanda')
        self.canvasX.vlines(heigth.keys(), [0], heigth.values(), colors='indigo' )

        self.canvasX.set_xlabel(xLabel)
        self.canvasX.set_ylabel(yLabel)
        self.canvasX.axis(xmin=0 , ymax=2*max(heigth.values()))
        self.canvasX.figure.canvas.draw()
    
    def mudaEscala(self, comboIndex):
        a = [ 1, 1/60 ]
        xlabel = ['Minutos', 'Horas']

        pointsToPlot = IOT_analyser(a[comboIndex], self.uiMainWindow.numeroCargaIOT.currentIndex())

        # self.plotOnCanvas(self.uiMainWindow.IOTPlotLayout, pointsToPlot, 'Plot vídeo sob demanda', xlabel[self.uiMainWindow.escalaIOT.currentIndex()], graphicColor='indigo')
        self.plotOnCanvas( pointsToPlot )

        self.uiMainWindow.widget_4.setVisible(True)
        self.mostraIOTStat(pointsToPlot)

    def mudaCarga(self, chargeNumber):
        self.uiMainWindow.escalaIOT.setCurrentIndex(0)
        xlabel = ['Minutos', 'Horas']

        pointsToPlot = IOT_analyser(1, chargeNumber)

        # self.plotOnCanvas(self.uiMainWindow.IOTPlotLayout, pointsToPlot, 'Plot vídeo sob demanda', xlabel[self.uiMainWindow.escalaIOT.currentIndex()], graphicColor='indigo')
        self.plotOnCanvas( pointsToPlot )

        self.uiMainWindow.widget_4.setVisible(True)
        self.mostraIOTStat(pointsToPlot)


    def mostraIOTStat(self, pointsToPlot):
        medidaTempo = [' minutos', ' horas']
        medidaTaxa = [' bytes/minutos', ' bytes/hora' ]
        self.uiMainWindow.analiseEstatIOT.setVisible(True)
        numberOfPoints = len(pointsToPlot[0])

        allPoints = [0]*(pointsToPlot[0][numberOfPoints - 1] + 1)
        for i in pointsToPlot[0]:
            allPoints[int(i)] += pointsToPlot[1]

        self.uiMainWindow.mediaViewIOT.setText('{0:.2f} '.format(numberOfPoints*pointsToPlot[1] / pointsToPlot[0][numberOfPoints - 1]) + medidaTaxa[self.uiMainWindow.escalaIOT.currentIndex()] )
        # if len( pointsToPlot ) > 1:
        #     self.uiMainWindow.desvioViewIOT.setText('{0:.2f} '.format(stdev(pointsToPlot)) + medidaTaxa[self.uiMainWindow.escalaIOT.currentIndex()])
        # else:
        self.uiMainWindow.desvioViewIOT.setText('{0:.2f}'.format(stdev(allPoints)) + medidaTaxa[self.uiMainWindow.escalaIOT.currentIndex()] )
        self.uiMainWindow.tempoTotalIOT.setText( str(pointsToPlot[0][len(pointsToPlot[0]) - 1]) + medidaTempo[self.uiMainWindow.escalaIOT.currentIndex()])
        if len(allPoints) > 100:
            # diferences = [0]*len(points)
            # # diferences[0] = points[0]
            # for i in range(len(points)):
            #     diferences[i] = points[i] - points[i-1]
                
            H, c, data = compute_Hc(allPoints, kind='change', simplified=False)
            self.uiMainWindow.hurstParametroIOT.setText('H={:.4f}, c={:.4f}'.format(H,c))
        else:
            self.uiMainWindow.hurstParametroIOT.setText('Sample com menos de 100 amostras')

    def funcText(self):
        print('Erro ao gerar tráfego IOT')