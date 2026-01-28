from brian2 import *
from parameters import *

import matplotlib.pyplot as plt
import numpy as np


from brian2 import ms

def spikegen_from_times(times):
    if len(times) == 0:
        return SpikeGeneratorGroup(1,
            indices=np.array([], dtype=int),
            times=np.array([])*ms
        )
    return SpikeGeneratorGroup(1, [0]*len(times), times)



start_scope()

defaultclock.dt = 0.1*ms


# -----------------------
# Model equations
# -----------------------
eqs = '''
# Local synaptic voltage
V = Vhold : volt

# NMDA gating traces (fast + slow exponentials triggered by presyn spikes)
dn_f/dt = -n_f/tau_f : 1
dn_s/dt = -n_s/tau_s : 1
g_nmda = I_f*n_f + I_s*n_s : 1


# Mg block and driving term
B = 1.0/(1.0 + exp(-0.062*(V/mV))*(Mg/3.57)) : 1
H = B*(V - Vr) : volt

# Calcium "current" through NMDA-R
I_NMDA = P0*G_NMDA*g_nmda*H : 1/second

open_frac = P0*g_nmda : 1

# Calcium concentration (relative to rest)
dCa/dt = I_NMDA - Ca/tau_Ca : 1

# Omega(Ca)
sig1 = exp(beta1*(Ca - alpha1))/(1 + exp(beta1*(Ca - alpha1))) : 1
sig2 = exp(beta2*(Ca - alpha2))/(1 + exp(beta2*(Ca - alpha2))) : 1
Omega = 0.25 + sig2 - 0.25*sig1 : 1



# eta(Ca)
tau_eta = P1/(P2 + Ca**P3) + P4 : second
eta = 1/tau_eta : 1/second

# Weight dynamics
W0 : 1 (constant)
Wnorm = W/W0 : 1
dW/dt = eta*(Omega - W) : 1
'''

syn = NeuronGroup(1, eqs, method='euler')

# -----------------------
# Event-driven updates
# -----------------------
pre_on = '''
n_f_post += 1
n_s_post += 1
'''



def run_protocol(pre_times, post_times, parameters, T=500*ms,params_override=None):

    start_scope()

    p = parameters
    if params_override:
        p.update(params_override)

    ns = dict(p)
    
    # Recreate syn INSIDE the scope
    syn = NeuronGroup(1, eqs, method='euler',namespace=ns)

    # reset/init
    syn.Ca = 0
    syn.W0  = 0.25
    syn.W = syn.W0

    #Ppre  = SpikeGeneratorGroup(1, [0]*len(pre_times), pre_times)
    #Ppost = SpikeGeneratorGroup(1, [0]*len(post_times), post_times)

    Ppre  = spikegen_from_times(pre_times)
    Ppost = spikegen_from_times(post_times)
    
    Spre = Synapses(Ppre, syn, on_pre=pre_on,namespace=ns)
    Spre.connect()

    Spost = Synapses(Ppost, syn,namespace=ns)
    Spost.connect()

    M = StateMonitor(syn, ['Wnorm', 'W', 'Ca', 'g_nmda', 'V','Omega'], record=True)

    # Explicit network avoids dependency warnings + empty monitors
    net = Network(syn, Ppre, Ppost, Spre, Spost, M)
    net.run(T)

    return M
    



