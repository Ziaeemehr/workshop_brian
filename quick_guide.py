import brian2 as b2
import numpy as np
import multiprocessing


# Seeding the pseudo random number generator when using cpp_standalone
b2.set_device('cpp_standalone')
b2.device.insert_code('main', 'srand(' + str(int(time.time()) + os.getpid()) + ');')
# https://github.com/brian-team/brian-material/blob/master/2015-CNS-tutorial/04-advanced-brian2/Advanced%20Brian2%20tutorial%20CNS%202015.ipynb

with multiprocessing.Pool(20) as p:
    results = p.map(my_func, arguments)