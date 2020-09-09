import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np

def plot_data(state_monitor, title=None):
    """Plots the state_monitor variable "vm" vs. time.

    Args:
        state_monitor (StateMonitor): the data to plot
        title (string, optional): plot title to display
    """

    fig, ax = plt.subplots(1, figsize=(10, 3))

    ax.plot(state_monitor.t / b2.ms, state_monitor.vm[0] / b2.mV, lw=2, c='k')

    ax.set_xlabel("t [ms]")
    ax.set_ylabel("v [mV]")
    plt.grid()

    plt.axis((
        0,
        np.max(state_monitor.t / b2.ms),
        -100, 50))

    if title is not None:
        ax.set_title(title)

    plt.tight_layout()

    plt.show();


import brian2 as b2
import matplotlib.pyplot as plt
import numpy as np


def simulate_HH_neuron(I_e, simulation_time):

    """A Hodgkin-Huxley neuron implemented in Brian2.

    Args:
        I_e: Input current injected into the HH neuron
        simulation_time (float): Simulation time [seconds]

    Returns:
        StateMonitor: Brian2 StateMonitor with recorded field "vm"
    """

    # neuron parameters
    El = -59. * b2.mV
    EK = -82. * b2.mV
    ENa = 45. * b2.mV
    gl = 0.3 * b2.msiemens
    gK = 36. * b2.msiemens
    gNa = 120. * b2.msiemens
    C = 1. * b2.ufarad

    # forming HH model with differential equations
    eqs = """
    membrane_Im = I_e + gNa*m**3*h*(ENa-vm) + \
        gl*(El-vm) + gK*n**4*(EK-vm) : amp
    
    alphan = 0.01/mV * (-60.0*mV - vm) / (exp((-60.0*mV - vm) / (10.0*mV)) - 1.0)/ms: Hz
    alpham = (vm + 45.0*mV) / (10.0*mV) / (1.0 - exp(-(vm + 45.0*mV) / (10.0*mV)))/ms : Hz
    alphah = 0.07*exp(-(vm + 70.*mV)/(20.*mV))/ms : Hz
    
    betan = 0.125 * exp(-(vm + 70.0*mV) / (80.0*mV))/ms: Hz
    betam = 4.0 * exp(-(vm + 70.0*mV) / (18.0*mV))/ms: Hz
    betah = 1. / (exp(-(vm + 40.0*mV) / (10.0*mV)) + 1.0)/ms : Hz
    
    dn/dt = alphan*(1-n)-betan*n : 1
    dm/dt = alpham*(1-m)-betam*m : 1
    dh/dt = alphah*(1-h)-betah*h : 1
    
    dvm/dt = membrane_Im/C : volt
    """
    
    neuron = b2.NeuronGroup(1, eqs, method="exponential_euler")

    # parameter initialization [come from x_inf(v) {x:m,n,h}]
    neuron.vm = -70.*b2.mV
    neuron.m = 0.05
    neuron.h = 0.60
    neuron.n = 0.32

    # tracking parameters
    st_mon = b2.StateMonitor(neuron, "vm", record=True)

    # running the simulation
    hh_net = b2.Network(neuron)
    hh_net.add(st_mon)
    hh_net.run(simulation_time)

    return st_mon

I_e = 7.0 * b2.uA
state_monitor = simulate_HH_neuron(I_e, 200 * b2.ms)
plot_data(state_monitor, title="HH Neuron")
