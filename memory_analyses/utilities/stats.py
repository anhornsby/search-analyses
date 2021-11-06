"""Statistics functions"""

import numpy as np
from scipy.stats import t, sem

def aic(ll, n, k):
    """
    Calculate the Akaike Information Critierion (AIC) of a model
    Lower = better

    Arguments:
        ll (float): Negative log likelihood
        n (int): Number of observations used to estimate the log likelihood
        k (int): Number of free parameters

    Returns:
        (float): Akaike Information Critierion
    """

    return 2. * k - 2. * ll

def bic(ll, n, k):
    """
    Calculate the Bayesian Information Criterion (BIC) of a model
    Assumes that ll is the log likelihood
    Lower = better

    Arguments:
        ll (float): Negative log likelihood
        n (int): Number of observations used to estimate the log likelihood
        k (int): Number of free parameters

    Returns:
        (float): The Bayesian Information Criterion
    """

    return k * np.log(n) - 2. * ll

def mean_confidence_interval(data, confidence=0.95):
    """
    Calculate the confidence interval of a mean
    
    Arguments:
        data (list): An array of values
        confidence (float): Confidence interval [0, 1]

    Returns:
        (float): The confidence interval of the mean
    """
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), sem(a)
    h = se * t.ppf((1 + confidence) / 2., n-1)
   
    return h
