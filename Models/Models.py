
class pedestrianDetail (object):
    
    Date = None
    Time = None
    SignalId = None
    SignalLocation = None

    def __init__(self,**kwargs):
        self.Date = kwargs.get("date")
        self.Time = kwargs.get("time")
        self.SignalId = kwargs.get("signalId")
        self.SignalLocation = kwargs.get("signalLocation")

    def getDict(self):
        data = {'date' : self.Date,
                'time' : self.Time,
                'signalId' : self.SignalId,
                'SignalLocation' : self.SignalLocation}
        return {'pedestrianDetail':data}