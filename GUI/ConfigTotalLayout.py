from GUI.ConfigLayout import ConfigLayout
from traffic_analyser import IOT_total_analyser, voip_total_analyser, web_total_analyser

class ConfigTotalLayout(ConfigLayout):
    def __init__ (self, uiMainWindow):
        super().__init__(uiMainWindow)

    def configTotalLayout(self):
        self.uiMainWindow.iotTotalParam.setVisible(False)
        self.uiMainWindow.streamTotalParam.setVisible(False)
        self.uiMainWindow.voipTotalParam.setVisible(False)
        self.uiMainWindow.webTotalParams.setVisible(False)
        
        self.uiMainWindow.analiseEstatTotal.setVisible(False)

        self.uiMainWindow.pushButtonTotal.clicked.connect (lambda: self.getTraffic())


    def getTraffic(self):
        pointsToPlot = [0]*1440
        IOT_total_analyser(pointsToPlot)
        # voip_total_analyser(pointsToPlot)
        web_total_analyser(pointsToPlot)


        self.plotOnCanvas(self.uiMainWindow.TotalPlotLayout, pointsToPlot, 'Total Plot Layout')
        self.mostraStat(pointsToPlot, self.uiMainWindow.mediaTotalView, self.uiMainWindow.desvioTotalView, self.uiMainWindow.tempoTotalView, self.uiMainWindow.hurstTotalView)
        self.uiMainWindow.analiseEstatTotal.setVisible(True)