
#! /usr/bin/env python

import sys, os
import argparse

#Format would be easier with pandas but not available in CMSSW7
#Define the point you want to generate with 4 parameters
#{'model': ['Scalar'], 'mChi': [1], 'mPhi': [75, 125, 150], 'gq': [1], 'gDM' : [1]}

MassScalar = [
    ['MassScalar'],
    [
        {'model': ['Scalar'],'mChi': [1], 'mPhi': [75, 125, 150], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [10], 'mPhi': [75, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [20], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Scalar'],'mChi': [30], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]}
        ]
    ]


MassPseudo = [
    ['MassPseudo'],
    [
        {'model': ['Pseudo'],'mChi': [1], 'mPhi': [75, 125, 150, 250], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [10], 'mPhi': [75, 125, 150, 200, 250], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [20], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [30], 'mPhi': [50, 75, 100, 125, 150, 200], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [50], 'mPhi': [175, 225, 250], 'gq': [1], 'gDM' : [1]},
        {'model': ['Pseudo'],'mChi': [30], 'mPhi': [175, 225, 250], 'gq': [1], 'gDM' : [1]},
        ]
    ]

Coupling = [
    ['Coupling'],
    [{'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [10], 'gq': [0.1, 0.2, 0.5, 0.6, 0.7, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [20], 'gq': [0.1, 0.2, 0.5, 0.6, 0.7, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [50], 'gq': [0.2, 0.5, 0.6, 0.7, 0.8, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [100], 'gq': [0.2, 0.5, 0.6, 0.7, 0.8, 1], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [200], 'gq': [0.5, 0.7, 1, 1.3, 1.4, 1.5], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [300], 'gq': [0.5, 1, 1.3, 1.4, 1.6, 2], 'gDM' : [1]},
     {'model': ['Scalar','Pseudo'],'mChi': [1], 'mPhi': [500], 'gq': [0.5, 1, 1.5,2, 2.5, 3, 3.5], 'gDM' : [1]}
     ]
    ]


Test = [
    ['Test'],
    [{'model': ['Scalar','Pseudo'],'mChi': [1,20], 'mPhi': [10,50], 'gq': [1], 'gDM' : [1]},
]]
mAll = [MassScalar, MassPseudo, Coupling, Test]
##################################

nEvents = 100000
#nEvents = 10
import time,datetime,random

rseed = datetime.datetime.now()
seed = random.randint(1, 50000) 


def createJobs(mSample, filein, outlocation,scenario):
    jobs = []
    counter = 0
    for sample in mSample[1]:
        models = sample['model']
        mChis = sample['mChi']
        mPhis = sample['mPhi']
        gqs = sample['gq']
        gDMs = sample['gDM']
        for model in models:
            for mChi in mChis:
                for mPhi in mPhis:
                    for gq in gqs:
                        for gDM in gDMs:
                            print "model", model,"mChi",mChi,"mPhi",mPhi, "gq", gq,"gDM", gDM
                            fileout = filein.replace("X",str(mChi)).replace("Y",str(mPhi)+"_MG").replace('Model',model).replace('VarGDM',str(gDM).replace('.','p')).replace('VarGq',str(gq).replace('.','p'))
                            
                            f = open(filein,'r')
                            filedata = f.read()
                            f.close()
                            
                            newdata = filedata.replace("VarMphi",str(mPhi)).replace("VarMchi",str(mChi))
                            
                            newdata = newdata.replace("Varnevents",str(nEvents))
                            newdata = newdata.replace("VarIseed",str(seed))
                            newdata = newdata.replace("VarModel",str(model))
                            newdata = newdata.replace("VarScenario",str(scenario))
                            newdata = newdata.replace("VarLocation",str(outlocation))
                            newdata = newdata.replace("VarGDMstr",str(gDM).replace('.','p'))
                            newdata = newdata.replace("VarGqstr",str(gq).replace('.','p'))
                            newdata = newdata.replace("VarGDM",str(gDM))
                            newdata = newdata.replace("VarGq",str(gq))
                            counter = counter+1
                            f = open(fileout,'w')
                            f.write(newdata)
                            f.close()
                            jobs.append(fileout)
    
    return jobs
if __name__ == "__main__":
    
    filein = "ttDMModel_MchiXMphiY_CMS_5F_gDMVarGDM_gqVarGq.sh"
    scenario = 'Scalar'
    mModel = mAll[0]

    inputs = [x[0][0] for x in mAll]


    if len(sys.argv) > 1:
        scenario = sys.argv[1]
        if scenario in inputs:
            print "Running scenario: ", scenario
        else:
            print "No valid input provided"
            print "Possible input scenarios are (check in code for more detail): ", inputs
            exit(0)
    else:
        print "No input provided"
        print "Possible input scenarios are (check in code for more detail): ", inputs
        exit(0)

    for m in mAll:
        print m[0]
        if scenario in m[0]:
            mModel = m

    print "running the following setup"
    print mModel
    print '=============================='

    counter = 0
 #   outlocation = '/eos/cms/store/cmst3/group/susy/clseitz/DMsignal/' #doesn't seemm to work
    outlocation = os.getcwd() +"/"
    print outlocation
    jobs = createJobs(mModel, filein, outlocation, scenario)


    outFolder = outlocation+'output_' + str(scenario) + '_' + str(seed)
    try: os.stat(outFolder) 
    except: os.mkdir(outFolder)

    try: os.stat(outFolder + '/logs') 
    except: os.mkdir(outFolder + '/logs')

    try: os.stat(outFolder +'/cards') 
    except: os.mkdir(outFolder + '/cards')

    for job in jobs:    
        cmd = "mv "+ job + " " + outFolder+"/cards/."
#        print cmd
        os.system(cmd)

    submit = raw_input("Do you also want to submit "+str(len(jobs))+" jobs to the batch system? [y/n] ")
    if submit == 'y' or submit=='Y':
        print "Submitting jobs"
        for job in jobs:    
            cmd = "bsub -q 2nw -o " + outFolder+ "/logs/" + job.replace('.sh','_STDOUT.txt') + " -e "+outFolder+ "/logs/" + job.replace('.sh','_ERR.txt') + " batchRunner.sh "  + outFolder+"/cards/"+job
            print cmd
            os.system(cmd)

    else:
        print "Not submitting jobs"
            
