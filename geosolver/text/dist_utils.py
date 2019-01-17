import numpy as np
from scipy.misc import logsumexp

__author__ = 'minjoon'

def log_normalize(distribution):
    log_sum_exp = logsumexp(distribution.values())
    normalized_distribution = {key: value - log_sum_exp for key, value in distribution.items()}
    # print distribution
    assert is_log_consistent(normalized_distribution)
    return normalized_distribution


def is_log_consistent(distribution, eps=0.01):
    sum_value = sum(np.exp(logp) for _, logp in distribution.items())
    return np.abs(1-sum_value) < eps


def log_add(distribution, key, logp):
    if key in distribution:
        distribution[key] = np.log(np.exp(distribution[key]) + np.exp(logp))
    else:
        distribution[key] = logp

def normalize(dist):
    s = sum(dist.values())
    new_dist = {}
    for key, prob in dist.items():
        new_dist[key] = prob/s
    return new_dist
