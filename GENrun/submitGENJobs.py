#!/usr/bin/env python
import os, glob, sys
from commands import getoutput
import re

#locatin /nfs/dust/cms/user/clseitz/DarkMatterMC/LHE_Grid_Scalar_Jul25/DMScalar_ttbar01j_Mphi100_Mchi20_g1_44965/Events/run_01/
def createJobs(f , jobs, i, EventsPerJob, outfolder):
    cmd = 'cmsRun Hadronizer_TuneCUETP8M1_13TeV_MLM_4f_max1j_LHE_pythia8_cff_py_GEN.py ' + f + ' '+ str(EventsPerJob) + ' ' + str(i) + ' ' + outfolder + '\n'
    print cmd
    jobs.write(cmd)
    return 1

def submitJobs(jobList, nchunks):
    print 'Reading joblist'
    jobListName = jobList
    print jobList
    subCmd = 'qsub -t 1-%s -o logs nafbatch_runner_GEN.sh %s' %(nchunks,jobListName)
    print 'Going to submit', nchunks, 'jobs with', subCmd
    os.system(subCmd)

    return 1

def getNEvents(f):
    nEvents = getoutput('grep "<event"  ' + f + ' | wc')
    return int(nEvents.split(' ')[1])
if __name__ == "__main__":

    outfolder = "Output"
    ## remove '-b' option
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print 'Location of input LHe files', pattern
    else:
        print "No location given, give folder with LHE files"
        exit(0)

    if len(sys.argv) > 2:
        outfolder = sys.argv[2]
        print 'Output goes here: ', outfolder                                                                                                                                    
    else:                                                                                                                                                                                       print "Using default output folder: ", outfolder                                                                                                                            

    try: os.stat(outfolder) 
    except: os.mkdir(outfolder)

    try: os.stat(outfolder+'/logs') 
    except: os.mkdir(outfolder+'/logs')
    
#    pattern = "datacardsABCD_2p1bins_fullscan2"
    filelist = glob.glob(pattern+'/DM*/*/*/'+'*.lhe')
    jobList = 'joblist.txt'
    jobs = open(jobList, 'w')
    nChunks = 0
    for f in filelist:
        print f
        nEvents = getNEvents(f)
        EventsPerJob = 100000
        nJobs = nEvents / EventsPerJob
        
        for i in range(0, nJobs):
            print i
            createJobs(f,jobs,i,EventsPerJob, outfolder)
            nChunks = nChunks+1

    jobs.close()
    submit = raw_input("Do you also want to submit the jobs to the batch system? [y/n] ")
    if submit == 'y' or submit=='Y':
        submitJobs(jobList,nChunks)
    else:
        print "Not submitting jobs"


    
