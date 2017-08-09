#! /usr/bin/env python
#THIS NEEDS CMSSW8 or higher

import sys, os, glob
import csv

#cmsswR =  os.environ.get('CMSSW_BASE')
#cmsswR = cmsswR[cmsswR.find('CMSSW')+6:].split('_')[0]
#if int(cmsswR) < 8:
#    print "ATTENTION: To run this script setup CMSSW8 or higher (needs higher python version with pandas)"
#    exit(0)


import pandas as pd
import numpy as np
from ROOT import *
import matplotlib.pyplot as plt
plt.style.use('ggplot')
gROOT.SetBatch(True)
gStyle.SetPaintTextFormat("4.3f")
gStyle.SetOptStat(0)

def readLogFiles(inputFolder, m):
    files = dirList = glob.glob(inputFolder+"/*")
    samplesList = []
    for fin in files:
        sampleList = []
        with open(fin) as f:
            for line in f:
                model, xsec = "model", "xsec"
                if "Running input file" in line:
                    print line
                    model = line[line.find("Mphi"):line.find("/Eve")]
                    mphi = line[line.find("Mphi")+4:line.find("_Mchi")]
                    mchi = line[line.find("Mchi")+4:line.find("_g")]
                    gq = line[line.find("_gq")+3:line.find("/Eve")].replace('p','.')
                    gq = gq[0:gq.find('_')]
                    
                    print gq
                    sampleList.append(model)
                    sampleList.append(int(mphi))
                    sampleList.append(int(mchi))
                    sampleList.append(float(gq))
                if "After matching:" in line:
                    xsec = line.split()[6]
                    xsecerr = line.split()[8]
                    sampleList.append(float(xsec))
     #               sampleList.append(xsecerr)
            samplesList.append(sampleList)

    #with open(m+"_xsec.csv", "wb") as fcsv:
    #    writer = csv.writer(fcsv)
     #   writer.writerows(samplesList)

    return samplesList

def createDataFrame(samplesList):
    
    df = pd.DataFrame(samplesList)
    df = df.set_index([0])
    df.columns = ['mPhi','mChi','gq','xsec'] 
    df.index.name = 'Model'
    df['xsec'] = df['xsec'].astype(float)
    df['gq'] = df['gq'].astype(float)
    df['mChi'] = df['mChi'].astype(float)
    df['mPhi'] = df['mPhi'].astype(float)
    df = df.groupby(df.index).mean()
    
    print df    
    df.to_csv("pandas_"+model+".csv")

    return df

def make2Dplot(df, model):
    massXsecPlot = TH2D("massXsecPlot","massXsecPlot",11,-12.5,262.5,7,-5,65)
    c_massXsecPlot = TCanvas("c_massXsecPlot","c_massXsecPlot",800,600)
    for index, row in df.iterrows():
        massXsecPlot.Fill(row['mPhi'], row['mChi'], row['xsec'])
    c_massXsecPlot.cd()
    massXsecPlot.Draw("colztext")
    massXsecPlot.SetMarkerSize(1.4)
    massXsecPlot.SetTitle(model + " tt+DM model")
    massXsecPlot.GetYaxis().SetTitle("m_{#chi} [GeV]")
    massXsecPlot.GetXaxis().SetTitle("m_{#phi} [GeV]")
    massXsecPlot.GetZaxis().SetTitle("Cross section [pb]")
    c_massXsecPlot.SetRightMargin(0.1541353);
    c_massXsecPlot.SaveAs(model+"_xsec.pdf")
    c_massXsecPlot.SaveAs(model+"_xsec.root")
    
    return 1

def makeGraph(df, model):
    
    masses = df['mPhi']
    masses = set(masses)
    print masses
    subframes =[]
    for m in masses:
        k = df.loc[(df['mPhi']==m)]
        x_arr = np.array(k['gq'])
        y_arr = np.array(k['xsec'])
        N = len(x_arr)
        graph = TGraph(N, x_arr, y_arr)
        graph.SaveAs(model+'_Mass'+str(int(m)).replace('.','p')+"_graph.root")

    return 1


