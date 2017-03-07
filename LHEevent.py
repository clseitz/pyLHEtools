import ROOT as rt

                     
class LHEevent():
    
    def __init__(self):
        self.Particles = []
        self.Weights = []
        self.Model = "none"
    def fillEvent(self, lheLines):
        # check that this is a good event
        if lheLines[0].find("<event") == -1 or lheLines[-1].find("</event>") == -1:
            print "THIS IS NOT A LHE EVENT"
            return 0
        # read the model
        for i in range(2,len(lheLines)-3):
            if "wgt" in lheLines[i]:
                self.Weights.append(self.readWeights(lheLines[i]))
            else:
                self.Particles.append(self.readParticle(lheLines[i]))
        return 1

    def readParticle(self, lheLine):
        dataIN = lheLine[:-1].split(" ")
        dataINgood = []
        for entry in dataIN:
            if entry != "": dataINgood.append(entry)
        
        if len(dataINgood) > 10:
            return {'ID': int(dataINgood[0]),
                    'mIdx': int(dataINgood[2])-1,
                    'Px' : float(dataINgood[6]),
                    'Py' : float(dataINgood[7]),
                    'Pz' : float(dataINgood[8]),
                    'E' : float(dataINgood[9]),
                    'M' : float(dataINgood[10])}

    def readWeights(self, lheLine):
        dataIN = lheLine[:-1].split(" ")
        dataINgood = []
        for entry in dataIN:
            if entry != "": dataINgood.append(entry)
        if len(dataINgood) > 3:
            return {'WeightID': dataINgood[1][dataINgood[1].find("='")+2:dataINgood[1].find("'>")],
                    'Weight' :  float(dataINgood[2])}
            
