# import ROOT in batch mode
import sys, os
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
from array import array
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
from math import *
# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

debug = False
#keep all the SM particles, except gluons/photons for now
GenToKeep = [1,2,3,4,5,6,11,12,13,14,15,16,17,18,23,24,9100022, 9100000]
if __name__ == '__main__': 

    finName = ""
    foutName = ""
    outfolder = "output"
    if len(sys.argv) == 2:                                                                                                                               
        finName = sys.argv[1]
        foutName = outfolder+ '/' + os.path.basename(finName).replace('.lhe','.root').replace("_Pythia8_","_Pythia8.chunk").replace("GEN","TREE") 
        print "using default folder", outfolder, "for output"
    elif len(sys.argv) == 3:
        finName = sys.argv[1]
        outfolder = sys.argv[2]
        foutName = outfolder+ '/' + os.path.basename(finName).replace('.lhe','.root').replace("_Pythia8_","_Pythia8.chunk").replace("GEN","TREE") 
        print "using folder", outfolder, "for output"
    elif len(sys.argv) < 2:
        print "No input file given"
        exit(0)


    try: os.stat(outfolder) 
    except: os.mkdir(outfolder)
    # open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
    events = Events(finName)

    handleGenParticles = Handle("std::vector<reco::GenParticle>")
    labelGenParticles = "genParticles"

    fout =  ROOT.TFile(foutName,"RECREATE") 
    t = ROOT.TTree( 'events', 'tree with events from GEN file' )
    nPart =  array('i',[60])
    np = 0
    PdgID = array('i',nPart[0]*[0])
    Status = array('i',nPart[0]*[0])
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
    t.Branch("Status",Status,"Status[nPart]/I")
    t.Branch("mIdx",mIdx,"mIdx[nPart]/I")
    t.Branch("E",E,"E[nPart]/F")
    t.Branch("Px",Px,"Px[nPart]/F")
    t.Branch("Py",Py,"Py[nPart]/F")
    t.Branch("Pz",Pz,"Pz[nPart]/F")
    t.Branch("Pt",Pt,"Pt[nPart]/F")
    t.Branch("M",M,"M[nPart]/F")
    t.Branch("Eta",Eta,"Eta[nPart]/F")
    t.Branch("Phi",Phi,"Phi[nPart]/F")
    
        


    for e,event in enumerate(events):
        vect = ROOT.TLorentzVector(0,0,0,0)
        DM_1 = ROOT.TLorentzVector(0,0,0,0)
        DM_2 = ROOT.TLorentzVector(0,0,0,0)
        MED = ROOT.TLorentzVector(0,0,0,0)
        if e == -1:
            break
        if e%500 == 0: print "Processing event", e
        event.getByLabel (labelGenParticles, handleGenParticles)
        GenParticles = handleGenParticles.product()
        np = int(len(GenParticles))
        i=-1
        for p in GenParticles:
            if debug:
                if abs(p.pdgId()) ==6: print p.pdgId() ,p.status(), p.pt() #p.mother().pdgId(), p.px(), p.py(), p.pz(), p.energy()
        
#            if p.status() > 22 and p.status() < 72:
            #keep the status 62 tops as well
            if (p.status() > 23 and p.status() < 62) or ((p.status() > 62 and p.status() < 72)): 
            #clean up pythia garbage from 
            #https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/PhysicsTools/PatAlgos/python/slimming/prunedGenParticles_cfi.py
                continue
            if abs(p.pdgId()) in GenToKeep and p.pt() > 5:
                i = i+1
                PdgID[i] = p.pdgId()
                Status[i] = p.status()
                mIdx[i] = 0
                E[i] = p.energy()
                Px[i] = p.px()
                Py[i] = p.py()
                Pz[i] = p.pz()
                vect.SetPxPyPzE(Px[i],Py[i],Pz[i],E[i])
                Pt[i] = vect.Pt()
                M[i] = vect.M()
                if debug: print p.pdgId() ,p.status(), p.mother().pdgId(), p.px(), p.py(), p.pz(), p.energy()
                Eta[i] = -999
                Phi[i] = -999
                if vect.Pt() > 0:
                    Eta[i] = vect.Eta()
                    Phi[i] = vect.Phi()
                
                if PdgID[i] == 9100022 and p.status() == 1: 
                    DM_1.SetPxPyPzE(Px[i],Py[i],Pz[i],E[i])
                    if debug: print 'setting DM_1 ', DM_1.Px(),DM_1.Py(),DM_1.Pz(),DM_1.Energy()
                if PdgID[i] == -9100022 and p.status() == 1: 
                    DM_2.SetPxPyPzE(Px[i],Py[i],Pz[i],E[i])
                    if debug: print 'setting DM_2 ', DM_2.Px(),DM_2.Py(),DM_2.Pz(),DM_2.Energy()    

        MED = DM_1 + DM_2
        
        nExtra = min(i,51)
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
        #clean stuff, not very cleverly done
        for n in range(0,len(PdgID)):
            PdgID[n] = 0
            Status[n] = 0
            E[n] = 0
            Px[n] = 0
            Py[n] = 0
            Pz[n] = 0
            Pt[n] = 0
            M[n] = 0
            Eta[n] = 0
            Phi[n] = 0
            
    fout.cd()
    t.Write()
