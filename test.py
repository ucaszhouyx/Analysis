from calculator import sum_weight

filename ="/publicfs/ucas/user/zhouyx/root/ucas01_backups/xiccpplcpkpipi/2017/mc/rec/XiccppMC17_preselallweighted_tis.root"
treename="DecayTree"
cut1 = 2000 < newchain.LcK_P and 150000 > newchain.LcK_P

all_weight =sum_weight.sum_weights(filename,treename,cut)
#all_weightsqr =sum_weight.sum_weightsqr(filename,treename)
print(all_weight)
#print(all_weightsqr)
