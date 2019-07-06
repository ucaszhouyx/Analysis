from ROOT import *

from math import sqrt, log
from array import array
import sys

'''
Evaluate the efficiency under different mass hypotheses, factorized into
    - Acceptance 
      (based on fiducial cuts, consider XiccPT weight)
    - Turbo and offline selections 
      (consider tracking correction and XiccPT weight, including pre-selections)
    - PID (PIDCalib weights, consider futher nSPD weight)
    - MVA1
    - MVA2
    - Trigger (L0 and Hlt1)
With mass weighted to 80 fs
'''

# Define variables 
mass = ["35", "36", "37"]
Nmass = len(mass)
Nstep = 6
# var[Nstep][Nmass]
Nbefore  = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]
Nbefore2 = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]
Npass    = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]
Npass2   = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]
Nfail    = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]
Nfail2   = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]
eff      = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]
err      = [ [ 0. for y in range(Nmass) ] for x in range(Nstep) ]

# Step 0: Acceptance is evaluated separately
step = 0
eff[step] = [ 0.942105263158, 0.928261459181, 0.924160346696]
err[step] = [ 0.00320194185349, 0.00212493115733, 0.003557503687]

# Input
f_mc = TFile("/home/xuao/workdir/Xiccp2LcKPi/ntuple/MC16/REC/Sim_AllWeights_MCDecayTree.root")
tree_mc = f_mc.Get("MCDecayTree")
f = TFile("/home/xuao/workdir/Xiccp2LcKPi/ntuple/MC16/REC/Sim_AllWeights_DecayTree.root")
tree = f.Get("DecayTree")

# MCDecayTree is used to evaluate Turbo eff
Nentries = tree_mc.GetEntries()
#Nentries = 50000
for ii in xrange(Nentries):
    tree_mc.GetEntry(ii)
    if ii%10000==0: print("{0} events processed...".format(ii))

    # Fiducial
    XiccPT = tree_mc.C_TRUEPT>4000 and tree_mc.C_TRUEPT<15000
    CY = 0.5*log((tree_mc.C_TRUEP_E+tree_mc.C_TRUEP_Z)/(tree_mc.C_TRUEP_E-tree_mc.C_TRUEP_Z))
    XiccY = CY>2.0 and CY<4.5
    if XiccPT and XiccY:
        # Step 1: Turbo and pre-selection
        step = 1
        for jj in range(Nmass):
            exec( "w = tree_mc.Tau80_weight*tree_mc.PT_weight*tree_mc.m{0}_weight".format(mass[jj]) )
            Nbefore[step][jj]  += w
            Nbefore2[step][jj] += w**2

# DecayTree is used in the rest steps
Nentries = tree.GetEntries()
#Nentries = 10000
for ii in xrange(Nentries):
    tree.GetEntry(ii)
    if ii%5000==0: print("{0} events processed...".format(ii))

    # Fiducial
    XiccPT = tree.C_TRUEPT>4000 and tree.C_TRUEPT<15000
    CY = 0.5*log((tree.C_TRUEP_E+tree.C_TRUEP_Z)/(tree.C_TRUEP_E-tree.C_TRUEP_Z))
    XiccY = CY>2.0 and CY<4.5
    if XiccPT and XiccY:
        for jj in range(Nmass):
            # Step 1: Turbo and pre-selection
            step = 1
            pre1 = log(tree.C_IPCHI2_OWNPV)<4.0 and (tree.C_ENDVERTEX_CHI2/tree.C_ENDVERTEX_NDOF<10.0) and tree.C_PVFit1_chi2[0]<50.0 and tree.C_PT>4000.0
            pre2 = 2000 < tree.LcK_P and 150000 > tree.LcK_P and 2000 < tree.LcP_P and 150000 > tree.LcP_P and 2000 < tree.LcPi_P and 150000 > tree.LcPi_P and 2000 < tree.XiccK_P and 150000 > tree.XiccK_P and 2000 < tree.XiccPi_P and 150000 > tree.XiccPi_P
            pre3 = 1.5 < tree.LcP_ETA and 5 > tree.LcP_ETA and 1.5 < tree.LcPi_ETA and 5 > tree.LcPi_ETA and 1.5 < tree.LcK_ETA and 5 > tree.LcK_ETA and 1.5 < tree.XiccK_ETA and 5 > tree.XiccK_ETA and 1.5 < tree.XiccPi_ETA and 5 > tree.XiccPi_ETA
            if (pre1 and pre2 and pre3):
                exec( "w = tree.Tau80_weight*tree.PT_weight*tree.SPD_weight*tree.Evt_Track_eff*tree.m{0}_weight".format(mass[jj]) )
                Npass[step][jj]  += w
                Npass2[step][jj] += w**2
                # Step 2: PID
                step = 2
                w = w*tree.Evt_PIDCalib_eff
                Npass[step][jj]  += w
                Npass2[step][jj] += w**2
                # Step 3: MVA1
                step = 3
                BDTG1 = tree.BDTG>0.0
                if BDTG1:
                    Npass[step][jj]  += w
                    Npass2[step][jj] += w**2
                    # Step 4: MVA2
                    step = 4
                    BDTG2 = tree.BDTG2>0.7
                    if BDTG2:
                        Npass[step][jj]  += w
                        Npass2[step][jj] += w**2
                        # Step 5: Trigger
                        step = 5
                        L0 = tree.Lc_L0HadronDecision_TOS
                        Hlt1 = tree.Lc_Hlt1TrackMVADecision_TOS or tree.Lc_Hlt1TwoTrackMVADecision_TOS
                        if (L0 and Hlt1):
                            Npass[step][jj]  += w
                            Npass2[step][jj] += w**2

