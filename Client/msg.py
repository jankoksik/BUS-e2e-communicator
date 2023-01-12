import datetime

class msg:
    def __init__(self, name):
        self.Name = name
        self.Msg = ""
        self.Date = datetime.datetime.now()
        self.Me = False
    

    def getName(self):
        return self.Name

    def getNameHTML(self):
        x = self.Name.split("#")
        return x[0]+"-"+x[1]
    
    def getMsg(self):
        return self.Msg

    def getMe(self):
        return self.Me
    
    def getDate(self):
        return self.Date.strftime("%d %b %Y %H:%M")


    def setName(self, Name:str):
        self.Name = Name
    
    def setMsg(self, Msg:str):
        self.Msg = Msg
    
    def setMe(self, Me:bool):
        self.Me = Me
    
    def setDate(self, Date:datetime ):
        self.Date = Date


    