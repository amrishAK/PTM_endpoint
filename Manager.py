from threading import Timer
from Handler.eventHook import EventHook
from Services.Mqtt.MqttPublisher import MqttPublisher
from Models.Models import PedestrianCrossing
import datetime as dt
import json

class Manager(object):

    _serviceTrigger = EventHook()

    def __init__(self,signalDetails):
        self.SignalDetails = signalDetails
        self._maxPpl = 3
        self._currentCount = 0
        self._pedestrianTimer =  Timer(15,self.timerHit)
        self._mqtt = MqttPublisher(signalDetails['Id'],'TM/PedestrianRequest/'+ signalDetails['Id'])
    
    def resetManager(self):
        self._currentCount = 0
        self._pedestrianTimer.cancel()
        self._pedestrianTimer =  Timer(15,self.timerHit)

    def startManager(self):
        print("Timer is started")
        self._pedestrianTimer.start()
        pass
    
    def updatePedestrian(self,**kwargs):
        count = kwargs.get("count")

        if self._currentCount == 0 and count > 0:
            self._currentCount = count
            self.startManager()
            self._serviceTrigger.fire(count=count)
        else:    
            #-> if there is no pedistrians waiting
            if count == 0 and self._currentCount > 0:
                print("pedistrians count zero")
                self.resetManager()
            #-> if there is pedistrians count doesnt change
            elif self._currentCount == count:
                return
            #-> if there is pedistrians count decreses
            elif(self._currentCount > count):
                print("pedistrians count decreased")
                self._currentCount -= count
            #-> if there is pedistrians count increases    
            elif(self._currentCount < count):
                self._currentCount = count
                IncreasedCount = count - self._currentCount
                self._serviceTrigger.fire(count=IncreasedCount)

        if self._currentCount >= self._maxPpl:
            self.PublishMqtt('Counter')
            self.resetManager()
    
    def timerHit(self):
        #restart and trigger the traffic light
        print("Request signal change")
        self.PublishMqtt('Timer')
        self.resetManager()  

    def PublishMqtt(self,trigger):
        currentTimeStamp = dt.datetime.now()
        model = PedestrianCrossing(trigger=trigger,
                                pplCount=self._currentCount,
                                date=currentTimeStamp.strftime('%m/%d/%Y'),
                                time=str(currentTimeStamp.strftime('%I:%M:%S %p')),
                                signalId=self.SignalDetails['Id'],
                                signalLocation=self.SignalDetails['Location'])
        self._mqtt.Publish(json.dumps(model.getDict()))      
