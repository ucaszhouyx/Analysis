
from ROOT import TFile, TH2D, TH1D, TCanvas, TLegend 
from array import array

import sys
import lhcbStyle



def two_dimensional_weight(mcfile, fixdata, var2weight1, var2weight2, nbins, xmin, xmax, ymin, ymax, weightfile, weightplot, denominator_weight = None, numerator_weight= "sig_sw"):
#global settings

    lhcbStyle.lhcbStyle.SetPadTopMargin(0.08)
    lhcbStyle.lhcbStyle.SetPadRightMargin(0.15)
    weightvar = var2weight1 + ":" + var2weight2
    cut = "1"
#obtain mc histo
    f1 = TFile(mcfile)
    t1 = f1.Get("DecayTree")
    h1 = TH2D("h1","h1", nbins, xmin, xmax, nbins, ymin, ymax)
    h1.Sumw2() 
    print(denominator_weight)
    if denominator_weight is None:
      t1.Project("h1",weightvar,cut)
    else:
      t1.Project("h1",weightvar,"({0})*{1}".format(cut,denominator_weight))
    h1.Scale(1./h1.Integral())
#obtain data histo
    f2 = TFile(fixdata)
    t2 = f2.Get("DecayTree")
    h2 = TH2D("h2","h2", nbins, xmin, xmax, nbins, ymin, ymax)
    h2.Sumw2()
    t2.Project("h2",weightvar,"({0})*{1}".format(cut,numerator_weight))
    h2.Scale(1./h2.Integral())
#calculate weights
    fw = TFile(weightfile,"RECREATE")
    hw = TH2D("hw","hw",nbins,xmin,xmax,nbins,ymin,ymax)
    hw.Divide(h2,h1,1,1,"B")
#weight plot save
    c1 = TCanvas("c1","c1")
    hw.Draw("COL Z TEXT")
    hw.SetXTitle(var2weight1)
    hw.SetYTitle(var2weight2)
    c1.SaveAs(weightplot)
#save weight to root file
    hw.Write()
    
def one_dimensional_weight(mcfile, fixdata, var2weight, nbins, bin_scheme, weightfile, weightplot, numerator_weight = "sig_sw"):
#def one_dimensional_weight(mcfile, fixdata, var2weight, nbins, bin_scheme, weightfile, weightplot, denominator_weight = None, numerator_weight = "sig_sw"):
#global settings
    lhcbStyle.lhcbStyle.SetPadTopMargin(0.08)
    lhcbStyle.lhcbStyle.SetPadRightMargin(0.15)
    cut = "1"
#obtain mc data histo
    f1 = TFile(mcfile)
    t1 = f1.Get("DecayTree")
    f2 = TFile(fixdata)
    t2 = f2.Get("DecayTree")
    h1 = TH1D("h1","h1", nbins, bin_scheme)
    h2 = TH1D("h2","h2", nbins, bin_scheme)
    h1.Sumw2()
    h2.Sumw2()
    t1.Project("h1",var2weight,cut)
#    t1.Project("h1",var2weight,"({0})*{1}".format(cut,denominator_weight))
    t2.Project("h2",var2weight,"({0})*{1}".format(cut,numerator_weight))
    h1.Scale(1./h1.Integral())
    h2.Scale(1./h2.Integral())
#calculate weights
    fw = TFile(weightfile,"RECREATE")
    hw = TH1D("hw","hw", nbins, bin_scheme)
    hw.Divide(h2,h1,1,1,"B")
#weight plot save
    c1 = TCanvas("c1","c1")
   # h1.Draw("e")
   # h2.Draw("esame")
   # h1.SetLineColor(1)
   # h2.SetLineColor(4)
   # h1.SetXTitle(var2weight)
   # le1 = TLegend(0.6,0.7,0.80,0.9)
   # le1.AddEntry(h1,"MC","elp")
   # le1.AddEntry(h2,"data","elp")
   # le1.Draw("same")
    hw.Draw("e")
    c1.SaveAs(weightplot)
#save weight to root file
    hw.Write()

    
