import numpy as np
import pandas as pd
from utils import gaussian_fitting, trasform_dict
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev_set_csv", type=str)
    parser.add_argument("--eval_set_csv", type=str)
    parser.add_argument("--output_csv", type=str)
    parser.add_argument("--fitting", type=str,  default="linear", choices=['linear', 'square'])
    parser.add_argument("--quality_score", type=str, default="IQA_LoDa")
    parser.add_argument('--detectors', type=str, default="DMID,CoDE,D3,B-Free,DRCT,CO-SPY")
    opt = parser.parse_args()

    quality_scores = opt.quality_score.split(',')
    detectors = opt.detectors.split(',')
    trasform_feats = trasform_dict[opt.fitting]

    ## fitting
    tab_train = pd.read_csv(opt.dev_set_csv)
    if 'type' not in tab_train.columns:
        tab_train['type'] = tab_train['label']
    assert 'weight' not in tab_train.columns
    tab_weights = tab_train.groupby(['src','type','label'])[quality_scores[0]].count().reset_index()
    tab_weights['weight'] = 1.0/tab_weights[quality_scores[0]]
    tab_train = tab_train.merge(tab_weights[['src','type','label','weight']])

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

    #data = {'quality_scores':quality_scores, 'detectors': detectors, 'normalization': normalization, 'p0': p0, 'p1': p1, 's0': s0, 's1': s1})

    ## calibration
    tab_test = pd.read_csv(opt.eval_set_csv)
    test_feats = tab_test[quality_scores].values
    test_ref   = tab_test[detectors].values
    test_feats, _ = trasform_feats(test_feats, normalization)

    tab_fit = tab_test.copy()
    test_res = 0.5* (+(test_ref-test_feats @ p0)**2 / np.exp(test_feats @ s0) + (test_feats @ s0) \
                     -(test_ref-test_feats @ p1)**2 / np.exp(test_feats @ s1) - (test_feats @ s1))
    tab_fit.loc[:,detectors] = test_res
    tab_fit.to_csv(opt.output_csv, index=False)
    
