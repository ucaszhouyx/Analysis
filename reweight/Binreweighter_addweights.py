
from ROOT import TFile, TH2D, TH1D, TCanvas, TLegend, TTree 
from array import array

import sys
import lhcbStyle



def add_1d_weight(weightfile, hist_name, target_file, tree_name, weightvar, weightname):
    cut = "1"
    weight_file = TFile(weightfile)
    h1 = weight_file.Get(hist_name)
    f1 = TFile(target_file,"update")
    t1 = f1.Get(tree_name)
    weight = array('d',[0])
    var1 = array('d',[0])
    t1.SetBranchAddress(weightvar, var1)
    branch = t1.Branch(weightname, weight, 'weight/D')
    entry = t1.GetEntries()
    a = 0
    for i in range(entry):
        t1.GetEntry(i)
        print(var1[0])
#        var1 = t2.GetBranch("Lc_PT").GetEntry(i)
        bin_num = h1.FindBin(var1[0])
# #       bin_num = h1.Fill(var1[0])
        print(bin_num)
        if bin_num ==1:
            a+=1
        weight[0] = h1.GetBinContent(bin_num) 
        print(weight[0])
        branch.Fill()
    print(a)
    t1.Write()
def test_1d_weight(weightfile, hist_name, target_file, tree_name, newfile, weightvar, weightname):
    cut = "1"
    weight_file = TFile(weightfile)
    h1 = weight_file.Get(hist_name)
    f1 = TFile(target_file)
    t1 = f1.Get(tree_name)
    f2 = TFile(newfile,"RECREATE")
    t2 = t1.CopyTree(cut)
    weight = array('d',[0])
    var1 = array('d',[0])
    t2.SetBranchAddress(weightvar, var1)
    branch = t2.Branch(weightname, weight, 'weight/D')
    entry = t2.GetEntries()
    a = 0
    for i in range(entry):
        t2.GetEntry(i)
        print(var1[0])
#        var1 = t2.GetBranch("Lc_PT").GetEntry(i)
        bin_num = h1.FindBin(var1[0])
# #       bin_num = h1.Fill(var1[0])
        print(bin_num)
        if bin_num ==1:
            a+=1
        weight[0] = h1.GetBinContent(bin_num) 
        print(weight[0])
        t2.Fill()
    print(a)
    f2.Write()
    f2.Close()
