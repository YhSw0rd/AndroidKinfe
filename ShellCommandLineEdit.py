
from PyQt5.QtCore import pyqtSignal,QEvent
from PyQt5.QtWidgets import QLineEdit



class ShellCommandLineEdit(QLineEdit):
    focusIn = pyqtSignal(QEvent)
    focusOut = pyqtSignal(QEvent)
    def __init__(self,parent=None) -> None:
        super(ShellCommandLineEdit,self).__init__(parent)

    def focusInEvent(self,event):
        self.focusIn.emit(event)
    
    def focusOutEvent(self,event):
        self.focusOut.emit(event)