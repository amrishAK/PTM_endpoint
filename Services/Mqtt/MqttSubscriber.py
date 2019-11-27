import paho.mqtt.client as mqtt
import socket
from Handler.eventHook import EventHook 

# This is the Subscriber
class MqttSubscriber (object):

    host = '34.244.190.178'
    port = 1883
    _otherDensityHandler = EventHook()

    def __init__(self,id_= ""):
        self.OwnId = id_
        self._clientId = id_
        self._client = mqtt.Client()
        self._client.connect(self.host,1883,60)

        self._client.on_connect = self.on_connect
        
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("#")

        
if __name__ == "__main__":
    MqttSubscriber("SIG123455")