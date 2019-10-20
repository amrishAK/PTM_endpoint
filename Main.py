from Handler.eventHook import EventHook
from Manager import Manager
from faceDectctor import FaceDetector
from APIServices import DataService
import cv2
model = "model.caffemodel"
prototxt = "prototxt.txt"

class Main(object):

    _pedistanManager = Manager()
    _faceDetecter = FaceDetector(prototxt,model,0.5)
    _dataService = DataService()

    def connectHandler(self):
        self._faceDetecter._managerTrigger.addHandler(self._pedistanManager.updatePedestrian)
        self._pedistanManager._serviceTrigger.addHandler(self._dataService.dataReceiver)

    def __init__(self):
        
        try:
            self.connectHandler()
            result = self._faceDetecter.InitiVideoStreamer()
            if result:
                self._faceDetecter.runStreamer()
            else:
                print("Video Streamer Failed to Initiate")
            
            while(True):
                
                frame = self._faceDetecter.runStreamer()
                
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord("c"):
                    break

        except KeyboardInterrupt:
            self._faceDetecter.stopStreamer()
            print("Program stoped by a KeyboardInterrupt")

if __name__ == "__main__":
    Main().__init__()