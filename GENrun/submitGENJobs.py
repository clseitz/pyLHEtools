#!/usr/bin/env python
import os, glob, sys
from commands import getoutput
import re

#locatin /nfs/dust/cms/user/clseitz/DarkMatterMC/LHE_Grid_Scalar_Jul25/DMScalar_ttbar01j_Mphi100_Mchi20_g1_44965/Events/run_01/
def createJobs(f , jobs, i, EventsPerJob, outfolder, ttDilep):
    cmd = 'cmsRun Hadronizer_TuneCUETP8M1_13TeV_MLM_4f_max1j_LHE_pythia8_cff_py_GEN.py ' + f + ' '+ str(EventsPerJob) + ' ' + str(i) + ' ' + outfolder + '\n'
    if ttDilep:
        cmd = 'cmsRun Hadronizer_TTDilep_TuneCUETP8M1_13TeV_MLM_4f_max1j_LHE_pythia8_cff_py_GEN.py ' + f + ' '+ str(EventsPerJob) + ' ' + str(i) + ' ' + outfolder + '\n'
    print cmd
    jobs.write(cmd)
    return 1

def submitJobs(jobList, nchunks, outfolder, batchSystem):
    print 'Reading joblist'
    jobListName = jobList
    print jobList
#    subCmd = 'qsub -t 1-%s -o logs nafbatch_runner_GEN.sh %s' %(nchunks,jobListName)
    subCmd = 'qsub -t 1-%s -o %s/logs/ ../scripts/%s %s' %(nchunks,outfolder,batchSystem,jobListName)
    print 'Going to submit', nchunks, 'jobs with', subCmd
    os.system(subCmd)

    return 1

def getNEvents(f):
    nEvents = getoutput('grep "<event"  ' + f + ' | wc')
    nEvents = list(set(nEvents.split(' ')))
    return int(nEvents[1])
if __name__ == "__main__":

    outfolder = "Output"

    #should probably rewrite with option parser
    batchSystem = 'psibatch_runner.sh'
    if '-naf' in sys.argv:  
        sys.argv.remove('-naf')                                                                                                                        
        batchSystem = 'nafbatch_runner.sh'
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print 'Location of input LHe files', pattern
    else:
        print "No location given, give folder with LHE files"
        exit(0)

    if len(sys.argv) > 2:
        outfolder = sys.argv[2]
        print 'Output goes here: ', outfolder                                                                                                                                    
    else: 
        print "Using default output folder: ", outfolder                                                                                                                            

    ttDilep = False
    if len(sys.argv) > 3:
        if "Dilep" in sys.argv[3]:
            ttDilep = True

    if ttDilep: print "running dilepton events only"

    try: os.stat(outfolder) 
    except: os.mkdir(outfolder)

    try: os.stat(outfolder+'/logs/') 
    except: os.mkdir(outfolder+'/logs/')
    
#    pattern = "datacardsABCD_2p1bins_fullscan2"
    filelist = glob.glob(pattern+'/ttDM*/*/*/'+'*.lhe')

    jobList = 'joblist.txt'
    if ttDilep:
        jobList = 'joblist_dilep.txt'

    jobs = open(jobList, 'w')
    nChunks = 0
    for f in filelist:
        print f
        nEvents = getNEvents(f)
        EventsPerJob = min(nEvents,100000)
        nJobs = nEvents / EventsPerJob
        
        for i in range(0, nJobs):
            print i
            createJobs(f,jobs,i,EventsPerJob, outfolder, ttDilep)
            nChunks = nChunks+1

    jobs.close()
    print "default submission is for PSI, if you want to run on the NAF ad -naf to input arguments"
    submit = raw_input("Do you also want to submit the jobs to the batch system? [y/n] ")
    if submit == 'y' or submit=='Y':
        submitJobs(jobList,nChunks, outfolder, batchSystem)
    else:
        print "Not submitting jobs"


    
