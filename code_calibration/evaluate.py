import numpy as np
import pandas as pd
import argparse
from utils import compute_acc_tab, compute_nll_tab

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("eval_set_csv", type=str)
    parser.add_argument('--detectors', type=str, default="DMID,CoDE,D3,B-Free,DRCT,CO-SPY")
    opt = parser.parse_args()

    detectors = opt.detectors.split(',')

    tab_test = pd.read_csv(opt.eval_set_csv)
    if 'type' not in tab_test.columns:
        tab_test['type'] = tab_test['label']
    
    tab_test = tab_test.groupby(['src','type','label'])[detectors].mean().reset_index()
    res = pd.DataFrame({
        'bAcc': compute_acc_tab(tab_test, detectors),
        'NLL': compute_nll_tab(tab_test, detectors),
    })
    res.loc['AVG',:] = res.mean(0)
    print(res)
    
