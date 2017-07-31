#! /usr/bin/env python
#Script to remove unnecessary stuff in the Madgraph output

import sys, os, glob

run = True
if __name__ == "__main__":
    
    folder = ''
    if len(sys.argv) > 1:
        folder = sys.argv[1]
        print 'Looking at folder: ', folder
    else:
        print 'no folder name given'
        exit(0)
    
    files = dirList = glob.glob(folder+"/tt*")
    counter = 0
    for f in files:
        sub = f+'/SubProcesses/'
        cmd = 'cp ' + sub + 'results.dat ' + f + '/.'
        print cmd
        if run: os.system(cmd)

        folders = f+'/lib '+f+'/HTML ' + f+'/Source ' + f+'/bin'
        cmd = 'rm -fr ' + sub  + ' ' + folders
        print cmd
        if run: os.system(cmd)
        
        cmd =  'gunzip ' + f +'/Events/run_01/unweighted_events.lhe.gz'
        print cmd
        if run: os.system(cmd)
