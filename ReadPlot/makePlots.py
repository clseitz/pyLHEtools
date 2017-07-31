import ROOT 
ROOT.gROOT.SetBatch() 
import glob, os
import math
title = 'Pt'
xMin = 0
xMax = 700
nBins = 10
treePath = 'rootFiles/'
histoPath= './'

treeName = 'events'
#histoName = 'Count'
plotPath = './'

#files


#selection
treeCut = 'PdgID==800'
#treeCut = 'PdgID==6 || PdgID==-6'

treeVar = 'Pt'
xTitle = 'Mediator p_{T} (GeV)'
yTitle = 'Normalized events'
colors = [2,8,4,ROOT.kMagenta+2, ROOT.kBlue]
num = 0


def getTree(job):
        Tree = ROOT.TChain(treeName)
        Tree.Add("%s/%s.root" %(treePath,job))
        Tree.SetDirectory(0)
        nEntries = Tree.GetEntries()

        return Tree

def getHisto(job):
    global histoPath

    fName = histoPath
    fName += job
    fName += '.root'
    
    print "histo name ", fName

    FileHisto = ROOT.TFile(fName)

    histoCount = ROOT.TH1F()
    histoCount = FileHisto.Get('E')
    histoCount.SetDirectory(0)

    FileHisto.Close()
    return histoCount


def getHistoFromTree(job, includeOverflow = True):
	global num

        hTree = ROOT.TH1F(job,job,nBins,xMin,xMax)
        hTree.Sumw2()
        Tree = getTree(job)
        Tree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job,nBins,xMin,xMax),'(%s)' %(treeCut),"goff")
        hTree = ROOT.gDirectory.Get(job)
	hTree.Sumw2()
	hTree.SetDirectory(0)
	hTree.SetTitle(job)



	if includeOverflow:
		nbins = hTree.GetNbinsX()
		overflow = hTree.GetBinContent(nbins+1)
		overflowE = hTree.GetBinError(nbins+1)
		lastbinContent = hTree.GetBinContent(nbins)
		lastbinContentE = hTree.GetBinError(nbins)
		hTree.SetBinContent(nbins, overflow+lastbinContent)
		hTree.SetBinError(nbins, math.sqrt(overflowE*overflowE+lastbinContentE*lastbinContentE))
        nEvents = hTree.Integral()
        if nEvents != 0:
            hTree.Scale(1/nEvents)
	    num = num+1

	return hTree
            
