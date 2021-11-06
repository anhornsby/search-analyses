"""Loss/error functions to be used during model estimation"""

import logging
import numpy as np

def _assert_values_between_0_and_1(values):
   
    try:
   
        assert(np.logical_and(np.round(values, 1) >= 0.0, np.round(values, 1) <= 1.1).all())
       
    except AssertionError:
        print(values)
        logging.info('Values not within 0-1 range: {0}'.format(values))
        raise

def negative_log_likelihood(likelihoods, replace_zero_with=0.00000001):
    """
    Calculate the negative log likelihood of an array
   
    Args:
        likelihoods (list): A list of model likelihoods
        replace_zero_with (float): Replace zero likelihoods with a very small number,
            to ensure that we don't take a log of 0
   
    Returns:
        (float): The total negative log-likelihood
    """

    # handle instances where 0 has been in the numerator or denominator
    likelihoods = np.nan_to_num(likelihoods, replace_zero_with, nan=0, neginf=0, posinf=1)

    # values should be between 0 and 1
    _assert_values_between_0_and_1(likelihoods)
   
    if replace_zero_with is not None:
        likelihoods[likelihoods <= replace_zero_with] = replace_zero_with
   
    # now calculate loss
    ll = np.log(likelihoods)
    negative_ll = -np.sum(ll)
   
    return negative_ll
