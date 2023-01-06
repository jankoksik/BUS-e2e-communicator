import datetime

class token:
    def __init__(self, enc, sec):
        self.enc = enc
        self.sec = sec
        date_1 = datetime.datetime.now()
        self.ExpDate = date_1 + datetime.timedelta(minutes=5)
    
    #return true if token has expired
    def isExpired(self):
        if datetime.datetime.now() > self.ExpDate:
            return True
        else :
            return False

    def getEnc(self):
        return self.enc
    
    def getSec(self):
        return self.sec