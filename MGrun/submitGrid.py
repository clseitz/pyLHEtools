#! /usr/bin/env python

import sys, os
import argparse

mScalar = {1: [75, 125, 150],
          10: [75, 125, 150, 200],
          20: [50, 75, 100, 125, 150, 200],
          30: [50, 75, 100, 125, 150, 200]}


mPseudo = {1: [75, 125, 150, 250],
           10: [75, 125, 150, 200, 250],
           20: [50, 75, 100, 125, 150, 200],
           30: [50, 75, 100, 125, 150, 200],
           50: [175, 225, 250],
           60: [175, 225, 250]}


#nEvents = 100000
nEvents = 10
import time,datetime,random
#seed = int(time.mktime(datetime.datetime.now().timetuple()))
rseed = datetime.datetime.now()
seed = random.randint(1, 50000) 


def createJobs(mSample, model, filein):
    jobs = []
    counter = 0
    for mChi, mPhis in mSample.iteritems():
        for mPhi in mPhis:
            print "mChi",mChi,"mPhi",mPhi
            fileout = filein.replace("X",str(mChi)).replace("Y",str(mPhi)+"_MG").replace('Model',model)
            f = open(filein,'r')
            filedata = f.read()
            f.close()
            
            newdata = filedata.replace("VarMphi",str(mPhi)).replace("VarMchi",str(mChi))
            
            newdata = newdata.replace("Varnevents",str(nEvents))
            newdata = newdata.replace("VarIseed",str(seed))
            newdata = newdata.replace("VarModel",str(model))
            counter = counter+1
            f = open(fileout,'w')
            f.write(newdata)
            f.close()
            jobs.append(fileout)
    
    return jobs
if __name__ == "__main__":
    
    filein = "ttDMModel_MchiXMphiY_CMS_5F_g1.sh"
    model = 'Scalar'
    mModel = mScalar

    if len(sys.argv) > 1:
        model = sys.argv[1]
        print 'Running model: ', model
    else:
        print "Using default model: ", model

    if model == 'Pseduo': mModel = mPseudo

    counter = 0
    jobs = createJobs(mModel, model, filein)

    try: os.stat('output_' + str(seed)) 
    except: os.mkdir('output_' + str(seed))

    try: os.stat('output_' + str(seed) + '/logs') 
    except: os.mkdir('output_' + str(seed) + '/logs')
 
    submit = raw_input("Do you also want to submit the jobs to the batch system? [y/n] ")
    if submit == 'y' or submit=='Y':
        print "Submitting jobs"
        for job in jobs:    
            cmd = "mv "+ job + " output_"+str(seed)+"/."
            print cmd
            os.system(cmd)
            cmd = "bsub -q 2nw -o output_" +str(seed)+ "/logs/" + job.replace('.sh','_STDOUT.txt') + " -e output_" +str(seed) + "/logs/" + job.replace('.sh','_ERR.txt') + " batchRunner.sh "  + "output_" +str(seed)+"/"+job
            print cmd
            os.system(cmd)

    else:
        print "Not submitting jobs"
            
