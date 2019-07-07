import numpy
import root_numpy
import pandas, root_pandas   #datasets which are nicer.
from root_pandas import read_root
from hep_ml import reweight
from matplotlib import pyplot as plt
from hep_ml.metrics_utils import ks_2samp_weighted


#draw function define (to check the weight results)
def draw_distributions(original, target, new_original_weights, splot_weights):
    hist1_settings = {'bins': 20, 'density': True, 'alpha': 0.7}
    plt.figure(figsize=[15, 7])
    for id, column in enumerate(used_branch, 1):
        xlim = numpy.percentile(numpy.hstack([target[column]]), [0.01, 99.99])
        plt.subplot(2, 3, id)
        plt.hist(original[column], weights=new_original_weights, range=xlim, **hist1_settings, label="MC(weighted)")
        plt.hist(target[column], weights=splot_weights,range=xlim, **hist1_settings,label="Data(splot)")
        handles,labels=plt.gca().get_legend_handles_labels()
        plt.legend(loc='best')
        plt.title(column)
        print('KS over ', column, ' = ', ks_2samp_weighted(original[column], target[column],weights1=new_original_weights, weights2=splot_weights))
    plt.savefig('compare_show.pdf')
    plt.show()




		
# the variables to reweight
used_branch = ['C_PT','C_Y','nSPDHits','Dp_M','pK_M']


#set up data sets
"""
root2reweight are the mc need to reweight
rootfixdata are the data to weight to
root2addweight usually is the denominator for efficiency estimation (e.g: total mc truth)
"""
#used root files
root2reweight = 'root/endlamdab2DpK.root'
rootfixdata = 'root/endSplot54t59Xibc.root'
root2addweight = 'root/aaaalamdab2DpK.root'
all_branch = root_numpy.list_branches(root2addweight,'DecayTree')

original = root_numpy.root2array(root2reweight, branches=used_branch)
target = root_numpy.root2array(rootfixdata, branches=used_branch)
used = root_numpy.root2array(root2addweight, branches=used_branch)

original = pandas.DataFrame(original)
target = pandas.DataFrame(target)
used = pandas.DataFrame(used)
used_tmp = read_root(root2addweight,columns=all_branch)


#set up the orignal weights (weights for the orignal file and the target files)
original_weights = numpy.ones(len(original))
tree01 = root_numpy.root2array('root/endSplot54t59Xibc.root', 'DecayTree')
target_weights = tree01['sig_sw']



#the reweight class also have the bins reweight functions (uncomment if needed)

##==============bins reweight!!!!!!!!!!!
#bins_reweighter = reweight.BinsReweighter(n_bins=25, n_neighs=1.)
#bins_reweighter.fit(original, target, original_weights, target_weights)
#
#bins_weights = bins_reweighter.predict_weights(original)
## validate reweighting rule on the test part comparing 1d projections
#draw_distributions(original, target, bins_weights, target_weights)



##====================gb reweighter reweight!!!
"""

the following set are used for the low statistic case
feel free to increase the n_estimators (number of trees) and min_samples_leaf (minimal number of evnts in the leaf) if you have enough statistics
usually set to be n_estimators = 200 , min_samples_leaf=1000 ; 

"""

reweighter = reweight.GBReweighter(n_estimators=70, learning_rate=0.1, max_depth=3, min_samples_leaf=100, gb_args={'subsample': 0.7})
reweighter.fit(original, target, original_weights, target_weights)

gb_weights_test = reweighter.predict_weights(original)
gb_weights_used = reweighter.predict_weights(used)
print(type(gb_weights_used))
#reweighting done

#show the weight results
#validate reweighting vars on the test part comparing 1d projections

draw_distributions(original, target, gb_weights_test, target_weights)


#saving weight to root

#root_numpy.array2root(used, root2addweight, treename='DecayTree', mode='update') 

weightfile = 'weight.root'
weighttree = 'DecayTree'
weightname = 'weight'
used_tmp[weightname]=gb_weights_used
used_tmp.to_root(weightfile,weighttree)


