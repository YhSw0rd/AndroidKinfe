from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import pyqtSignal


class AndroidTextEdit(QTextEdit):
    listforward = pyqtSignal()
    def __init__(self,parent=None) -> None:
        super(AndroidTextEdit,self).__init__(parent)
        self.menu = QMenu()
        self.copyAction = self.menu.addAction("复制")
        self.selectallAction = self.menu.addAction("全选")
        self.clearAction = self.menu.addAction("清空")
        self.listforwardAction = self.menu.addAction("转发列表")

        self.copyAction.triggered.connect(self.copy_event)
        self.selectallAction.triggered.connect(self.selectall_event)
        self.clearAction.triggered.connect(self.clear_event)
        self.listforwardAction.triggered.connect(self.listforward_event)
        
        
    def contextMenuEvent(self,event):
        self.menu.exec_(event.globalPos())

    def copy_event(self):
        self.copy()

    def selectall_event(self):
        self.selectAll()

    def clear_event(self):
        self.clear()

    def listforward_event(self):
        self.listforward.emit()