from ROOT import *
from math import acos

gROOT.ProcessLine(".x ~/lhcbStyle.C")

mp,mk,mh=938.3, 493.7,139.6
mLc=2286.46
tbkg1 = TChain("DecayTree")
tbkg1.Add("XiccRec.root")
total_entries = tbkg1.GetEntries()


nfile = TFile( "MC_removeClone.root" ,"recreate")
newtree = tbkg1.CloneTree(0)


drad = 0.5/1000.
#for tbkg1 in tbkg1:
for jentry in xrange(total_entries):
    tbkg1.GetEntry(jentry)
    #if tbkg1.KmHpHmMLP<0.94:continue
    if abs(tbkg1.C_PVFit1_Lambda_cplus_M[0]-2288) > 18: continue
    #if tbkg1.LcP_ProbNNghost>0.3 or tbkg1.LcPi_ProbNNghost>0.3 or tbkg1.LcK_ProbNNghost>0.3 or tbkg1.XiccK_ProbNNghost>0.3 or tbkg1.XiccPi1_ProbNNghost>0.3 or tbkg1.XiccPi2_ProbNNghost>0.3:continue

    vpXi=[ 
         TVector3(tbkg1.XiccPi1_PX,tbkg1.XiccPi1_PY,tbkg1.XiccPi1_PZ),
            TVector3(tbkg1.XiccPi2_PX,tbkg1.XiccPi2_PY,tbkg1.XiccPi2_PZ) 
         ]
    vpLc=[ TVector3(tbkg1.LcP_PX,tbkg1.LcP_PY,tbkg1.LcP_PZ),
            TVector3(tbkg1.LcPi_PX,tbkg1.LcPi_PY,tbkg1.LcPi_PZ),
            ]
    vmXi=[ 
            TVector3(tbkg1.XiccK_PX,tbkg1.XiccK_PY,tbkg1.XiccK_PZ),
            ]
    vmLc=[ 
            TVector3(tbkg1.LcK_PX,tbkg1.LcK_PY,tbkg1.LcK_PZ) 
            ]
    for vv in vpXi+vpLc+vmXi+vmLc:
        vv *= 1./vv.Mag()


    clone = 0
    if acos(vpXi[0].Dot(vpXi[1])) < drad:
        clone = 1
    if acos(vpLc[0].Dot(vpLc[1])) < drad:
        clone = 1
    for vv in vpXi:
        for ww in vpLc:
            if acos(vv.Dot(ww)) < drad:
                clone = 1; continue
    for vv in vmXi:
        for ww in vmLc:
            if acos(vv.Dot(ww)) < drad:
                clone = 1; continue
    if not clone: newtree.Fill()

#print "Before (all mass): ",tbkg1.GetEntries("KmHpHmMLP>0.94&&abs(C_PVFit1_Lambda_cplus_M[0]-2288)<18")
print "Before (all mass): ",tbkg1.GetEntries()
print "After  (all mass): ",newtree.GetEntries()

newtree.Write()

