import root_pandas
import numpy as np
import pandas as pd
#from cut import presel_cuts
from config import cut
#import config
import argparse



def parse_args():
    parser = argparse.ArgumentParser()

    # create the parser for training a classifier
    parser.add_argument('--channel', default='Xicc')
    parser.add_argument('--dir', default='/home/baba/lhcb/python_pack/own/')
    args = parser.parse_args() 
    preeff_cal(args.channel,args.dir)



def preeff_cal(channel,dirname):
    filename = dirname + channel +'.root'
    precuts = cut.presel_cuts(channel)
    #precuts = presel_cuts(channel)
    before_df = root_pandas.read_root(filename,'DecayTree')
    before_sum_weight = before_df['sweight'].sum()
    after_df = before_df.query(precuts)
    print(precuts)
    after_sum_weight = after_df['sweight'].sum()
    print('befor weight was ',before_sum_weight)
    print('after weight was ',after_sum_weight)
    return after_sum_weight/before_sum_weight







if __name__ == '__main__':
    parse_args()
