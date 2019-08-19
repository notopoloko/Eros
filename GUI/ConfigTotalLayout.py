from GUI.ConfigLayout import ConfigLayout

class ConfigTotalLayout(ConfigLayout):
    def __init__ (self, uiMainWindow):
        self.uiMainWindow = uiMainWindow

    def configTotalLayout(self):
        self.uiMainWindow.iotTotalParam.setVisible(False)
        self.uiMainWindow.streamTotalParam.setVisible(False)
        self.uiMainWindow.voipTotalParam.setVisible(False)
        self.uiMainWindow.webTotalParams.setVisible(False)

        self.uiMainWindow.pushButtonTotal.clicked.connect (lambda: self.getTraffic())


    def getTraffic(self):
        pass