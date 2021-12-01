

import frida
import sys
from Stream import Stream
import time
js = '''
    setTimeout(function(){
        Java.perform(function (){
           console.log("Hello world111");
        }); 

    },0)

'''


# def on_message(message, data):
#     if message['type'] == 'send':
#         print(message['payload'])
#     elif message['type'] == 'error':
#         print(message['stack'])

def test(aaa):
    f_handler=open('out.log', 'w')
    f_handler.write(aaa)
    f_handler.close()




try:
    sys.stdout = Stream(pipe=test)
except Exception as e:
    pass
session = frida.get_usb_device().attach("com.example.fridatestexample")
script = session.create_script(js)
script.load()
time.sleep(5)
sys.stdout = sys.__stdout__
session.detach()