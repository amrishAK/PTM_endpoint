from imutils.video import videostream
import numpy
import cv2
import imutils
import time
from Handler.eventHook import EventHook


class FaceDetector(object):

    _managerTrigger = EventHook() 
    
    def __init__ (self,protoTxt,model,confidence):
        self._stop = False
        self._cofidence = confidence
        self._net = cv2.dnn.readNetFromCaffe(protoTxt,model)

    def InitiVideoStreamer(self):
        #initilise the video streamer
        self._streamer = videostream.VideoStream().start()
        time.sleep(2.0)
        return True

    def runStreamer(self):
        
        frame = self._streamer.read()
        frame = imutils.resize(frame, width=400)
    
        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
    
        # pass the blob through the network and obtain the detections and
        # predictions
        self._net.setInput(blob)
        detections = self._net.forward()

        if len(detections) > 0:
            self._managerTrigger.fire(count=len(detections))

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < 0.4:
                continue

            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * numpy.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
    
            # draw the bounding box of the face along with the associated
            # probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv2.putText(frame, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        return frame
            

    def stopStreamer(self):
        print("In stop")
        self._stop = False
        cv2.destroyAllWindows()
        self._streamer.stop()







