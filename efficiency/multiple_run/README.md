### Multiple RUN

-  01_example.py : in each run a parametr change. It use default cython for efficiency.
-  02_example.py : use standalone mode. It just shows the usage and is not the best option for this example. for more discussion look at [here](https://brian.discourse.group/t/multiple-run-in-standalone-mode/131/7).
- parallel.py and sequential.py: repeated execution of a standalone simulation with changed parameters without recompilation, taken from [here](https://gist.github.com/mstimberg/572d5cc3d303da2326a6193980c701db).
