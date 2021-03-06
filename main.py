import sys
from PyQt5 import QtWidgets

from GUI.Charge_generator.mainwindow1 import Ui_Gerador
from GUI.ConfigVoIPLayout import ConfigVoIPLayout
from GUI.ConfigStreamODLayout import StreamODLayout
from GUI.ConfigWEBLayout import ConfigWEBLayout
from GUI.ConfigIOTLayout import ConfigIOTLayout
from GUI.ConfigTotalLayout import ConfigTotalLayout

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_Gerador()

    mainWindow = QtWidgets.QMainWindow()
    ex.setupUi(mainWindow)

    voipLayout = ConfigVoIPLayout(ex)
    voipLayout.configVoIPTabLayout()

    streamODLayout = StreamODLayout(ex)
    streamODLayout.configStreamODLayout()

    configIOTLayout = ConfigIOTLayout(ex)
    configIOTLayout.configIOTLayout()

    webLayout = ConfigWEBLayout(ex)
    webLayout.configWEBTabLayout()

    totalLayout = ConfigTotalLayout(ex, configIOTLayout, voipLayout, webLayout, streamODLayout)
    totalLayout.configTotalLayout()

    mainWindow.show()

    sys.exit(app.exec_())