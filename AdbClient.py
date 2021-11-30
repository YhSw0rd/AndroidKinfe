import socket
from threading import Thread


class AdbClient(object):
    default_encoding = 'utf-8'
    def __init__(self,host:str = None ,port:int = None, hook = None,) -> None:
        super().__init__()
        self.__host = host or '127.0.0.1'
        self.__port = port or 5037
        self.__adb_client = None
        self.__hook = hook
        
        
    
    # message we sent to server contains 2 parts
    # 1. length
    # 2. content
    # @classmethod
    def __encode_data(self,data):
        byte_data = data.encode(self.default_encoding)
        byte_length = "{0:04X}".format(len(byte_data)).encode(self.default_encoding)
        # looks like
        # b'000Chost:devices'
        return byte_length + byte_data

    def __send(self,cmd,isShell=False):
        if self.__adb_client == None:
            self.__adb_client = socket.socket()
            self.__adb_client.connect((self.__host, self.__port))
            self.__adb_client_recv_thread = Thread(target=self.__read,)
            self.__adb_client_recv_thread.start()
        ready_data = None
        if isShell:
            ready_data = cmd.encode(self.default_encoding)
        else:
            ready_data = self.__encode_data(cmd)
        self.__adb_client.send(ready_data)
        return self



    def __read(self):
        try:
            while True:
                buf = self.__adb_client.recv(1024)
                if self.__hook:
                    self.__hook(buf.decode(self.default_encoding))
        except Exception as e:
            print(e)

    def __close(self):
        if self.__adb_client != None:
            try:
                self.__adb_client.close()
                self.__adb_client = None
            except Exception as e:
                print(e)

    def close(self):
        self.__close()

    # 执行命令，异步接收
    def execCmd(self,cmd:str,ifClose:bool = True,isShell = False) -> None:
        self.__send(cmd+ ('\n' if isShell else ''),isShell)
        if ifClose:
            self.__close()


if __name__ == '__main__':
    adbclient = AdbClient()
    # adbclient._recv()
    # adbclient.send("host:transport-any")
    # print(adbclient.adb_client.recv(1024))
    # print(adbclient.send("shell:dumpsys activity activities").recv())
    # time.sleep(2)
    # adbclient.send("host:transport-any")
    # adbclient.send("shell:dumpsys activity activities")
    # print(adbclient.adb_client.recv(1024))
    # adbclient.close()
    # print(adbclient.execCmdRecvMore(["host:transport-any","shell:dumpsys activity activities"]))
    # print(adbclient.comboCmd(["host:devices"]))
    print(adbclient.execCmdRecvOnce("host:transport-any",ifClose=False))
    print(adbclient.execCmdRecvMore("shell:dumpsys activity activities"))