# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/ThirteenTeV/Hadronizer_TuneCUETP8M1_13TeV_MLM_4f_max1j_LHE_pythia8_cff.py -s GEN --mc --no_exec --conditions auto:mc -n -1 --filein file:DMPseudo_Mphi10_Mchi1_g0p8.lhe
import FWCore.ParameterSet.Config as cms
import os, sys
process = cms.Process('GEN')


#Get input file name from submit script
if len(sys.argv) > 5:
        fin = sys.argv[2]
	RunEvents = int(sys.argv[3])
	JobNumber = int(sys.argv[4])
	outfolder = sys.argv[5]
	start = fin.find('ttDM')
	stop=fin.find('/Eve')
	#fout = (os.path.split(fin)[1]).replace('.lhe','_Pythia8_'+str(JobNumber)+'_GEN.root')
	fout =  outfolder + '/' + fin[start:stop] + '_Pythia8_'+str(JobNumber)+'_GEN.root'
	print fout
	print '# Running input file', fin
	print '# producing outputfile', fout
	print '# Runnning job ', str(JobNumber), 'with ', str(RunEvents),' events, skipping ', str(JobNumber*RunEvents) 

else:
        print "No input file given"
	exit(0)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedNominalCollision2015_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(RunEvents)
)

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 500

# Input source
process.source = cms.Source("LHESource",
    fileNames = cms.untracked.vstring('file:'+fin),
			    inputCommands = cms.untracked.vstring('keep *', 
								  'drop LHEXMLStringProduct_*_*_*'),
			    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
			    skipEvents=cms.untracked.uint32(JobNumber * RunEvents)

			    
)

process.options = cms.untracked.PSet(

)

# Production Infosout
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('Configuration/GenProduction/python/ThirteenTeV/Hadronizer_TuneCUETP8M1_13TeV_MLM_4f_max1j_LHE_pythia8_cff.py nevts:-1'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
#    outputCommands = process.RECOSIMEventContent.outputCommands,
    outputCommands = cms.untracked.vstring('drop *',
					   'keep recoGenParticles_*_*_*', 
					   'keep LHEEventProduct_*_*_*',
					   'keep recoGenJets_ak4GenJets_*_*',
					   'keep recoGenMETs_genMetTrue_*_*',
					   'keep recoGenMETs_genMetCalo_*_*',
					   ),

    fileName = cms.untracked.string(fout),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.0),
    maxEventsToPrint = cms.untracked.int32(1),
    PythiaParameters = cms.PSet(
        pythia8CommonSettings = cms.vstring('Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 10', 
            'ParticleDecays:allowPhotonRadiation = on'),
        pythia8CUEP8M1Settings = cms.vstring('Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:pT0Ref=2.4024', 
            'MultipartonInteractions:ecmPow=0.25208', 
            'MultipartonInteractions:expPow=1.6'),
        processParameters = cms.vstring('JetMatching:setMad = off', 
            'JetMatching:scheme = 1', 
            'JetMatching:merge = on', 
            'JetMatching:jetAlgorithm = 2', 
            'JetMatching:etaJetMax = 5.', 
            'JetMatching:coneRadius = 1.', 
            'JetMatching:slowJetPower = 1', 
            'JetMatching:qCut = 90.', 
            'JetMatching:nQmatch = 4', 
            'JetMatching:nJetMax = 1', 
            'JetMatching:doShowerKt = off', 
            'Check:epTolErr = 0.0003', 
            '9100000:new  = MED MED 3 0 0 X_MMed_X 0 0 0 99999', 
            '9100022:new  = DM  DM  2 0 0 X_MFM_X  0 0 0 99999', 
            '9100022:mayDecay = off'),
        parameterSets = cms.vstring('pythia8CommonSettings', 
            'pythia8CUEP8M1Settings', 
            'processParameters')
    )
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RECOSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

