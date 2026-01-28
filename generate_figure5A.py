## how long should the model run in seconds:
model_runtime = 20
## this, parameter, step in the range of voltages to plot, controls
## the resolution, or smoothness of the curve
voltage_step = 1

from parameters.sets import single_neuron_stimulation_clamped
from models.shouval_clamped_voltage import *
from stimulation.protocols import precompute_pre_train_100_times

import pickle
import numpy as np
import matplotlib.pyplot as plt

i_pairs = [(0.25,0.75),(0.5,0.5),(0.75,0.25)]

V_vals = np.arange(-70, -5, voltage_step) * mV

plt.figure(figsize = (6,4))

for m, n in i_pairs:
    W_inf = []
    for Vi in V_vals:
        M = run_protocol(
            pre_times = precompute_pre_train_100_times(N=100)[0],
            post_times = precompute_pre_train_100_times(N=100)[1],
            parameters = single_neuron_stimulation_clamped(),
            T = model_runtime*second,
            params_override = {"Vhold": Vi,
                               "I_f": m,
                               "I_s": n}
        )
        Ca_max = float(np.max(M.Ca[0]))
        Om_max = float(np.max(M.Omega[0]))  # only if you record Omega
        print("V=", float(Vi/mV), "Ca_max=", Ca_max, "W_norm=", M.Wnorm[0][-1])
        print(Vi)
        W_inf.append(M.Wnorm[0][-1])
    plt.plot(V_vals/mV, W_inf,label=f"If = {m}")
    
plt.legend()
plt.xlim(-70, -10)
plt.ylim(0, 4)
plt.axhline(y=1.0,linestyle ="--",color = "#888A85")
plt.xlabel("Postsynaptic voltage (mV)")
plt.ylabel(r"$W_{final} / W_0$", rotation = 90 )
plt.savefig("produced_figures/5A.png")    
plt.close("all")
