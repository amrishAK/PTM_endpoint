import datetime as dt
from Handler.eventHook import EventHook
from Models.Models import pedestrianDetail
from Models.Models import SignalSwitchDetail
from Services.REST.RESTservice import httpService

class DataService(object):

    http = httpService()

    def __init__(self,signalDetails):
        self._id = signalDetails['Id']
        self._location = signalDetails['Location']
        print(signalDetails)

    def pedestrianDataReceiver(self,**kwargs):
        currentTimeStamp = dt.datetime.now()
        for _ in range(0,kwargs.get("count",0)):
            model = pedestrianDetail(date=currentTimeStamp.strftime('%m/%d/%Y'),
                                time=str(currentTimeStamp.strftime('%I:%M:%S %p')),
                                signalId=self._id,
                                signalLocation=self._location)
            self.http.post("traffic/pedestrianDetail",model.getDict())

    def signalSwitchDataReceiver(self,**kwargs):
        print("HH")
        currentTimeStamp = dt.datetime.now()
        model = SignalSwitchDetail(state=kwargs.get("currentSignal"),
                                date=currentTimeStamp.strftime('%m/%d/%Y'),
                                time=str(currentTimeStamp.strftime('%I:%M:%S %p')),
                                signalId=self._id,
                                signalLocation=self._location)
        self.http.post("traffic/signalSwitch",model.getDict())
            



