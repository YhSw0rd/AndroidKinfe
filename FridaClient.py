


import frida


class FridaClient:
    # 连接的设备
    device = None
    # frida连接设备后打开程序创建的会话
    session = None
    # 加载的脚本
    script = None



    def setDevice(self,device_name):
        self.device = frida.get_device(device_name)
        return self

    def runApp(self,runAppWay,app_name):
        func = getattr(self,runAppWay)
        return func(app_name)

    def attach(self,app_name):
        self.session = self.device.attach(app_name)
        return self
    
    def spawn(self,app_name):
        pid = self.device.spawn(app_name)
        self.session = self.device.attach(pid)
        self.device.resume(pid)
        return self

    def loadScript(self,js_code):
        self.script = self.session.create_script(js_code)
        return self
    
    def exec(self):
        self.script.load()
        return self

    def exitApp(self):
        self.session.detach()
