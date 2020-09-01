import numpy as np
import brian2 as b2
import pylab as plt


b2.start_scope()
b2.set_device('cpp_standalone', debug=True)
# b2.prefs.codegen.target = 'numpy'  # use the Python fallback

tau = 10*b2.ms
eqs = '''
dv/dt = (1-v)/tau : 1
'''
G = b2.NeuronGroup(1, eqs, method='exact')
b2.run(100*b2.ms)
print('After v = %s' % G.v[0])