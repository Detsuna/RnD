import datetime

class UTC(datetime.tzinfo) : 
    delta = datetime.timedelta()
    def utcoffset(self, dt) : 
        return UTC.delta
    def dst(self, dt) : 
        return UTC.delta
    def tzname(self, dt) : 
        return UTC.__name__

class Local(datetime.tzinfo) : 
    delta = datetime.datetime.now() - datetime.datetime.utcnow()
    def utcoffset(self, dt) : 
        return Local.delta
    def dst(self, dt) : 
        return Local.delta
    def tzname(self, dt) : 
        return Local.__name__