import argparse
import random
from threading import Timer
from Handler.JsonHandler import JsonHandler
from Services.Mqtt.MqttPublisher import MqttPublisher
from Models.Models import TrafficDensity
import json
import datetime as dt

class TrafficSimulator(object):

    def __init__(self,fileName,enableTimer = True):
        jHandler = JsonHandler()
        self.char = jHandler.LoadJson("Characterstics/"+ fileName)
        self._mqtt = MqttPublisher(self.char['SignalDetails']['Id'],'TM/TrafficDensity/'+ self.char['SignalDetails']['Id'])
        self._timer = Timer(10,self.TimerHit)
        self._timer.start()

    def TimerHit(self):
        data = self.SimulateTraffic()
        self._mqtt.Publish(json.dumps(data))
        self._timer = Timer(10,self.TimerHit)
        self._timer.start()

    def SimulateTraffic(self):
        val = random.randint(0,1000)
        val = val/1000.0 * 100
        
        if val < 33.3 :
            traffic = 'l'
        elif val < 66.6:
            traffic = 'm'
        else:
            traffic = 'h' 
        currentTimeStamp = dt.datetime.now()
        model = TrafficDensity(density=val,
                                label=traffic,
                                date=currentTimeStamp.strftime('%m/%d/%Y'),
                                time=str(currentTimeStamp.strftime('%I:%M:%S %p')),
                                signalId=self.char['SignalDetails']['Id'],
                                signalLocation=self.char['SignalDetails']['Location'])

        return model.getDict()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--charFile', help='name of the charfile', type=str)
    args = parser.parse_args()
    TrafficSimulator(args.charFile)
