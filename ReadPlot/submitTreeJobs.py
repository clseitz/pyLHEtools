#!/usr/bin/env python
import os, glob, sys
#locatin /nfs/dust/cms/user/clseitz/DarkMatterMC/LHEfiles/
def createJobs(f , jobs):
    cmd = 'python readFWliteGEN.py ' + f + '\n'
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

    ## remove '-b' option
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
        print '# pattern is', pattern
    else:
        print "No pattern given!"
        exit(0)
        
    try: os.stat('logs') 
    except: os.mkdir('logs')
    
#    pattern = "datacardsABCD_2p1bins_fullscan2"
    filelist = glob.glob(pattern+'/*GEN'+'*.root')
    jobList = 'joblist.txt'
    jobs = open(jobList, 'w')
    for f in filelist:
        print f
        createJobs(f,jobs)
    submitJobs(jobList,len(filelist))
        
    jobs.close()

    
