import numpy as np
import pandas as pd
from utils import gaussian_fitting, trasform_dict
import argparse
import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_set_csv", type=str)
    parser.add_argument("--output_csv", type=str)
    parser.add_argument("--fitting", type=str,  default="linear", choices=['linear', 'square'])
    parser.add_argument("--quality_score", type=str, default="IQA_LoDa")
    parser.add_argument('--detectors', type=str, default="DMID,CoDE,D3,B-Free,DRCT,CO-SPY")
    opt = parser.parse_args()

    quality_scores = opt.quality_score.split(',')
    detectors = opt.detectors.split(',')
    trasform_feats = trasform_dict[opt.fitting]

    tab_all = pd.read_csv(opt.eval_set_csv)
    if 'type' not in tab_all.columns:
        tab_all['type'] = tab_all['label']
    tab_weights = tab_all.groupby(['src','type','label'])[quality_scores[0]].count().reset_index()
    tab_weights['weight'] = 1.0/tab_weights[quality_scores[0]]
    num_cases = len(tab_weights)
    tab_weights['leaveoneout'] = np.arange(num_cases)

    tab_all = tab_all.merge(tab_weights[['src','type','label','weight','leaveoneout']])

    tab_fit = list()
    for index in tqdm.tqdm(range(num_cases)):
        tab_train = tab_all[tab_all['leaveoneout']!=index]
        tab_test  = tab_all[tab_all['leaveoneout']==index].copy()

        ## fitting
        tab_train0 = tab_train[tab_train['label']=='REAL']
        tab_train1 = tab_train[tab_train['label']=='FAKE']

        feats0  = tab_train0[quality_scores ].values
        feats1  = tab_train1[quality_scores ].values
        ref0    = tab_train0[detectors].values
        ref1    = tab_train1[detectors].values
        weight0 = tab_train0['weight'].values
        weight1 = tab_train1['weight'].values
        
        _, normalization = trasform_feats(np.concatenate((feats0,feats1),0))
        feats0, _ = trasform_feats(feats0, normalization)
        feats1, _ = trasform_feats(feats1, normalization)

        p0, s0 = gaussian_fitting(feats0, ref0, weight0)
        p1, s1 = gaussian_fitting(feats1, ref1, weight1)

        ## calibration
        test_feats = tab_test[quality_scores].values
        test_ref   = tab_test[detectors].values
        test_feats, _ = trasform_feats(test_feats, normalization)

        test_res = 0.5* (+(test_ref-test_feats @ p0)**2 / np.exp(test_feats @ s0) + (test_feats @ s0) \
                         -(test_ref-test_feats @ p1)**2 / np.exp(test_feats @ s1) - (test_feats @ s1))
        tab_test.loc[:,detectors] = test_res
        tab_fit.append(tab_test)
    
    tab_fit = pd.concat(tab_fit)
    tab_fit.to_csv(opt.output_csv, index=False)
    