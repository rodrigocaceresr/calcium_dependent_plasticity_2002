## how long should the model run in seconds:
## 100s will take a long time but captures better the final synaptic weight
## and replicates better the plot of the paper
model_runtime = 0.5

from parameters.sets import single_neuron_stimulation
from models.shouval_free_voltage import *
from stimulation.protocols import precompute_stdp_times


import numpy as np
from brian2 import second, ms


### stimulation rate
freqs = [1.0,5.0,10]


dts = np.arange(-100, 150, 5) * ms  
plt.figure(figsize = (6,4))

for f in freqs:
    W_final = []
    for dt in dts:
        pre_times,post_times = precompute_stdp_times(dt,
                                                     n_pairs=100,
                                                     freq=f)
        T = model_runtime*second
        M = run_protocol(pre_times,
                         post_times,
                         T=T,
                         parameters = single_neuron_stimulation(),
                         params_override={"s_value": 1*mV})
        W_final.append(M.Wnorm[0][-1])  # or M.W[0][-1]/M.W0[0]
        print("dt=", float(dt/ms), "W_norm=", M.Wnorm[0][-1])
    plt.plot(dts/ms,W_final,label=rf"$f = {f}  Hz$")



plt.legend()
plt.xlim(-100, 150)
plt.ylim(0.25, 2.75)
plt.axhline(y=1.0,linestyle ="--",color = "#888A85")
plt.xlabel(r"$\Delta$ t (ms)")
plt.ylabel(r"$W_{final} / W_0$", rotation = 90 )
plt.savefig("produced_figures/4B.png")
plt.close("all")

