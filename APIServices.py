import datetime as dt
from Handler.eventHook import EventHook
from Models.Models import pedestrianDetail

class DataService(object):
    
    def dataReceiver(self,**kwargs):
        currentTimeStamp = dt.datetime.now()
        for i in range(0,kwargs.get("count",0)):
            model = pedestrianDetail(date=currentTimeStamp.strftime('%m/%d/%Y'),
                                time=str(currentTimeStamp.strftime('%I:%M:%S %p')),
                                signalId=kwargs.get("signalId"),
                                signalLocation=kwargs.get("signalLocation"))
            print(model.getDict())



