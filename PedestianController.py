from Handler.eventHook import EventHook
from Manager import Manager
from faceDectctor import FaceDetector
from APIServices import DataService
from Handler.JsonHandler import JsonHandler
from trafficController import TrafficController
from Services.Mqtt.MqttSubscriber import MqttSubscriber
from TrafficSimulator import TrafficSimulator
import cv2 as cv2
model = "model.caffemodel"
prototxt = "prototxt.txt"


class Main(object):

    def connectHandler(self):
        self._faceDetecter._managerTrigger.addHandler(self._pedistanManager.updatePedestrian)
        self._pedistanManager._serviceTrigger.addHandler(self._dataService.pedestrianDataReceiver)

    def __init__(self):        
        jsonHandler = JsonHandler()
        detailsChar = jsonHandler.LoadJson('Characterstics/Details.json')
        self._dataService = DataService(detailsChar['SignalDetails'])
        self._pedistanManager = Manager(detailsChar['SignalDetails'])
        self._faceDetecter = FaceDetector(prototxt,model,0.5) 
        
        #-> Event handlers
        self.connectHandler()
        
        #-> Initialize pedistan Manager 
        result = self._faceDetecter.InitiVideoStreamer()
        if result:
            self._faceDetecter.runStreamer()
        else:
            print("Video Streamer Failed to Initiate")
    
        try:
            while(self._faceDetecter._stop == False):
                frame = self._faceDetecter.runStreamer()    
                cv2.imshow("Frame", frame)           
                cv2.waitKey(1) & 0xFF
        except KeyboardInterrupt:
            self._faceDetecter.stopStreamer()
            print("Program stoped by a KeyboardInterrupt")

if __name__ == "__main__":
    Main()