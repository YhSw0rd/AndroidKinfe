import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Stream(QObject):
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initGui()
        sys.stdout = Stream(newText=self.onUpdateText)
    def initGui(self):
        self.layout = QVBoxLayout()

        self.btn1 = QPushButton('输出”Hello World! “')
        self.btn1.clicked.connect(self.printHello)

        self.consoleBox = QTextEdit(self, readOnly=True)

        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.consoleBox)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.show()
    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.consoleBox.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.consoleBox.setTextCursor(cursor)
        self.consoleBox.ensureCursorVisible()
        self.consoleBox.append(text)
    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)
    def printHello(self):
        print('Hello, World! ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())