def makePlotFit(model):
    styles = {
    '1': [kBlue,(0.05,  1.2)],
    '10' : [kRed,(0.05,  1.2)],
    '20' : [kGreen,(0.05,  1.2)],
    '50' : [kAzure,(0.1 , 1.2)],
    '100' : [kBlack,(0.1 , 1.2)],
    '200' : [kMagenta,(0.4,  1.7)],
    '300' : [kOrange,(0.4  ,2.2)],
    '500' : [kViolet,(0.4  ,4)]}

    fout = TFile("graphs_fits_"+model+".root",'RECREATE')
    filelist = glob.glob(model+'_*.root')
    canvas = TCanvas("graphs","graphs", 800, 600)
    dummy = TH1D("dummy",model + " cross section vs coupling",10,0,3.6)
    dummy.Draw()
    dummy.GetYaxis().SetRangeUser(0.001,25)
    dummy.GetYaxis().SetTitle("cross section [pb]")
    dummy.GetXaxis().SetTitle("coupling gq (gDM = 1)")
    graphs = []
    functions = []
    leg = TLegend(0.660401,0.4591304,0.8709273,0.8834783)
    leg.SetTextSize(0.02782609)
    for i,fin in enumerate(filelist):

        mass = fin[fin.find('Mass')+4:fin.find('_gr')]
        print mass
        Tf = TFile(fin)
        graph = Tf.Get("Graph")
        canvas.cd()

        start = styles[mass][1][0]
        stop = styles[mass][1][1]
        color = styles[mass][0]

        print start, stop, color
        function = TF1("pol3","pol3",start,stop);
        graph.Draw("samec*")
        graph.Fit(function,'R')
        function.Draw("same")
        function.SetTitle(model+ ': '+ mass + ' GeV')
        leg.AddEntry(function,function.GetTitle(),'lep')
        function.SetLineColor(color)

        graph.SetName(model+ '_graph_'+ mass)
        function.SetName(model+ '_fitpol3_'+ mass)

        Tf.Close()

        SetOwnership(graph, 0)
        SetOwnership(function, 0)
        graphs.append(graph)
        graphs.append(function)
        fout.cd()
        function.Write()
        graph.Write()

    leg.Draw()
    fout.cd()
    canvas.SetLogy()
    canvas.Write()

    fout.Close()



def extractCouplingLimit(model):

    fin = TFile("graphs_fits_"+model+".root")
    fOut = open('CouplingLimits_'+model+'.txt','w')


    with open("Limits_"+model+".txt") as flim:
        readerlim = csv.reader(flim)
        limits = list(readerlim)

    print limits

    fOut.write("== Model ==    g_obs     g_exp   [  g-1sig, g+1sig  ]  [  g-2sig, g+2sig  ] \n")

    for limit in limits[1:]:
        
        xsec = float(limit[3])

        xsecLimits = ()
        xsecLimits = (xsec*float(limit[4]), xsec*float(limit[5]), xsec*float(limit[6]), xsec*float(limit[7]), xsec*float(limit[8]), xsec*float(limit[9]))

        modelShort = limit[0]
        mPhi = limit[1]
        mChi = limit[2]


        functionName = model+"_fitpol3_"+mPhi
        function = TF1()

        function = fin.Get(functionName)

        print model, mPhi, mChi
        print 'rLimits',limit
        print 'xsecLimit', xsecLimits
        print xsecLimits[0], xsecLimits[1], xsecLimits[2]
        couplingLimits = [function.GetX(x) for x in xsecLimits]
        fOut.write(modelShort + "  " + mPhi + "     " + mChi + "     ")
        print couplingLimits
        for c in couplingLimits:
            fOut.write(str('%.2f' %  c)+'       ')
        fOut.write(' \n')
    fOut.close()
    fin.Close()
    return 1

if __name__ == "__main__":

    #This code will extrac cross sections from log files, turn them into functions, and extract limits in coupling
    model = "Scalar"
    if len(sys.argv) > 1:
        model = sys.argv[1]

    print "using", model
    samplesList = list()
    samplesList = readLogFiles(model+"/logs", model)


    #intermediate step for the data format
    df = createDataFrame(samplesList)


    #Needed for the coupling vs cross section extraction
    makeGraph(df, model)  
    makePlotFit(model)
    extractCouplingLimit(model)
