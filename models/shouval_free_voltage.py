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
# EPSP traces (difference of exponentials)
dx_ep/dt = -x_ep/tau_ep1 : 1
dy_ep/dt = -y_ep/tau_ep2 : 1
epsp = (s/norm_ep)*(x_ep - y_ep) : volt
s : volt

# BPAP traces (sum of exponentials)
dp_f/dt = -p_f/tau_bs_f : 1
dp_s/dt = -p_s/tau_bs_s : 1
bpap = BPAP_peak*(I_bs_f*p_f + I_bs_s*p_s) : volt

# Local synaptic voltage
V = Vrest + epsp + bpap : volt

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
dW/dt = eta*(Omega -W) : 1
'''

syn = NeuronGroup(1, eqs, method='euler')

# -----------------------
# Event-driven updates
# -----------------------
pre_on = '''
x_ep_post += 1
y_ep_post += 1
n_f_post += 1
n_s_post += 1
'''

post_on = '''
p_f_post += 1
p_s_post += 1
'''



def run_protocol(pre_times, post_times, parameters,  T=500*ms,params_override=None):

    start_scope()

    p = parameters
    if params_override:
        p.update(params_override)

    ns = dict(p)
    
    # Recreate syn INSIDE the scope
    syn = NeuronGroup(1, eqs, method='euler',namespace=ns)
    syn.s = p["s_value"]

    # reset/init
    syn.x_ep = 0; syn.y_ep = 0
    syn.p_f = 0; syn.p_s = 0
    syn.n_f = 0; syn.n_s = 0
    syn.Ca = 0
    syn.W0  = 0.25
    syn.W = syn.W0

    
    #Ppre  = SpikeGeneratorGroup(1, [0]*len(pre_times), pre_times)
    #Ppost = SpikeGeneratorGroup(1, [0]*len(post_times), post_times)


    Ppre  = spikegen_from_times(pre_times)
    Ppost = spikegen_from_times(post_times)
    
    Spre = Synapses(Ppre, syn, on_pre=pre_on,namespace=ns)
    Spre.connect()

    Spost = Synapses(Ppost, syn, on_pre=post_on,namespace=ns)
    Spost.connect()
    Spost.delay = p["bpap_delay"]

    M = StateMonitor(syn, ['Wnorm', 'W', 'Ca', 'g_nmda', 'V'], record=True)

    # Explicit network avoids dependency warnings + empty monitors
    net = Network(syn, Ppre, Ppost, Spre, Spost, M)
    net.run(T)

    return M
    



