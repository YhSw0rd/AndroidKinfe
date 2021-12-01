

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal

class Stream(QObject):
    pipe = pyqtSignal(str)

    def write(self, text):
        self.pipe.emit(str(text))
        QApplication.processEvents()


def test(aaa):
    print(aaa)
    print(type(aaa))

if __name__ == '__main__':
    stream = Stream(pipe=test)
    # print(dir(stream.pipe))
    stream.write('123')