from GUI.ConfigLayout import ConfigLayout
from traffic_analyser import IOT_total_analyser, voip_total_analyser, web_total_analyser, video_stream_total_analyser
import _thread

class ConfigTotalLayout(ConfigLayout):
    def __init__ (self, uiMainWindow):
        super().__init__(uiMainWindow)

    def configTotalLayout(self):
        self.uiMainWindow.iotTotalParam.setVisible(False)
        self.uiMainWindow.streamTotalParam.setVisible(False)
        self.uiMainWindow.voipTotalParam.setVisible(False)
        self.uiMainWindow.webTotalParams.setVisible(False)
        
        self.uiMainWindow.analiseEstatTotal.setVisible(False)
        self.uiMainWindow.widget.setVisible(False)

        self.uiMainWindow.pushButtonTotal.clicked.connect (lambda: self.getTraffic())


    def getTraffic(self):
        pointsToPlot = [0]*1440
        # totalTrafficIOT = 0
        # totalTrafficVoip = 0
        # totalTrafficWeb = 0
        # totalTrafficVoD = 0

        try:
            _thread.start_new_thread(IOT_total_analyser, (pointsToPlot, self.uiMainWindow.bytesIOT ))
            _thread.start_new_thread(voip_total_analyser, (pointsToPlot, self.uiMainWindow.byteVoip ))
            _thread.start_new_thread(web_total_analyser, (pointsToPlot, self.uiMainWindow.bytesWeb ))
            _thread.start_new_thread(video_stream_total_analyser, (pointsToPlot, self.uiMainWindow.bytesVoD ))
        except Exception as exp:
            print('Erro ao tentar abrir thread\n' + exp.__str__())

        self.plotOnCanvas(self.uiMainWindow.TotalPlotLayout, pointsToPlot, 'Total Plot Layout', xLabel='Minutos')
        self.mostraStat(pointsToPlot, self.uiMainWindow.mediaTotalView, self.uiMainWindow.desvioTotalView, self.uiMainWindow.tempoTotalView, self.uiMainWindow.hurstTotalView)

        # self.uiMainWindow.byteVoip.setText(str(totalTrafficVoip))
        # self.uiMainWindow.bytesIOT.setText(str(totalTrafficIOT))
        # self.uiMainWindow.bytesVoD.setText(str(totalTrafficVoD))
        # self.uiMainWindow.bytesWeb.setText(str(totalTrafficWeb))
        self.uiMainWindow.bytesTotal.setText(str(250))

        self.uiMainWindow.analiseEstatTotal.setVisible(True)
        self.uiMainWindow.widget.setVisible(True)