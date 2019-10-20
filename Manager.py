from threading import Timer
from Handler.eventHook import EventHook

class Manager(object):

    _serviceTrigger = EventHook()

    def __init__(self):
        self._maxPpl = 8
        self._currentCount = 0
        self._pedestrianTimer =  Timer(60,self.timerHit)
    
    def resetManager(self):
        self._currentCount = 0
        self._timer = 0

    def startManager(self):
        self._pedestrianTimer.start()
        pass
    
    def updatePedestrian(self,**kwargs):
        count = kwargs.get("count")
        self._serviceTrigger.fire(count=count)
        if self._currentCount == 0:
            self._currentCount = 1
            self.startManager()
            self._serviceTrigger.fire(count=count)
        elif self._currentCount == count:
            return
        elif(self._currentCount > count):
            self._currentCount -= count
        elif(self._currentCount < count):
            count = count - self._currentCount
            self._currentCount = count
            self._serviceTrigger.fire(count=count)

        if self._currentCount >= self._maxPpl:
            #restart and trigger the traffic light
            self.resetManager()
    
    def timerHit(self):
        #restart and trigger the traffic light
        print("Request signal change")
        self.resetManager()        
