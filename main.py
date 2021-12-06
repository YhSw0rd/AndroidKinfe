import sys
from threading import Thread
from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor
from FridaClient import FridaClient
from whenconnect import when_connect,when_disconnect
import ConnectionTracer
from AndroidReverse import  Ui_AndroidReversePanel
from AdbClient import AdbClient
from Stream import Stream
import time

from PyQt5.QtWebChannel import QWebChannel



class MainWindow(QtWidgets.QMainWindow, Ui_AndroidReversePanel):
    updateAppInfoTextSignal = pyqtSignal(str)
    isShellMode = False

    fridaClient = None
    def __init__(self,parent=None) -> None:
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.startGetDevices()
        # 设置tab的console
        self.AndroidTab.setConsole(self.AppInfoText)
        self.FridaTab.setConsole(self.FridaConsole)
        # 设置文本更新槽
        self.updateAppInfoTextSignal[str].connect(self.on_updateAppInfoTextSignal)
        # 如果有接收就更新到文本编辑框
        self.adbClient = AdbClient(hook=lambda x : self.updateAppInfoTextSignal.emit(x))

        # 更改标准输出到文本编辑框
        sys.stdout = Stream(pipe=self.on_updateAppInfoTextSignal)
        # 打开本地frida编辑页面，这个用monaco editor实现的，设置qwebchannel来接收页面加载完成信息，加载完成后读取fridagum.ts文件发送给页面，增加提示
        self.FridaEditPage.load( QtCore.QUrl( QtCore.QFileInfo("./fridapage/index.html").absoluteFilePath() ))
        
        self.webchannel = QWebChannel()
        self.webchannel.registerObject('conmunicateChannel',self)
        self.FridaEditPage.page().setWebChannel(self.webchannel)

    
    
    # 开始监听设备连接
    def startGetDevices(self):
        when_connect(device='any',do=self.deviceConnectEvent)
        when_disconnect(device='any',do=self.deviceDisconnectEvent)

    # 关闭监听设备连接
    def stopGetDevices(self):
        ConnectionTracer.stop()

    # 连接事件
    def deviceConnectEvent(self,device):
        self.DeviceList.addItem(device)
    
    # 断开事件
    def deviceDisconnectEvent(self,device):
        self.exit_device()
        index = self.DeviceList.findText(device)
        self.DeviceList.removeItem(index)
        self.DeviceList.setCurrentText(None)
        self.DeviceList.setCurrentIndex(-1)
        self.DeviceList.update()

    @QtCore.pyqtSlot()
    def on_StartDDMS_triggered(self):
        # 启动DDMS
        print('on_StartDDMS_triggered')

    @QtCore.pyqtSlot()
    def on_SettingDDMS_triggered(self):
        # 配置DDMS路径
        print('on_SettingDDMS_triggered')

        
    @QtCore.pyqtSlot()
    def on_StartIDA_triggered(self):
        # 启动IDA
        print('on_StartIDA_triggered')

    @QtCore.pyqtSlot()
    def on_StartIDAServer_triggered(self):
        # 启动IDA服务，手机里的服务
        print('on_StartIDAServer_triggered')

    @QtCore.pyqtSlot()
    def on_SettingIDAPath_triggered(self):
        # 配置IDA路径
        print('on_SettingIDAPath_triggered')

    @QtCore.pyqtSlot()
    def on_SettingIDAServer_triggered(self):
        # 启动IDA服务，手机里的服务
        print('on_SettingIDAServer_triggered')



    @QtCore.pyqtSlot()
    def on_StartFridaServer_triggered(self):
        # 启动fridaserver
        print('on_StartFridaServer_triggered')

    @QtCore.pyqtSlot()
    def on_SettingFridaScript_triggered(self):
        # 配置运行脚本
        print('on_SettingFridaScript_triggered')

    @QtCore.pyqtSlot(str)
    def on_DeviceList_currentTextChanged(self,device):
        # 如果是shell模式请先断开
        self.exit_device()
        if device:
            # 选择设备，这个得起个线程去监听
            self.AppInfoText.append('选择设备:'+device)
            self.isShellMode = True
            self.adbClient.execCmd("host:transport:"+self.DeviceList.currentText(),ifClose=False)
            time.sleep(.1)
            self.adbClient.execCmd("shell:",ifClose=False)


    @QtCore.pyqtSlot()
    def on_GetAppInfo_clicked(self):
        if self.DeviceList.currentText():
            self.adbClient.execCmd("dumpsys activity activities",ifClose=False,isShell=True)
        else:
            self.AppInfoText.append('请选择设备')
        
    @QtCore.pyqtSlot()
    def on_StartDebug_clicked(self):
        if self.ActivityInput.text():
            self.adbClient.execCmd("am start -D -n "+self.ActivityInput.text(),ifClose=False,isShell=True)
        else:
            self.AppInfoText.append('请输入要调试的页面')

    @QtCore.pyqtSlot()
    def on_AdbForward_clicked(self):
        if self.DeviceList.currentText() and self.LocalPort.text() and self.RemotePort.text():
            adbClient = AdbClient(hook=lambda x : self.updateAppInfoTextSignal.emit(x))
            adbClient.execCmd("host:transport:"+self.DeviceList.currentText(),ifClose=False)
            adbClient.execCmd("host:forward:tcp:%s;tcp:%s"%(self.LocalPort.text(),self.RemotePort.text()),ifClose=False)
            def recvThenClose():
                time.sleep(5)
                adbClient.close()
            Thread(target=recvThenClose).start()
        else:
            self.AppInfoText.append('请连接手机并填写本地端口和手机端口')

    
    @QtCore.pyqtSlot()
    def on_AppInfoText_listforward(self):
        adbClient = AdbClient(hook=lambda x : self.updateAppInfoTextSignal.emit(x))
        adbClient.execCmd("host:list-forward",ifClose=False)
        def recvThenClose():
            time.sleep(3)
            adbClient.close()
        Thread(target=recvThenClose).start()

    

    @QtCore.pyqtSlot()
    def on_CommandInput_returnPressed(self):
        if self.CommandInput.text() and self.isShellMode:
            self.adbClient.execCmd(self.CommandInput.text(),ifClose=False,isShell=True)
        else:
            self.AppInfoText.append("输入内容为空或者没选设备")
        if self.CommandInput.text() == 'exit':
            self.exit_device()
            self.DeviceList.setCurrentIndex(-1)
            self.DeviceList.setCurrentText(None)
            self.DeviceList.update()
        self.CommandInput.setText("")
    
    # firda页面点击启动按钮获取编辑器里的js文本
    @QtCore.pyqtSlot()
    def on_FridaStart_clicked(self):
        # 开始和调试按钮失效
        self.FridaStart.setDisabled(True)
        self.FridaDebug.setDisabled(True)
        # 获取文本，执行frida
        self.fridaClient = FridaClient().setDevice(self.DeviceList.currentText()).runApp('',self.FridaPackageName.text())
        self.FridaEditPage.page().runJavaScript('getEditorContent();',lambda js_code: self.fridaClient.loadScript(js_code).exec())

    

    # frida页面点击调试按钮
    @QtCore.pyqtSlot()
    def on_FridaDebug_clicked(self):
        # 开始和调试按钮失效
        self.FridaStart.setDisabled(True)
        self.FridaDebug.setDisabled(True)
        # 获取文本，调试frida
        self.fridaClient = FridaClient().setDevice(self.DeviceList.currentText()).runApp('',self.FridaPackageName.text())
        self.FridaEditPage.page().runJavaScript('getEditorContent();',lambda js_code: self.fridaClient.loadScript(js_code).exec())

    # frida页面点击停止按钮
    @QtCore.pyqtSlot()
    def on_FridaStop_clicked(self):
        # 开始和调试按钮有效
        self.FridaStart.setDisabled(False)
        self.FridaDebug.setDisabled(False)
        # 停止frida

    

    # frida页面加载完成，添加提示frida提示
    @QtCore.pyqtSlot()
    def onFridaPageLoaded(self):
        firdaGumTsFile = open('./fridapage/node_modules/@types/frida-gum/frida-gum.ts','r',encoding="UTF-8")
        self.FridaEditPage.page().runJavaScript('addProgramTip(`%s`);'%(''.join(firdaGumTsFile.readlines()))) 









    def on_updateAppInfoTextSignal(self,text:str):
        if text:
            self.PanelTabs.currentWidget().getConsole().append(text)

    def exit_device(self):
        if self.isShellMode:
            self.adbClient.execCmd("exit",isShell=True)
            self.adbClient.close()
            self.isShellMode = False

    # 关闭主窗体后的事件
    def closeEvent(self,event):
        sys.stdout = sys.__stdout__
        self.stopGetDevices()
        self.adbClient.close()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    