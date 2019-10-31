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
        self._pedestrianTimer.cancel()
        self._pedestrianTimer =  Timer(60,self.timerHit)

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
            #restart and trigger the traffic light
            self.resetManager()
    
    def timerHit(self):
        #restart and trigger the traffic light
        print("Request signal change")
        self.resetManager()        
