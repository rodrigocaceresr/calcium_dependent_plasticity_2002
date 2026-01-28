## how long should the model run in seconds:
model_runtime = 4
## this, parameter, step in the frequencies to plot, controls
## the resolution, or smoothness of the curve
frequency_step = 0.5


from parameters.sets import extracellular_stimulation
from models.shouval_free_voltage import *
from stimulation.protocols import precompute_pre_train_based_on_frequency

import pickle
import numpy as np
import matplotlib.pyplot as plt

## list of frequencies to generate presynaptic times
f_vals = np.arange(0.5, 20, frequency_step)

## list for accumulating weights
W_inf = []
for f in f_vals:
    M = run_protocol(
        pre_times = precompute_pre_train_based_on_frequency(f),
        post_times = [],
        parameters = extracellular_stimulation(),
        T = model_runtime*second,
        params_override = {"s_value": 10*mV}
    )
    W_inf.append(M.Wnorm[0][-1])


plt.figure(figsize = (6,4))
plt.plot(f_vals,W_inf,color="blue")
plt.xlim(0, 20)
plt.ylim(0, 4)
plt.axhline(y=1.0,linestyle ="--",color = "#888A85")
plt.xlabel("Frequency (Hz)")
plt.ylabel(r"$W_{final} / W_0$", rotation = 90 )
plt.plot(f_vals, W_inf)
plt.savefig("produced_figures/3B_without_postsynaptic_contributions.png")
plt.close("all")
