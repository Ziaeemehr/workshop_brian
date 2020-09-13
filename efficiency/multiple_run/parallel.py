from brian2 import *
import os
import time
# -----------------------------------------------------------------------------
# Helper functions that expose some internal Brian machinery


def initialize_parameter(variableview, value):
    variable = variableview.variable
    array_name = device.get_array_name(variable)
    static_array_name = device.static_array(array_name, value)
    device.main_queue.append(('set_by_array', (array_name,
                                               static_array_name,
                                               False)))
    return static_array_name


def set_parameter_value(identifier, value):
    np.atleast_1d(value).tofile(os.path.join(device.project_dir,
                                             'static_arrays',
                                             identifier))


def run_again():
    device.run(device.project_dir, with_output=False, run_args=[])


set_device('cpp_standalone', directory='parallel', clean=False)
num_neurons = 500
duration = 2*second

# Parameters
area = 20000*umetre**2
Cm = 1*ufarad*cm**-2 * area
gl = 5e-5*siemens*cm**-2 * area
El = -65*mV
EK = -90*mV
ENa = 50*mV
g_na = 100*msiemens*cm**-2 * area
g_kd = 30*msiemens*cm**-2 * area
VT = -63*mV

# The model
eqs = Equations('''
dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt
dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
    (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
    (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
    (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
I : amp
''')
# Threshold and refractoriness are only used for spike counting
group = NeuronGroup(num_neurons, eqs,
                    threshold='v > -40*mV',
                    refractory='v > -40*mV',
                    method='exponential_euler', name='neurongroup')
group.v = El
param_I = initialize_parameter(group.I, np.zeros(num_neurons))

monitor = SpikeMonitor(group, name='spikemonitor')
run(duration)

# Run it again
start = time.time()
set_parameter_value(param_I, 0.7*nA * np.arange(num_neurons) / num_neurons)
run_again()
print('Took: {:.3f}s'.format(time.time() - start))

plot(group.I/nA, monitor.count / duration)
xlabel('I (nA)')
ylabel('Firing rate (sp/s)')
show()