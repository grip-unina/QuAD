import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import softplus

def nll_log(theta, X, y, weights):
    mu = X @ theta[:X.shape[1]]
    log_var = X @ theta[X.shape[1]:]
    log_var = np.clip(log_var, -30, 30)    # prevents overflow/underflow
    var = np.exp(log_var)
    return 0.5 * np.sum(weights * (log_var + (y - mu) ** 2 / var))

def nll_log_grad(theta, X, y, weights):
    mu = X @ theta[:X.shape[1]]
    log_var = X @ theta[X.shape[1]:]
    log_var = np.clip(log_var, -30, 30)    # prevents overflow/underflow
    var = np.exp(log_var)
    da = 0.5 * np.sum((-2 * ((y - mu)      / var)[:,None] * X) * weights[:,None],0) 
    db = 0.5 * np.sum(( X - ((y - mu) ** 2 / var)[:,None] * X) * weights[:,None],0) 
    return np.concatenate((da,db), 0)

def gaussian_fitting(X, y, weights):
    p0 = np.linalg.inv(X.T @ X) @ X.T @ y
    s0 = np.zeros_like(p0)
    s0[-1, :] = np.log(np.mean((y - X @ p0)**2, 0))

    for index in range(y.shape[1]):
        res = np.concatenate((p0[:,index], s0[:,index]), 0)
        res = minimize(nll_log, res, jac=nll_log_grad, args=(X, y[:,index], weights), method="BFGS", options={'gtol': 1e-4, 'disp': False})
        p0[:,index] = res.x[:X.shape[1]]
        s0[:,index] = res.x[X.shape[1]:]

    return p0, s0

def trasform_linear(x, normalization=None):
    if normalization is None:
        normalization = (np.mean(x, 0, keepdims=True), np.std(x, 0, keepdims=True))
    x = (x - normalization[0]) / normalization[1]
    x = np.concatenate((x, np.ones_like(x)[:,:1]), 1)
    return x, normalization

def trasform_square(x, normalization=None):
    if normalization is None:
        normalization = (np.mean(x, 0, keepdims=True), np.std(x, 0, keepdims=True))
    x = (x - normalization[0]) / normalization[1]
    x = np.concatenate((x, np.ones_like(x)[:,:1]), 1)
    x = np.concatenate([x[:,:_+1]*x[:,_:_+1] for _ in range(x.shape[1])], 1)
    return x, normalization

trasform_dict = {
    'linear' : trasform_linear,
    'square' : trasform_square,
}

def compute_mean_result(tab, detectors, func):
    tab0 = tab[tab['label']=='REAL'].copy()
    tab1 = tab[tab['label']=='FAKE'].copy()
    tab0[detectors] = -1.0*tab0[detectors]
    tab0[detectors] = tab0[detectors].apply(func)
    tab1[detectors] = tab1[detectors].apply(func)
    val0 = tab0.groupby('type')[detectors].mean().mean(0)
    val1 = tab1.groupby('type')[detectors].mean().mean(0)
    return (val0+val1)/2

def compute_acc_tab(tab, detectors):
    return compute_mean_result(tab, detectors, lambda x: x>0)

def compute_nll_tab(tab, detectors):
    return compute_mean_result(tab, detectors, lambda x: softplus(-1*x))
