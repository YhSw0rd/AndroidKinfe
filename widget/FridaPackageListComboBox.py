
from PyQt5 import QtWidgets,QtCore


class FridaPackageListComboBox(QtWidgets.QComboBox):
    focusIn = QtCore.pyqtSignal(QtCore.QEvent)
    def __init__(self,parent=None) -> None:
        super(FridaPackageListComboBox,self).__init__(parent)
        
    def focusInEvent(self,event):
        self.focusIn.emit(event)