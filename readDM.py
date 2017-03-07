import sys
import ROOT as rt
import math
from LHEevent import *
from LHEfile import *
import plotTools
from array import array
import numpy as n
if __name__ == '__main__':

    # find events in file
    myLHEfile = LHEfile(sys.argv[1])
    myLHEfile.setMax(10000)

    eventsReadIn = myLHEfile.readEvents()

    t = rt.TTree( 'events', 'tree with events from LHE file' )
    nPart =  array('i',[50])
    np = 0
    ID = array('f',nPart[0]*[0])
    t.Branch("nPart",nPart,"nPart/I")
    t.Branch("ID",ID,"ID[np]/F")
#    t.Branch("E",E,"E[nPart]/F")
#    t.Branch("Px",Px,"Px[nPart]/F")
#    t.Branch("Py",Py,"Py[nPart]/F")
#    t.Branch("Pz",Pz,"Pz[nPart]/F")

#    tree.Branch( 'staff', staff, '' )
    for oneEvent in eventsReadIn:

        myLHEevent = LHEevent()
        myLHEevent.fillEvent(oneEvent)
        w = myLHEevent.Weights
        nPart[0] = int(len(myLHEevent.Particles))
        np = int(len(myLHEevent.Particles))
        print nPart
        for i,p  in enumerate(myLHEevent.Particles):
            ID[i] = p['ID']
        print ID
        t.Fill()


            

        del oneEvent, myLHEevent
    fout =  rt.TFile(sys.argv[2],"RECREATE") 
    t.Write()
