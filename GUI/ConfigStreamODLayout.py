import numpy as np
import matplotlib.backends.backend_qt5agg as backQt5
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from statistics import mean, stdev
import numpy as np
from hurst import compute_Hc

from charge_generator import video_stream_charge
from traffic_analyser import video_stream_analyser

class StreamODLayout(object):
    def __init__(self, uiMainWindow):
        self.uiMainWindow = uiMainWindow
        self.canvasX = None

    def configStreamODLayout(self):
        self.uiMainWindow.widget_2.setVisible(False)
        self.uiMainWindow.analiseEstatStreamOD.setVisible(False)
        self.uiMainWindow.escalaStreamOD.setCurrentIndex(1)

        self.uiMainWindow.pushButtonStreamOD.clicked.connect(lambda: self.generateTraffic())
        self.uiMainWindow.escalaStreamOD.currentIndexChanged.connect(lambda: self.mudaEscala(self.uiMainWindow.escalaStreamOD.currentIndex()))
        self.uiMainWindow.numeroCarga.currentIndexChanged.connect( lambda: self.mudaCarga( self.uiMainWindow.numeroCarga.currentIndex() ) )

    def mudaEscala(self, comboIndex):
        a = [ 10, 1, 1/60 ]

        # Problema quando a escala é alterada
        pointsToPlot = video_stream_analyser(a[comboIndex], self.uiMainWindow.numeroCarga.currentIndex())

        self.plotOnCanvas( self.uiMainWindow.streamPlotLayout, pointsToPlot )

        self.uiMainWindow.widget_2.setVisible(True)
        self.mostraStreamODEstat(pointsToPlot)

    def mudaCarga(self, comboIndex):
        self.uiMainWindow.escalaStreamOD.setCurrentIndex(1)
        pointsToPlot = video_stream_analyser(1, comboIndex)
        self.mostraStreamODEstat(pointsToPlot)
        self.plotOnCanvas(self.uiMainWindow.streamPlotLayout, pointsToPlot)

    def atualizaLabel(self, state):
        labels = [ 'Tempo de vídeo' , 'Tempo médio de vídeo']
        self.uiMainWindow.maisCargasStreamODWidget.setVisible(state)
        self.uiMainWindow.label_3.setText( labels[int(state)] )

    def generateTraffic(self):
        # Padrões de codificação conhecidos
        video_codes = [91000, 180000, 469000, 978000, 2058000, 3953000, 9581000, 21373000]
        
        try:
            numeroCarga = 1
            if self.uiMainWindow.numeroCargas.toPlainText() != '':
                numeroCarga = int(self.uiMainWindow.numeroCargas.toPlainText())
            video_code = video_codes[ self.uiMainWindow.comboBox_3.currentIndex() ]
            tempoVideo = int(self.uiMainWindow.tempoVideo.toPlainText())

            self.uiMainWindow.tempoVideo.setText('')
            self.uiMainWindow.numeroCargas.setText('')

            self.uiMainWindow.numeroCarga.clear()
            for i in range(numeroCarga):
                self.uiMainWindow.numeroCarga.addItem('Carga ' + str(i))
            self.uiMainWindow.numeroCarga.setCurrentIndex(0)
            self.uiMainWindow.escalaStreamOD.setCurrentIndex(1)

            video_stream_charge(tempoVideo, video_code, numeroCarga)
            pointsToPlot = video_stream_analyser(1)

            self.uiMainWindow.widget_2.setVisible(True)
            self.plotOnCanvas(self.uiMainWindow.streamPlotLayout, pointsToPlot)
            self.mostraStreamODEstat(pointsToPlot)
        except ValueError:
            self.functText()

    def plotOnCanvas(self, canvasLayout, pointsToPlot, xLabel='Segundos', yLabel="Kbits"):
        if self.canvasX is None:
            canvas = backQt5.FigureCanvasQTAgg(Figure((5,3)))
            navi_bar = NavigationToolbar( canvas, self.uiMainWindow.widget_2 )
            canvasLayout.addWidget(canvas)
            canvasLayout.addWidget(navi_bar)

            self.canvasX = canvas.figure.subplots()
            self.canvasX.set_title('Plot vídeo sob demanda')
        else:
            self.canvasX.clear()

        t = np.linspace(0, (len(pointsToPlot) - 1), len(pointsToPlot))
        self.canvasX.vlines(t, [0], pointsToPlot, colors='blue' )

        self.canvasX.set_xlabel(xLabel)
        self.canvasX.set_ylabel(yLabel)
        self.canvasX.axis(ymax=max(pointsToPlot)*4/3)
        self.canvasX.figure.canvas.draw()

    def functText(self):
        print('Erro ao gerar carga de StreamOD')
    
    def mostraStreamODEstat(self, pointsToPlot):
        medidaTempo = [' milisegundos', ' segundos', ' minutos']
        medidaTaxa = [ ' Kbits/100 milisegundos', ' Kbits/segundo', ' Kbits/minuto' ]
        self.uiMainWindow.analiseEstatStreamOD.setVisible(True)
        self.uiMainWindow.mediaViewStreamOD.setText('{0:.2f} '.format(mean(pointsToPlot)) + medidaTaxa[self.uiMainWindow.escalaStreamOD.currentIndex()] )
        if len( pointsToPlot ) > 1:
            self.uiMainWindow.desvioViewStreamOD.setText('{0:.2f} '.format(stdev(pointsToPlot)) + medidaTaxa[self.uiMainWindow.escalaStreamOD.currentIndex()])
        else:
            self.uiMainWindow.desvioViewStreamOD.setText('Não há desvio com apenas 1 ponto')
        self.uiMainWindow.tempoTotalViewStreamOD.setText(str(len(pointsToPlot) - 1) + medidaTempo[self.uiMainWindow.escalaStreamOD.currentIndex()])

        if len(pointsToPlot) > 100:
            # diferences = [0]*len(pointsToPlot)
            # # diferences[0] = points[0]
            # for i in range(len(pointsToPlot)):
            #     diferences[i] = pointsToPlot[i] - pointsToPlot[i-1]
                
            H, c, data = compute_Hc(pointsToPlot, kind='change', simplified=False)
            self.uiMainWindow.hurstParameterStreamOD.setText('H={:.4f}, c={:.4f}'.format(H,c))
        else:
            self.uiMainWindow.hurstParameterStreamOD.setText('Sample com menos de 100 amostras')
            