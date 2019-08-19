import numpy as np
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.backends.backend_qt5agg as backQt5


class ConfigLayout(object):
    def __init__(self, uiMainWindow):
        self.uiMainWindow = uiMainWindow
        self.canvasX = None

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

    def mostraStat(self, points, mediaView, desvioView, tempoTotalView, hurstView):
        pass