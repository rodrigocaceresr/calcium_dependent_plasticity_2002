## how long should the model run in seconds:
## 100s will take a long time but captures better the final synaptic weight
## and replicates better the plot of the paper
model_runtime = 100

from parameters.sets import single_neuron_stimulation
from models.shouval_free_voltage import *
from stimulation.protocols import precompute_stdp_times


import numpy as np
from brian2 import second, ms


### NMDA kinetic manipulations on the fast and slow components
i_pairs = [(0.25,0.75),(0.5,0.5),(0.75,0.25)]

dts = np.arange(-100, 200, 5) * ms  
plt.figure(figsize = (6,4))

for m, n in i_pairs:
    W_final = []
    for dt in dts:
        pre_times,post_times = precompute_stdp_times(dt,
                                                     n_pairs=100,
                                                     freq=1.0)
        T = model_runtime*second
        M = run_protocol(pre_times,
                         post_times,
                         T=T,
                         parameters = single_neuron_stimulation(),
                         params_override={"s_value": 1*mV,
                                          "I_f": m,
                                          "I_s": n})
        W_final.append(M.Wnorm[0][-1])  # or M.W[0][-1]/M.W0[0]
        print("dt=", float(dt/ms), "W_norm=", M.Wnorm[0][-1])
    plt.plot(dts/ms,W_final,label=rf"$I_{{f}} = {m}$")



plt.legend()
plt.xlim(-100, 200)
plt.ylim(0.25, 2.75)
plt.axhline(y=1.0,linestyle ="--",color = "#888A85")
plt.xlabel(r"$\Delta$ t (ms)")
plt.ylabel(r"$W_{final} / W_0$", rotation = 90 )
plt.savefig("produced_figures/5C.png")
plt.close("all")

