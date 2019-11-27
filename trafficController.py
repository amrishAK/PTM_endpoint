from Handler.eventHook import EventHook
from Handler.JsonHandler import JsonHandler
from APIServices import DataService
from threading import Timer
from Services.Mqtt.MqttPublisher import MqttPublisher
from Services.Mqtt.MqttSubscriber import MqttSubscriber
from TrafficSimulator import TrafficSimulator
from Models.Models import TrafficDensity
import json
import statistics
from PIL import Image, ImageOps
import datetime as dt

class TrafficController (MqttSubscriber) :

    _signalSwitchEvent = EventHook()

    def __init__(self):
        jsonHandler = JsonHandler()
        detailsChar = jsonHandler.LoadJson('Characterstics/Details.json')
        self.char = detailsChar
        self._signalId = detailsChar['SignalDetails']['Id']
        self.otherSignals = detailsChar['otherSignals']
        self._gTime = detailsChar['Timer']['Green']  
        self._rTime = detailsChar['Timer']['Red']
        self._yTimer = 10
        self._currentSignal = 'g'
        self._mqtt = MqttPublisher(detailsChar['SignalDetails']['Id'],'TM/FusedTrafficDensity/'+ self.char['SignalDetails']['Id'])
        #self._subscriber = MqttSubscriber(detailsChar['SignalDetails']['Id'])
        self._dataService = DataService(detailsChar['SignalDetails'])
        self.connectHandler()
        self._timer = Timer(self._gTime,self.TimerHit)
        self._timer.start()
        self._pedestrianRequest = False
        super().__init__(self._signalId)
        self._client.on_message = self.on_message
        self._client.loop_forever()


    def connectHandler(self):
        self._signalSwitchEvent.addHandler(self._dataService.signalSwitchDataReceiver)

    def TimerHit(self,**kwarg):
        self._timer.cancel()
        if self._currentSignal == 'g' : 
            self._currentSignal = 'y'
            print("Yellow--->>>",self._yTimer)
            self._timer = Timer(self._yTimer,self.TimerHit)
        elif self._currentSignal == 'y':
            self._currentSignal = 'r'
            time = (self._rTime + 20) if self._pedestrianRequest else self._rTime
            print("Red--->>>",time)
            self._timer = Timer(time,self.TimerHit)
            if self._pedestrianRequest:
                self._pedestrianRequest = False
        else:
            self._currentSignal = 'g'
            print("Green--->>>",self._gTime)
            self._timer = Timer(self._gTime,self.TimerHit)
        
        image = Image.open(self._currentSignal+'.jpg')
        #image.show()
        
        self._timer.start()
        self._signalSwitchEvent.fire(currentSignal=self._currentSignal)

    def UpdateSignalTime(self,gTime,rTime):
        self._gTime = gTime  
        self._rTime = rTime
    
    def on_message(self,client, userdata, msg):
        
        topicArray = str(msg.topic).split('/')
        signalId=topicArray[2]
        print(topicArray[1])
        
        if topicArray[1] == 'TrafficDensity':
            data= json.loads(msg.payload.decode())
            print(data)
            if signalId == self._signalId:
                self._signalDensity = data['density']
            try:
                self.otherSignals[signalId]['CurrentDensity'] = (data['density'] * self.otherSignals[signalId]['possibleTraffic'])/100
            except Exception as ex:
                print("catch",ex)
                pass
            self.FuseDensity()
        else:
            if signalId == self._signalId:
                self._pedestrianRequest = True
        
    def FuseDensity(self):
        
        DensityArray = []
        for _,val in self.otherSignals.items():
            DensityArray.append(val['CurrentDensity'])
        
        fusedDensity = statistics.mean(DensityArray)
        # fusedDensity = statistics.mean([fusedDensity,self._signalDensity])
        print("in fuse",fusedDensity)
        self.FussionAlgorithm(fusedDensity)
        
    def FussionAlgorithm(self,fusedDensity):
        
        currentTimeStamp = dt.datetime.now()
        model = TrafficDensity(density=fusedDensity,
                                label='',
                                date=currentTimeStamp.strftime('%m/%d/%Y'),
                                time=str(currentTimeStamp.strftime('%I:%M:%S %p')),
                                signalId=self.char['SignalDetails']['Id'],
                                signalLocation=self.char['SignalDetails']['Location'])
        self._mqtt.Publish(json.dumps(model.getDict()))
        print("Fused",fusedDensity)

        if fusedDensity < 28.3 :
            green = 5
            red = 5
        elif fusedDensity < 56.6:
            green = 9
            red = 6
        elif fusedDensity < 84.9:
            green = 12
            red = 8
        else:
            pass

        self.UpdateSignalTime(green,red)

if __name__ == "__main__":
    TrafficController()