#!/bin/tcsh
set BASEDIR = $CMSSW_BASE
cd ${BASEDIR}/src/
eval `scramv1 runtime -csh`
ls ${BASEDIR}/src/pyLHEtools/MGrun/$1
cd ${BASEDIR}/src/pyLHEtools/MGrun
./../../MG5_aMC_v2_5_5/bin/mg5_aMC ${BASEDIR}/pyLHEtools/MGrun/$1
