from ROOT import *

def sum_weights(filename,tree_name,cut):
    total_weights =0.
    newchain = TChain(tree_name)
    newchain.Add(filename)
    total_entries = newchain.GetEntries()
    for tmpentry in xrange(total_entries):
        newchain.GetEntry(tmpentry) 
        if(cut):
            total_weights+=newchain.sweight
    
    return total_weights



def sum_weightsqr(filename,tree_name):
    total_weightsqr=0.
    newchain = TChain(tree_name)
    newchain.Add(filename)
    total_entries = newchain.GetEntries()

    for tmpentry in xrange(total_entries):
        newchain.GetEntry(tmpentry) 
        total_weightsqr+=newchain.sweight*newchain.sweight
    
    return total_weightsqr
