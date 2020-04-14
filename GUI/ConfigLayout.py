import numpy as np
import matplotlib.backends.backend_qt5agg as backQt5
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from hurst import compute_Hc
from statistics import stdev, mean


class ConfigLayout(object):
    def __init__(self, uiMainWindow):
        self.uiMainWindow = uiMainWindow
        self.canvasX = None
        self.numeroCargas = 0

    def plotOnCanvas(self, plotLayout, pointsToPlot, title, xLabel = 'Segundos', yLabel = 'bytes', graphicColor='red'):
        if self.canvasX is None:
            canvas = backQt5.FigureCanvasQTAgg(Figure((5,3)))
            navi_bar = NavigationToolbar( canvas, self.uiMainWindow.widgetWEB )

            plotLayout.addWidget(canvas)
            plotLayout.addWidget(navi_bar)

            self.canvasX = canvas.figure.subplots()
            self.canvasX.set_title( title )
        else:
            self.canvasX.clear()

        t = np.linspace(0, len(pointsToPlot) - 1, len(pointsToPlot))
        self.canvasX.vlines( t, [0] , pointsToPlot, colors=graphicColor)

        self.canvasX.set_xlabel( xLabel )
        self.canvasX.set_ylabel( yLabel )
        self.canvasX.axis(ymax = max( pointsToPlot ) *4/3)
        self.canvasX.figure.canvas.draw()

    # TODO: Arrumar escala
    def mostraStat(self, pointsToPlot, mediaView, desvioView, tempoTotalView, hurstView):
        medidaTempo = [' segundos']
        medidaTaxa = [' bytes/segundo']
        # self.uiMainWindow.analiseEstatIOT.setVisible(True)

        mediaView.setText('{0:.2f} '.format(mean(pointsToPlot)) + medidaTaxa[0] )
        # if len( pointsToPlot ) > 1:
        #     self.uiMainWindow.desvioViewIOT.setText('{0:.2f} '.format(stdev(pointsToPlot)) + medidaTaxa[self.uiMainWindow.escalaIOT.currentIndex()])
        # else:
        desvioView.setText('{0:.2f}'.format(stdev(pointsToPlot)) + medidaTaxa[0] )
        tempoTotalView.setText( str( len(pointsToPlot) ) + medidaTempo[0])
        if len(pointsToPlot) > 100:
            # diferences = [0]*len(points)
            # # diferences[0] = points[0]
            # for i in range(len(points)):
            #     diferences[i] = points[i] - points[i-1]
            try:
                H, c, _ = compute_Hc(pointsToPlot, kind='change', simplified=False)
                if H > 1:
                    hurstView.setText('H > 1 não é um valor válido')
                    return
                hurstView.setText('H={:.4f}, c={:.4f}'.format(H,c))
            except FloatingPointError as fpe:
                hurstView.setText('Unable to calculate Hurst value with current series')
                print('Erro no calculo do valor de hurst: ' + fpe.__str__())
        else:
            hurstView.setText('Sample com menos de 101 amostras')

    def getNumeroCargas(self):
        return self.numeroCargas