def makePlots(jobs, variable, legends):
	
        ROOT.gROOT.SetStyle("Plain")

	H=600         
	W=600     
	T = 0.08*H
	B = 0.12*H 
	L = 0.12*W 
	R = 0.08*W

        c = ROOT.TCanvas(title,title, 600, 600)
	c.SetFillColor(0);     
	c.SetBorderMode(0);     
	c.SetFrameFillStyle(0);     
	c.SetFrameBorderMode(0);     
	#c.SetLeftMargin( 0.13 );     
	#c.SetRightMargin( 0.08 );     
	#c.SetBottomMargin(0.12);     
	#c.SetTopMargin(0.08);     

	pad1= ROOT.TPad("pad1", "pad1", 0, 0.33 , 1, 1)        
	pad1.SetTopMargin(0.08)        
	pad1.SetBottomMargin(0.02)        
	pad1.SetLeftMargin(0.12)        
	pad1.SetRightMargin(0.05)
	pad1.SetBorderMode(0)
	pad1.SetTickx(0)
	pad1.SetTicky(0)    
	pad1.Draw()    
	pad1.cd()
	pad1.SetLogy() 
	
        allStack = ROOT.THStack(title,title)
	histos = []
	for job in jobs:
            hTemp = getHistoFromTree(job)
	    hTemp.Sumw2()
            histos.append(hTemp)

	l = ROOT.TLegend(0.70,0.58,0.93,0.89)
	l.SetFillColor(0)     
	l.SetFillStyle(0)     
	l.SetTextFont(42)     
	l.SetBorderSize(0)
	l.SetTextSize(0.04)

	l.SetHeader('Model: ' + variable)
	for i in range(0,len(histos)):
            histos[i].SetFillStyle(0)
            histos[i].SetLineColor(colors[i])
            histos[i].SetLineWidth(3)
	    if i !=0: histos[i].SetLineStyle(ROOT.kDashed)
	    histos[i].Sumw2() 
            allStack.Add(histos[i])
            l.AddEntry(histos[i],legends[i],'l')

	allStack.Add(histos[0])

	allStack.SetTitle('')
        allStack.Draw("HISTNOSTACK,e")
        allStack.GetXaxis().SetTitle(xTitle)
        allStack.GetYaxis().SetTitle(yTitle)

	allStack.GetXaxis().SetLabelFont(42);
	allStack.GetYaxis().SetLabelFont(42);
	allStack.GetXaxis().SetTitleFont(42);
	allStack.GetYaxis().SetTitleFont(42);

	allStack.GetYaxis().SetTitleSize(0.052);
	allStack.GetYaxis().SetLabelSize(0.05);

        allStack.GetHistogram().GetXaxis().SetLabelOffset(0.1)         
	allStack.GetHistogram().GetYaxis().SetLabelOffset(0.01)
	allStack.GetHistogram().GetYaxis().SetTitleOffset(1.2)

        allStack.GetXaxis().SetRangeUser(xMin,xMax)
        allStack.SetMinimum(0.001)
        allStack.SetMaximum(2)

        l.Draw()

	#ratio plot
	c.cd()
	pad2 = ROOT.TPad("pad2", "pad2", 0, 0.01, 1, 0.32)         
	pad2.SetTopMargin(0.045)#0.05
	pad2.SetBottomMargin(0.35)#0.45        
	pad2.SetLeftMargin(0.12)        
	pad2.SetRightMargin(0.05)        
	c.cd()        

	pad2.Draw()        
	pad2.cd()        

	ratios =[]
	baseline = histos[0].Clone("baseline")
	baseline.SetLineColor(0)
	baseline.Draw("histe")
	baseline.SetStats(0)
	for i,h in enumerate(histos):
		ratio = h.Clone()
		print baseline.GetTitle(), ratio.GetTitle()
		print i
		ratio.Divide(baseline)
		ratio.SetMarkerStyle(20)        
		ratio.SetMarkerColor(colors[i])        
		ratio.SetMarkerSize(0.6)        
		ratio.SetStats(0)
		if i > 0: ratios.append(ratio)
		
		
	f1 = ROOT.TF1("myfunc","[0]",xMin,xMax);        
	f1.SetLineColor(ROOT.kGray+3)
	f1.SetLineWidth(1)
	f1.SetParameter(0,1);        
	f1.Draw("same")
	for ratio in ratios:
		ratio.Draw("histesame")
		
	baseline.SetTitle("")   
	baseline.Sumw2()        
	baseline.GetXaxis().SetTitle(xTitle)        
	baseline.GetYaxis().SetTitle("g = x / g = 1")        
	baseline.GetYaxis().SetNdivisions(503)        
	
	baseline.GetXaxis().SetLabelFont(42);        
	baseline.GetYaxis().SetLabelFont(42);        
	baseline.GetXaxis().SetLabelSize(0.11);        
	baseline.GetYaxis().SetLabelSize(0.11);        
	baseline.GetXaxis().SetLabelOffset(0.04)        
	baseline.GetYaxis().SetLabelOffset(0.02)
	
	baseline.GetXaxis().SetTitleFont(42);        
	baseline.GetYaxis().SetTitleFont(42);        
	baseline.GetXaxis().SetTitleOffset(1.45);        
	baseline.GetYaxis().SetTitleOffset(0.5);#0.31 ##0.29        
	baseline.GetXaxis().SetTitleSize(0.12);        
	baseline.GetYaxis().SetTitleSize(0.12);        
	
	baseline.GetYaxis().SetRangeUser(0.5,1.5);#-2.3,3.7        

	

		
        name_pdf = '%s/%s_%s.pdf' %(plotPath,title,variable)
        name_root = '%s/%s_%s.root' %(plotPath,title,variable)
        c.Print(name_pdf)
        c.Print(name_root)


if __name__ == "__main__":   

	fileList = glob.glob(treePath+'/*root')
	models = [] #list with dictionary for the model paramters
	mPhis = []
	gs = []
	for f in fileList:
		modelName = os.path.basename(f).replace('.root','').split('_')
		model = {}
		model['type'] = modelName[0]
		model['mPhi'] = modelName[1]
		model['mChi'] = modelName[2]		
		model['g'] = modelName[3]
		models.append(model)
		mPhis.append(model['mPhi'])
		gs.append(model['g'])
	
	mPhis = list(set(mPhis))
	gs = list(set(gs))
	jobs = []

	#order the model list 
	for mPhi in mPhis:
		jobs = [item['type']+'_'+item['mPhi']+'_'+item['mChi']+'_'+item['g'] for item in models if item["mPhi"] == mPhi and item["g"] == 'g1']
		legends = [item['g'] for item in models if item["mPhi"] == mPhi and item["g"] == 'g1']
		#find all items that are not g=1
		jobs =jobs + [item['type']+'_'+item['mPhi']+'_'+item['mChi']+'_'+item['g'] for item in models if item["mPhi"] == mPhi and item["g"] != 'g1']
		legends = legends + [item['g'] for item in models if item["mPhi"] == mPhi and item["g"] != 'g1']
		print jobs
		print legends
		makePlots(jobs, mPhi, legends)
	
	#for now just make one plot for coupling g1
	jobs = [item['type']+'_'+item['mPhi']+'_'+item['mChi']+'_'+item['g'] for item in models if  item["g"] == 'g1' and item["mPhi"] == 'Mphi10']
	legends = [item['mPhi'] for item in models if  item["g"] == 'g1' and item["mPhi"] == 'Mphi10']
	jobs =  jobs + [item['type']+'_'+item['mPhi']+'_'+item['mChi']+'_'+item['g'] for item in models if  item["g"] == 'g1' and item["mPhi"] != 'Mphi10']
	legends = legends + [item['mPhi'] for item in models if  item["g"] == 'g1' and item["mPhi"] != 'Mphi10']
	print jobs
	print legends
	makePlots(jobs, 'g1', legends)
