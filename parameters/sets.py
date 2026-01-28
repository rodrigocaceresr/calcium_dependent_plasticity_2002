from brian2 import *

def single_neuron_stimulation():
    return dict(
        Vrest = -65*mV,
        Vr = 130*mV,
        
        Mg = 1.0,  # [Mg] = 1 (dimensionless here, consistent with paper formula)
        
        # EPSP kernel
        tau_ep1 = 50*ms,
        tau_ep2 = 5*ms,
        norm_ep = 0.6968373144130144,  # for (tau_ep1=50ms, tau_ep2=5ms)
        
        # BPAP kernel
        tau_bs_f = 3*ms,
        tau_bs_s = 25*ms,
        
        I_bs_f = 0.75,
        I_bs_s = 0.25,
        
        BPAP_peak = 100*mV,
        bpap_delay = 2*ms,
        
        # NMDA gate kernel
        # If paper does not specify, start with 0.5/0.5
        I_f = 0.5,
        I_s = 0.5,
        # You MUST set these to the paper’s values if you find them
        tau_f = 50*ms,
        tau_s = 200*ms,
        
        # Calcium dynamics
        P0 = 0.5,
        G_NMDA = (-1/500) / (ms*mV),  # [uM/(ms*mV)] implemented as 1/(ms*mV)
        tau_Ca = 50*ms,
        s_value = 1*mV,
        
        # Omega(Ca)
        alpha1 =  0.35,
        alpha2 = 0.55,
        beta1 = 80.0,
        beta2 = 80.0,
        
        # eta(Ca)
        P1 = 0.1*second,
        P2 = 1e-4,
        P3 = 3.0,
        P4 = 1*second,
    )


##### TODO: Remove parameters that are not used in clamped protocol
def single_neuron_stimulation_clamped():
    return dict(
        ##Vrest = -65*mV,
        Vr = 130*mV,
        Vhold = -40*mV,
        
        Mg = 1.0,  # [Mg] = 1 (dimensionless here, consistent with paper formula)
        
        # EPSP kernel
        ##tau_ep1 = 50*ms,
        ##tau_ep2 = 5*ms,
        ##norm_ep = 0.6968373144130144,  # for (tau_ep1=50ms, tau_ep2=5ms)
        
        # BPAP kernel
        ##tau_bs_f = 3*ms,
        tau_bs_s = 25*ms,
        
        ##I_bs_f = 0.75,
        ##I_bs_s = 0.25,
        
        ##BPAP_peak = 100*mV,
        ##bpap_delay = 2*ms,
        
        # NMDA gate kernel
        # If paper does not specify, start with 0.5/0.5
        I_f = 0.5,
        I_s = 0.5,
        # You MUST set these to the paper’s values if you find them
        tau_f = 50*ms,
        tau_s = 200*ms,
        
        # Calcium dynamics
        P0 = 0.5,
        G_NMDA = (-1/500) / (ms*mV),  # [uM/(ms*mV)] implemented as 1/(ms*mV)
        tau_Ca = 50*ms,
        s_value = 1*mV,
        
        # Omega(Ca)
        alpha1 =  0.35,
        alpha2 = 0.55,
        beta1 = 80.0,
        beta2 = 80.0,
        
        # eta(Ca)
        P1 = 0.1*second,
        P2 = 1e-4,
        P3 = 3.0,
        P4 = 1*second,
    )


def extracellular_stimulation():
    return dict(
        Vrest = -65*mV,
        Vr = 130*mV,
        Vhold = -40*mV,
        
        Mg = 1.0,  # [Mg] = 1 (dimensionless here, consistent with paper formula)
           
        # EPSP kernel
        tau_ep1 = 50*ms,
        tau_ep2 = 5*ms,
        norm_ep = 0.6968373144130144,  # for (tau_ep1=50ms, tau_ep2=5ms)
        
        # BPAP kernel
        tau_bs_f = 3*ms,
        tau_bs_s = 25*ms,
        
        I_bs_f = 0.75,
        I_bs_s = 0.25,
        
        BPAP_peak = 100*mV,
        bpap_delay = 2*ms,
        
        # NMDA gate kernel
        # If paper does not specify, start with 0.5/0.5
        I_f = 0.5,
        I_s = 0.5,
        # You MUST set these to the paper’s values if you find them
        tau_f = 50*ms,
        tau_s = 200*ms,
        
        # Calcium dynamics
        P0 = 0.5,
        G_NMDA = (-1/500) / (ms*mV),  # [uM/(ms*mV)] implemented as 1/(ms*mV)
        tau_Ca = 50*ms,
        s_value = 10*mV,
        
        # Omega(Ca)
        alpha1 =  0.35,
        alpha2 = 0.55,
        beta1 = 80.0,
        beta2 = 80.0,
        
        # eta(Ca)
        P1 = 0.1*second,
        P2 = 1e-4,
        P3 = 3.0,
        P4 = 1*second,
    )
