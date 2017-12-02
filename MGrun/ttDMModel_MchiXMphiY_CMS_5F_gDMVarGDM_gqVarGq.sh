set group_subprocesses Auto
set ignore_six_quark_processes False
set loop_optimized_output True
set complex_mass_scheme False
import model DMVarModel
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define l+ = e+ mu+
define l- = e- mu-
define vl = ve vm vt
define vl~ = ve~ vm~ vt~
define p = p b  b~
define j = j b  b~
generate p p > t t~ chi chi~ @0
add process  p p > t t~ chi chi~ j @1
output VarLocation/output_VarScenario_VarIseed/ttDMVarModel_MphiVarMphi_MchiVarMchi_gDMVarGDMstr_gqVarGqstr_VarIseed
launch
0
set Mphi VarMphi
set Mchi VarMchi
set gqq VarGq
set gDM VarGDM
set pdlabel lhapdf
set lhaid 263000 
set ebeam1 6500
set ebeam2 6500
set nevents Varnevents 
set iseed VarIseed
set maxjetflavor 5
set asrwgtflavor 5
set pdfwgt F
set ptj 0
set pta 0
set ptl 0
set etab 5
set etaa -1
set etal -1
set drll 0
set draa 0
set draj 0
set dral 0
set xqcut 20
set use_syst F
0