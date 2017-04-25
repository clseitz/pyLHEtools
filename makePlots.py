import ROOT 
ROOT.gROOT.SetBatch() 

legenden = ['g=1','g=0.6','g=0.7','g=0.8']
title = 'Pt'
xMin = 0
xMax = 500
nBins = 20
treePath = './rootFiles'
histoPath= './'

treeName = 'events'
#histoName = 'Count'
plotPath = './'

#files
jobs = ['DMScalar_Mphi50_Mchi1_g1','DMScalar_Mphi50_Mchi1_g0p6','DMScalar_Mphi50_Mchi1_g0p7','DMScalar_Mphi50_Mchi1_g0p8']

#selection
treeCut = 'PdgID==9100000'
#treeCut = 'ID==6 || ID==-6'

treeVar = 'Pt'
xTitle = 'p_{T} (GeV)'
yTitle = 'Normalized events'
colors = [2,8,4,ROOT.kMagenta+2]
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


def getHistoFromTree(job):
        global num

        hTree = ROOT.TH1F(job,job,nBins,xMin,xMax)
        hTree.Sumw2()
        Tree = getTree(job)
        Tree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job,nBins,xMin,xMax),'(%s)' %(treeCut),"goff")
        hTree = ROOT.gDirectory.Get(job)
	hTree.Sumw2()
	hTree.SetDirectory(0)

        nEvents = hTree.Integral()

        if nEvents != 0:
            hTree.Scale(1/nEvents)
	    num = num+1
	return hTree
            
def makePlots():
	
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

        #c.SetLogy()
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

	for i in range(0,len(histos)):
            histos[i].SetFillStyle(0)
            histos[i].SetLineColor(colors[i])
            histos[i].SetLineWidth(3)
	    if i !=0: histos[i].SetLineStyle(ROOT.kDashed)
	    histos[i].Sumw2() 
            allStack.Add(histos[i])
            l.AddEntry(histos[i],legenden[i],'l')

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

	ratio = []
	print "len ", len(histos)
	for i in range(0,len(histos)-1):
		print "i ", i
		ratio.append(histos[0].Clone("ratio"))
	print " ratio ", ratio

	#for i in range(1,len(histos)):
	for i in range(0,len(histos)-1):
		print " ratio ", ratio
		print " ratio[0] ", ratio[0]
		print " ratio[1] ", ratio[1]
		print " ratio[2] ", ratio[2]
	#ratio[i].append(histos[0].Clone("ratio"))
		ratio[i].SetLineColor(colors[i+1])        
		ratio[i].Sumw2()        
		ratio[i].SetStats(0)        

		print "i ", i
		denom = histos[i].Clone("denom")        
		denom.Sumw2()        
		
		ratio[i].Divide(denom)        
		ratio[i].SetMarkerStyle(20)        
		ratio[i].SetMarkerColor(colors[i+1])        
		ratio[i].SetMarkerSize(0.6)        

		if i==0: ratio[i].Draw("PE0,X0") #epx0        
		else: ratio[i].Draw("PE0,X0same")
		
	f1 = ROOT.TF1("myfunc","[0]",xMin,xMax);        
	f1.SetLineColor(ROOT.kGray+3)        
	f1.SetLineStyle(ROOT.kDashed)        
	f1.SetParameter(0,1);        
	f1.Draw("same")
	for i in range(0,len(histos)-1):
		ratio[i].Draw("PE0,X0same")
		
	ratio[0].SetTitle("")   
	ratio[0].Sumw2()        
	ratio[0].GetXaxis().SetTitle(xTitle)        
	ratio[0].GetYaxis().SetTitle("g=1 / g")        
	ratio[0].GetYaxis().SetNdivisions(503)        
	
	ratio[0].GetXaxis().SetLabelFont(42);        
	ratio[0].GetYaxis().SetLabelFont(42);        
	ratio[0].GetXaxis().SetLabelSize(0.11);        
	ratio[0].GetYaxis().SetLabelSize(0.11);        
	ratio[0].GetXaxis().SetLabelOffset(0.04)        
	ratio[0].GetYaxis().SetLabelOffset(0.02)
	
	ratio[0].GetXaxis().SetTitleFont(42);        
	ratio[0].GetYaxis().SetTitleFont(42);        
	ratio[0].GetXaxis().SetTitleOffset(1.45);        
	ratio[0].GetYaxis().SetTitleOffset(0.5);#0.31 ##0.29        
	ratio[0].GetXaxis().SetTitleSize(0.12);        
	ratio[0].GetYaxis().SetTitleSize(0.12);        
	
	ratio[0].GetYaxis().SetRangeUser(0.5,1.5);#-2.3,3.7        

	

		
        name_pdf = '%s/%s.pdf' %(plotPath,title)
        name_root = '%s/%s.root' %(plotPath,title)
        c.Print(name_pdf)
        c.Print(name_root)

makePlots()