# Print
for ii in range(Nstep):
    if ii==0: continue
    for jj in range(Nmass):
        if ii==1:
            Nfail[ii][jj]  = Nbefore[ii][jj]  - Npass[ii][jj]
            Nfail2[ii][jj] = Nbefore2[ii][jj] - Npass2[ii][jj]
        else:
            Nbefore[ii][jj]  = Npass[ii-1][jj]
            Nbefore2[ii][jj] = Npass2[ii-1][jj]
            Nfail[ii][jj]  = Nbefore[ii][jj]  - Npass[ii][jj]
            Nfail2[ii][jj] = Nbefore2[ii][jj] - Npass2[ii][jj]
        
        eff[ii][jj] = Npass[ii][jj]/Nbefore[ii][jj]
        err[ii][jj] = sqrt( Nfail[ii][jj]**2*Npass2[ii][jj]+Npass[ii][jj]**2*Nfail2[ii][jj] )/Nbefore[ii][jj]**2

# Total eff. Take Acc. and the rest as independent
eff_tot = [0. for x in range(Nmass)]
err_tot = [0. for x in range(Nmass)]
eff_par = [0. for x in range(Nmass)]
err_par = [0. for x in range(Nmass)]
Npass_par   = [0. for x in range(Nmass)]
Nbefore_par = [0. for x in range(Nmass)]
for jj in range(Nmass):
    # Eff without Acc.
    Npass_par[jj]   = Npass[Nstep-1][jj]
    Nbefore_par[jj] = Nbefore[1][jj]
    eff_par[jj] = Npass_par[jj]/Nbefore_par[jj]
    err_par[jj] = sqrt(1.*Npass_par[jj]/Nbefore_par[jj]**2 * (1-1.*Npass_par[jj]/Nbefore_par[jj]))

    eff_tot[jj] = eff[0][jj]*eff_par[jj]
    err_tot[jj] = sqrt( (err_par[jj]**2)*(eff[0][jj]**2)+(err[0][jj]**2)*(eff_par[jj]**2) )

    print("Total efficiency = {:.3e} +/- {:.3e}".format(eff_tot[jj],err_tot[jj]))

str_step = ["Acc.", "Turbo", "PID", "MVA1", "MVA2", "Trigger"]
with open("Efficiency_VaryMass.tex", "w") as f:
    f.write("\\begin{table} \n")
    f.write("\\centering \n")
    f.write("\\begin{tabular}{clll} \n")
    f.write("\\toprule[1pt] \n")
    f.write("Items [\%] & $m(\\Xi_{{cc}})={0}18$ MeV & $m(\\Xi_{{cc}})={1}21$ MeV & $m(\\Xi_{{cc}})={2}00$ MeV \\\\ \n".format(mass[0],mass[1],mass[2]))
    f.write("\\midrule[1pt] \n")
    for ii in range(Nstep):
        line = "{0}".format(str_step[ii])
        for jj in range(Nmass):
            line += "& {:.3f} $\\pm$ {:.3f}".format(eff[ii][jj]*100,err[ii][jj]*100)
        line += "\\\\ \n"
        f.write(line)
    f.write("\\midrule[1pt] \n")
    f.write("Total & {:.3f} $\\pm$ {:.3f} & {:.3f} $\\pm$ {:.3f} & {:.3f} $\\pm$ {:.3f} \\\\ \n".format(eff_tot[0]*100,err_tot[0]*100,eff_tot[1]*100,err_tot[1]*100,eff_tot[2]*100,err_tot[2]*100))
    f.write("\\bottomrule[1pt] \n")
    f.write("\\end{tabular} \n")
    f.write("\\end{table}")

# Print
with open("Efficiency_VaryMass.py","w") as f:
    f.write("eff_tot = [ ")
    for ii in range(Nmass):
        print("Efficiency = {:.5f} +/- {:.5f}".format(eff_tot[ii],err_tot[ii]))
        f.write("{0}".format(eff_tot[ii]))
        if ii+1 != Nmass: f.write(", ")
    f.write("]\n")
    f.write("err_tot = [ ")
    for ii in range(Nmass):
        f.write("{0}".format(err_tot[ii]))
        if ii+1 != Nmass: f.write(", ")
    f.write("]\n")
