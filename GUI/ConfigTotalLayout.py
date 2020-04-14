from GUI.ConfigLayout import ConfigLayout
from traffic_analyser import IOT_total_analyser, voip_total_analyser, web_total_analyser, video_stream_total_analyser
import _thread
import threading

class ConfigTotalLayout(ConfigLayout):
    def __init__ (self, uiMainWindow, iotLayout, voipLayout, webLayout, streamLayout):
        super().__init__(uiMainWindow)
        self.iotLayout = iotLayout
        self.voipLayout = voipLayout
        self.webLayout = webLayout
        self.streamLayout = streamLayout

    def configTotalLayout(self):
        self.uiMainWindow.totalPlotWidget.setVisible(False)
        self.uiMainWindow.analiseEstatTotal.setVisible(False)
        self.uiMainWindow.widget.setVisible(False)

        self.uiMainWindow.pushButtonTotal.clicked.connect (lambda: self.getTraffic())


    def getTraffic(self):
        initTime = 0
        if self.uiMainWindow.tempoInicialTotal.toPlainText() != '':
            initTime = int(self.uiMainWindow.tempoInicialTotal.toPlainText())
        endTime = int(self.uiMainWindow.tempoFinalTotal.toPlainText())

        pointsToPlot = [0] * (endTime-initTime)
        individualCharge = [0] * 4
        # totalTrafficIOT = 0
        # totalTrafficVoip = 0
        # totalTrafficWeb = 0
        # totalTrafficVoD = 0

        try:
            iotThread = threading.Thread(target=IOT_total_analyser, args=(pointsToPlot, self.uiMainWindow.bytesIOT, self.iotLayout.getNumeroCargas(), initTime, endTime ))
            voipThread = threading.Thread(target=voip_total_analyser, args=(pointsToPlot, self.uiMainWindow.byteVoip, self.voipLayout.getNumeroCargas(), initTime, endTime))
            webThread = threading.Thread(target=web_total_analyser, args=(pointsToPlot, self.uiMainWindow.bytesWeb, self.webLayout.getNumeroCargas(), initTime, endTime))
            iotThread.start()
            voipThread.start()
            webThread.start()
            # _thread.start_new_thread(web_total_analyser, ( ))
            # _thread.start_new_thread(video_stream_total_analyser, (pointsToPlot, self.uiMainWindow.bytesVoD ))
            iotThread.join()
            voipThread.join()
            webThread.join()
        except Exception as exp:
            print('Erro ao tentar abrir thread\n' + exp.__str__())

        self.plotOnCanvas(self.uiMainWindow.TotalPlotLayout, pointsToPlot, 'Total Plot Layout', xLabel='Minutos')
        self.mostraStat(pointsToPlot, self.uiMainWindow.mediaTotalView, self.uiMainWindow.desvioTotalView, self.uiMainWindow.tempoTotalView, self.uiMainWindow.hurstTotalView)

        totalCharge = sum(pointsToPlot)

        # self.uiMainWindow.byteVoip.setText(str(totalTrafficVoip))
        # self.uiMainWindow.bytesIOT.setText(str(totalTrafficIOT))
        # self.uiMainWindow.bytesVoD.setText(str(totalTrafficVoD))
        # self.uiMainWindow.bytesWeb.setText(str(totalTrafficWeb))
        self.uiMainWindow.bytesTotal.setText(str(totalCharge))
        self.uiMainWindow.percentTotal.setText('100%')

        self.uiMainWindow.analiseEstatTotal.setVisible(True)
        self.uiMainWindow.totalPlotWidget.setVisible(True)
        self.uiMainWindow.widget.setVisible(True)