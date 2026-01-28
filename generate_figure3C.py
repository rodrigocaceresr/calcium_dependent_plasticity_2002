## how long should the model run in seconds:
model_runtime = 60

from parameters.sets import single_neuron_stimulation
from models.shouval_free_voltage import *
from stimulation.protocols import precompute_stdp_times


import numpy as np
from brian2 import second, ms

dts = np.arange(-100, 200, 5) * ms  

### accumulate final weight values for each iteration
W_final = []

for dt in dts:
    pre_times,post_times = precompute_stdp_times(dt,
                                        n_pairs=100,
                                        freq=1.0)
    T = model_runtime*second
    M = run_protocol(pre_times,
                     post_times,
                     parameters = single_neuron_stimulation(),
                     T=T,
                     params_override={"s_value": 1*mV})
    W_final.append(M.Wnorm[0][-1])  # or M.W[0][-1]/M.W0[0]
    print("dt=", float(dt/ms), "W_norm=", M.Wnorm[0][-1])

plt.figure(figsize = (6,4))
plt.plot(dts/ms, W_final[0:60],color="blue")
plt.xlim(-100, 200)
plt.ylim(0.25, 2.75)
plt.axhline(y=1.0,linestyle ="--",color = "#888A85")
plt.xlabel(r"$\Delta$ t (ms)")
plt.ylabel(r"$W_{final} / W_0$", rotation = 90 )
plt.savefig("produced_figures/3C.png")
plt.close("all")
    
