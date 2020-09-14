# https://github.com/brian-team/brian2/issues/1154#issuecomment-582994117
import os
import multiprocessing

from brian2 import *


def run_sim(tau):
    
    set_device('cpp_standalone', directory=None)
    pid = os.getpid()
    print(f'RUNNING {pid}')

    G = NeuronGroup(1, 'dv/dt = -v/tau : 1', method='euler')
    G.v = 1

    mon = StateMonitor(G, 'v', record=0)
    net = Network()
    net.add(G, mon)
    net.run(100 * ms)
    res = (mon.t/ms, mon.v[0])

    device.reinit()

    print(f'FINISHED {pid}')
    return res


if __name__ == "__main__":
    num_proc = 4

    tau_values = np.arange(10)*ms + 5*ms
    with multiprocessing.Pool(num_proc) as p:
        results = p.map(run_sim, tau_values)

    for tau_value, (t, v) in zip(tau_values, results):
        plt.plot(t, v, label=str(tau_value))
    plt.legend()
    plt.show()
