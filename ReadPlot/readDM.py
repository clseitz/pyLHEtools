import sys
import ROOT as rt
import math
from LHEevent import *
from LHEfile import *
import plotTools
from array import array
import numpy as n
import os
if __name__ == '__main__':

    # find events in file
    finName = ""
    foutName = ""
    if len(sys.argv) == 2:                                                                                                                               
        finName = sys.argv[1]
        foutName = os.path.basename(finName).replace('.lhe','.root')
    elif len(sys.argv) == 3:
        finName = sys.argv[1]
        foutName = sys.argv[2]
    elif len(sys.argv) < 2:
        print "No input LHE file given"
        exit(0)
    
        
    myLHEfile = LHEfile(finName)
    myLHEfile.setMax(-1)

    eventsReadIn = myLHEfile.readEvents()

    #define tree
    t = rt.TTree( 'events', 'tree with events from LHE file' )
    nPart =  array('i',[50])
    np = 0

    PdgID = array('i',nPart[0]*[0])
    mIdx = array('i',nPart[0]*[0])
    E = array('f',nPart[0]*[0])
    Px = array('f',nPart[0]*[0])
    Py = array('f',nPart[0]*[0])
    Pz = array('f',nPart[0]*[0])
    Pt = array('f',nPart[0]*[0])

    M = array('f',nPart[0]*[0])
    Eta = array('f',nPart[0]*[0])
    Phi = array('f',nPart[0]*[0])

    t.Branch("nPart",nPart,"nPart/I")
    t.Branch("PdgID",PdgID,"PdgID[nPart]/I")
    t.Branch("mIdx",mIdx,"mIdx[nPart]/I")
    t.Branch("E",E,"E[nPart]/F")
    t.Branch("Px",Px,"Px[nPart]/F")
    t.Branch("Py",Py,"Py[nPart]/F")
    t.Branch("Pz",Pz,"Pz[nPart]/F")
    t.Branch("Pt",Pt,"Pt[nPart]/F")
    t.Branch("M",M,"M[nPart]/F")
    t.Branch("Eta",Eta,"Eta[nPart]/F")
    t.Branch("Phi",Phi,"Phi[nPart]/F")

    vect = rt.TLorentzVector(0,0,0,0)
    DM_1 = rt.TLorentzVector(0,0,0,0)
    DM_2 = rt.TLorentzVector(0,0,0,0)
    MED = rt.TLorentzVector(0,0,0,0)

    for oneEvent in eventsReadIn:

        myLHEevent = LHEevent()
        myLHEevent.fillEvent(oneEvent)
        w = myLHEevent.Weights
        nPart[0] = int(len(myLHEevent.Particles)+1)
        np = int(len(myLHEevent.Particles))
        for i,p  in enumerate(myLHEevent.Particles):

            PdgID[i] = p['PdgID']
            mIdx[i] = p['mIdx']
            E[i] = p['E']
            Px[i] = p['Px']
            Py[i] = p['Py']
            Pz[i] = p['Pz']
            vect.SetPxPyPzE(Px[i],Py[i],Pz[i],E[i])
            Pt[i] = vect.Pt()
            M[i] = vect.M()

            Eta[i] = -999
            Phi[i] = -999
            if vect.Pt() > 0:
                Eta[i] = vect.Eta()
                Phi[i] = vect.Phi()
                
            if PdgID[i] == 9100022: 
                DM_1.SetPxPyPzE(Px[i],Py[i],Pz[i],E[i])
#                print 'setting DM_1 ', DM_1
            if PdgID[i] == -9100022: 
                DM_2.SetPxPyPzE(Px[i],Py[i],Pz[i],E[i])
#                print 'setting DM_2 ', DM_2

        MED = DM_1 + DM_2
#        print 'setting MED Pt', MED.Pt()
        
        len(myLHEevent.Particles)
#        print len(myLHEevent.Particles)
        nExtra = len(myLHEevent.Particles)
        PdgID[nExtra] = 800
        E[nExtra] = MED.E()
        Px[nExtra] = MED.Px()
        Py[nExtra] = MED.Py()
        Pz[nExtra] = MED.Pz()
        Pt[nExtra] = MED.Pt()
        M[nExtra] = MED.M()
        Eta[nExtra] = -999
        Phi[nExtra] = -999
        if MED.Pt() > 0:
            Eta[nExtra] = MED.Eta()
            Phi[nExtra] = MED.Phi()
        t.Fill()

        del oneEvent, myLHEevent
    print "creating output root file", foutName
    fout =  rt.TFile(foutName,"RECREATE") 
    t.Write()
