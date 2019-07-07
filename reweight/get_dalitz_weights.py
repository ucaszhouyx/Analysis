from ROOT import *
from array import array

import sys
import lhcbStyle
lhcbStyle.lhcbStyle.SetPadTopMargin(0.08)
lhcbStyle.lhcbStyle.SetPadRightMargin(0.15)

gROOT.SetBatch(True)

###
# Note: need to keep the selection of MC and data consistent
###
# MC
#cut = "nSPDHits<450 && Lc_TRUEPT<15000 && 0.5*log((Lc_TRUEP_E+Lc_TRUEP_Z)/(Lc_TRUEP_E-Lc_TRUEP_Z))>2.0 && 0.5*log((Lc_TRUEP_E+Lc_TRUEP_Z)/(Lc_TRUEP_E-Lc_TRUEP_Z))<4.5"
cut = " 2000 < LcK_P && 150000 > LcK_P && 2000 < LcP_P && 150000 > LcP_P && 2000 < LcPi_P && 150000 > LcPi_P"
cut += " && 1.5 < LcP_ETA && 5 > LcP_ETA && 1.5 < LcPi_ETA && 5 > LcPi_ETA && 1.5 < LcK_ETA && 5 > LcK_ETA"
#cut += "&& BDTG>0.0"
#cut += "&& Lc_L0HadronDecision_TOS"
cut += "&&(Lc_Hlt1TrackMVADecision_TOS || Lc_Hlt1TwoTrackMVADecision_TOS)"
#cut = "1"
#weight = "Evt_Track_eff*Evt_PIDCalib_eff"
weight = "Pt_weight"
f1 = TFile("mc_allcut.root")
t1 = f1.Get("DecayTree")
nbins = 10
xlow, xup = 600, 1400
ylow, yup = 1400, 2200
h1 = TH2D("h1","h1", nbins, xlow, xup, nbins, ylow, yup)
h1.Sumw2()
varexp = "sqrt((LcP_PE+LcK_PE)*(LcP_PE+LcK_PE)-(LcP_PX+LcK_PX)*(LcP_PX+LcK_PX)-(LcP_PY+LcK_PY)*(LcP_PY+LcK_PY)-(LcP_PZ+LcK_PZ)*(LcP_PZ+LcK_PZ)) : sqrt((LcPi_PE+LcK_PE)*(LcPi_PE+LcK_PE)-(LcPi_PX+LcK_PX)*(LcPi_PX+LcK_PX)-(LcPi_PY+LcK_PY)*(LcPi_PY+LcK_PY)-(LcPi_PZ+LcK_PZ)*(LcPi_PZ+LcK_PZ))"
t1.Project("h1",varexp,"({0})*{1}".format(cut,weight))
h1.Scale(1./h1.Integral())
# Data
f2 = TFile("sPlot_L0all.root")
t2 = f2.Get("DecayTree")
h2 = TH2D("h2","h2", nbins, xlow, xup, nbins, ylow, yup)
h2.Sumw2()
cut = "1"
weight = "sig_sw"
varexp = "sqrt((LcP_PE+LcK_PE)*(LcP_PE+LcK_PE)-(LcP_PX+LcK_PX)*(LcP_PX+LcK_PX)-(LcP_PY+LcK_PY)*(LcP_PY+LcK_PY)-(LcP_PZ+LcK_PZ)*(LcP_PZ+LcK_PZ)) : sqrt((LcPi_PE+LcK_PE)*(LcPi_PE+LcK_PE)-(LcPi_PX+LcK_PX)*(LcPi_PX+LcK_PX)-(LcPi_PY+LcK_PY)*(LcPi_PY+LcK_PY)-(LcPi_PZ+LcK_PZ)*(LcPi_PZ+LcK_PZ))"
t2.Project("h2",varexp,"({0})*{1}".format(cut,weight))
h2.Scale(1./h2.Integral())

# weight
fw = TFile("Dalitz_weight.root","RECREATE")
hw = TH2D("hw","hw",nbins,xlow,xup,nbins,ylow,yup)
# upstair / downstair = data / MC
hw.Divide(h2,h1,1,1,"B")

# Draw
c1 = TCanvas("c1","c1")
hw.Draw("COL Z TEXT")
hw.SetXTitle("m(K#pi)")
hw.SetYTitle("m(pK)")
c1.SaveAs("Dalitz_weight.pdf")
# Print
for i in range(nbins):
    for j in range(nbins):
        print(hw.GetBinContent(i+1,j+1))
hw.Write()

