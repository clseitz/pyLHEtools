import ROOT as rt

class LHEfile():
    
    def __init__(self, fileINname):
        self.eventList = []
        self.fileINname = fileINname
        self.MaxEv = -99

    def setMax(self, maxVal):
        self.Max = maxVal
        
    def readEvents(self):
        xfile = open(self.fileINname,"r")
        
        newEVENT = False
        oneEvent = []
        lines = xfile.readlines()                                                                                  
        print 'Found %i lines in %s' %(len(lines),self.fileINname)                                                                  
        for line in lines:                                                                                                              

            if line[0] == '#': continue                                                                                                
            if newEVENT: oneEvent.append(line)

            if line.find("</event>") != -1:
                newEVENT = False
                self.eventList.append(oneEvent)
                oneEvent = []
                if len(self.eventList) >= self.Max and self.Max>0: break
            if line.find("<event") != -1:
                newEVENT = True
                oneEvent.append(line)

        return self.eventList
