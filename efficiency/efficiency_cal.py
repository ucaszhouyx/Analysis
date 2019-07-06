import os,sys


AbsolutePath = os.path.abspath(__file__)           #将相对路径转换成绝对路径

SuperiorCatalogue = os.path.dirname(AbsolutePath)   #相对路径的上级路径

BaseDir = os.path.dirname(SuperiorCatalogue)        #在“SuperiorCatalogue”的基础上在脱掉一层路径，得到我们想要的路径。

sys.path.insert(0,BaseDir)

import root_pandas
import numpy as np
import pandas as pd
from config import cut
import argparse
import math



def parse_args():
    parser = argparse.ArgumentParser()

    # create the parser for training a classifier
    parser.add_argument('--channel', default='Xicc')
    parser.add_argument('--dir', default='/home/baba/lhcb/python_pack/own/root/')
    args = parser.parse_args() 
    #eff_cal('presel',args.channel,args.dir)
    #denominator_cal(args.channel,args.dir)
    total_eff_table(args.channel,args.dir)


def denominator_cal(channel,dirname):
    filename = dirname + channel +'.root'
    before_df = root_pandas.read_root(filename,'MCDecayTree')
    before_sum_weight = before_df['sweight1'].sum()
    tmp_df = before_df['sweight1']**2
    before_sum_weightsqr = tmp_df.sum()
    print('total weight was ', before_sum_weight)
    print('befor weight square was ', before_sum_weightsqr)
    return before_sum_weight, before_sum_weightsqr

def eff_cal(steps,orignal_steps,channel,dirname):

    filename = dirname + channel +'.root'
    orignal_cuts = cut.get_mm_cuts(orignal_steps)

    if steps=='reco':
        before_sum_weight, before_sum_weightsqr = denominator_cal(channel,dirname)
        before_df_tmp = root_pandas.read_root(filename,'DecayTree')
        before_df = before_df_tmp.query(orignal_cuts)
    else:
        before_df_tmp = root_pandas.read_root(filename,'DecayTree')
        before_df = before_df_tmp.query(orignal_cuts)
        before_sum_weight = before_df['sweight'].sum()
        tmpbefore_df = before_df['sweight']**2
        before_sum_weightsqr = tmpbefore_df.sum()
    aftercuts = cut.get_mm_cuts(steps)
    after_df = before_df.query(aftercuts)
#    print(aftercuts)
    if steps =='pid':
        after_sum_weight = after_df['mweight'].sum()
        tmpafter_df = after_df['mweight']**2
        after_sum_weightsqr = tmpafter_df.sum()
    else:
       after_sum_weight = after_df['sweight'].sum()
       tmpafter_df = after_df['sweight']**2
       after_sum_weightsqr = tmpafter_df.sum()
    sel_eff = after_sum_weight/before_sum_weight
    eff_error_tmp =eff_error(before_sum_weight,after_sum_weight,before_sum_weightsqr,after_sum_weightsqr) 
    print('{0} efficiency was = {1} +/- {2}'.format(steps,sel_eff,eff_error_tmp))
#    print('{0} efficiency error was ={1}'.format(steps,sel_eff))

    return sel_eff, eff_error_tmp

def eff_error(num,de,num_sqr,de_sqr):
    tmp_num = (de-num)**2*num_sqr+num**2*de_sqr
    error = math.pow(tmp_num,.5)/((num+de)**2)
    return error
    
    
def total_eff_table(channel,dirname):
    steps =['tmp','reco','l0','hlt1','hlt2','pid','bdt','mass_veto'] 
    eff  = [ 0. for y in range(len(steps)-1) ]
    eff_err  = [ 0. for y in range(len(steps)-1) ]
 #   total_denominator = denominator_cal(channel,dirname)
    for ii in range(len(steps)-1):
      eff[ii],eff_err[ii] = eff_cal(steps[ii+1],steps[ii],channel,dirname)

    with open("Efficiency_test.tex", "w") as f:
        f.write("\\begin{table} \n")
        f.write("\\centering \n")
        f.write("\\begin{tabular}{clll} \n")
        f.write("\\toprule[1pt] \n")
        f.write("Steps  & efficiency [\%]  ")
        f.write("\\midrule[1pt] \n")
        for ii in range(len(steps)-1):
            line = "{0}".format(steps[ii+1])
            line += "& {:.3f} $\\pm$ {:.3f}".format(eff[ii]*100,eff_err[ii]*100)
            line += "\\\\ \n"
            f.write(line)
        f.write("\\midrule[1pt] \n")
        f.write("Total & -")
        f.write("\\bottomrule[1pt] \n")
        f.write("\\end{tabular} \n")
        f.write("\\end{table}")





if __name__ == '__main__':
    parse_args()
