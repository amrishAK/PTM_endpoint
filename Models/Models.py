
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
        return data


class SignalSwitchDetail (object):
    State = None
    Date = None
    Time = None
    SignalId = None
    SignalLocation = None

    def __init__(self,**kwargs):
        self.State = kwargs.get("state")
        self.Date = kwargs.get("date")
        self.Time = kwargs.get("time")
        self.SignalId = kwargs.get("signalId")
        self.SignalLocation = kwargs.get("signalLocation")

    def getDict(self):
        data = {'state' : self.State,
                'date' : self.Date,
                'time' : self.Time,
                'signalId' : self.SignalId,
                'SignalLocation' : self.SignalLocation}
        return data

class PedestrianCrossing (object):
    Trigger = None
    PplCount = None
    Date = None
    Time = None
    SignalId = None
    SignalLocation = None

    def __init__(self,**kwargs):
        self.Trigger = kwargs.get('trigger')
        self.PplCount = kwargs.get('pplCount')
        self.Date = kwargs.get("date")
        self.Time = kwargs.get("time")
        self.SignalId = kwargs.get("signalId")
        self.SignalLocation = kwargs.get("signalLocation")

    def getDict(self):
        data = {'trigger' : self.Trigger,
                'pplCount' : self.PplCount,
                'date' : self.Date,
                'time' : self.Time,
                'signalId' : self.SignalId,
                'SignalLocation' : self.SignalLocation}
        return data

class TrafficDensity (object):
    Density = None
    Label = None
    Date = None
    Time = None
    SignalId = None
    SignalLocation = None

    def __init__(self,**kwargs):
        self.Density = kwargs.get('density')
        self.Label = kwargs.get('label')
        self.Date = kwargs.get("date")
        self.Time = kwargs.get("time")
        self.SignalId = kwargs.get("signalId")
        self.SignalLocation = kwargs.get("signalLocation")

    def getDict(self):
        data = {'density' : self.Density,
                'label': self.Label,
                'date' : self.Date,
                'time' : self.Time,
                'signalId' : self.SignalId,
                'SignalLocation' : self.SignalLocation}
        return data
    