

from PyQt5 import QtWidgets
class ConsoleTab(QtWidgets.QWidget):
    console:QtWidgets.QTextEdit = None

    def setConsole(self,console:QtWidgets.QTextEdit):
        self.console = console

    def getConsole(self):
        return self.console