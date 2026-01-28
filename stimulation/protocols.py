from brian2 import *

def precompute_pre_train_100_times(N = 100):
    pre  = [k*second for k in range(N)]
    post = []
    return [pre,post]


def precompute_pre_train_based_on_frequency(f_Hz, N=900, t0=0.0):
    isi = 1.0 / f_Hz
    return [(t0 + k*isi) * second for k in range(N)]


def precompute_stdp_times(delta_t, n_pairs=100, freq=1.0, t0=0.5*second):
    """
    delta_t: Brian2 time (e.g. 10*ms or -20*ms)
    """
    isi = (1.0/freq) * second  # 1 Hz -> 1 second
    pre_times  = [t0 + k*isi for k in range(n_pairs)]
    post_times = [t + delta_t for t in pre_times]
    return pre_times, post_times
