import datetime

class chat:
    def __init__(self, name):
        self.Active = False
        self.Name = name
        self.LastMsg = ""
        self.LastMsgDate = datetime.datetime.now()
        self.NewMsgCount = 0
    
    def getActive(self):
        return self.Active

    def getName(self):
        return self.Name
    
    def getLastMsg(self):
        return self.LastMsg
    
    def getLastMsgDate(self):
        return self.LastMsgDate.strftime("%d %b %Y %H:%M")

    def getNewMsgCount(self):
        return self.NewMsgCount

    def setActive(self, Active:bool):
        self.Active = Active

    def setName(self, Name:str):
        self.Name = Name
    
    def setLastMsg(self, LastMsg:str):
        self.LastMsg = LastMsg
    
    def setLastMsgDate(self, LastMsgDate:datetime ):
        self.LastMsgDate = LastMsgDate

    def setNewMsgCount(self, NewMsgCount:int ):
         self.NewMsgCount = NewMsgCount

    