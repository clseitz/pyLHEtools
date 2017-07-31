#!/usr/bin/env python
import os, glob, sys
#locatin /nfs/dust/cms/user/clseitz/DarkMatterMC/LHEfiles/
def createJobs(f , jobs, outfolder):
    cmd = 'python readFWliteGEN.py ' + f + ' ' + outfolder + '\n'
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
if __name__ == "__main__":

    infolder = ''
    outfolder = 'output'
    ## remove '-b' option
    if len(sys.argv) == 2:
        infolder = sys.argv[1]
        print 'Reading files from:', infolder, " Writing output to:", outfolder
    if len(sys.argv) > 2:
        infolder = sys.argv[1]
        outfolder = sys.argv[2]
        print 'Reading files from:', infolder, " Writing output to:", outfolder
    else:
        print "No input folder given"
        exit(0)
        
    try: os.stat(outfolder) 
    except: os.mkdir(outfolder)
    try: os.stat(outfolder+'/logs') 
    except: os.mkdir(outfolder+'/logs')
    
#    pattern = "datacardsABCD_2p1bins_fullscan2"
    filelist = glob.glob(infolder+'/*GEN'+'*.root')
    jobList = 'joblist.txt'
    jobs = open(jobList, 'w')
    for f in filelist:
        print f
        createJobs(f,jobs, outfolder)
  
    submit = raw_input("Do you also want to submit the jobs to the batch system? [y/n] ")
    if submit == 'y' or submit=='Y':
        submitJobs(jobList,len(filelist))
    else:
        print "Not submitting jobs"
        
    jobs.close()

    
