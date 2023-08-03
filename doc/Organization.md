# Organization of the codebase

## The default case

` run_sim.py ` -> ` main_multi_sensory.py`-> ` initializations.py `

* In `run_sim.py`: set `s1range` to default value of 0.8
* In `main_multi_sensory.py`: load default model parameters from `parameters.txt` 
* Data saved in `/gpfs/gjor/data/Lab/kongd/simulations/overlap_12022021/s1_v1_20_80_with_bias/`
* Function `plot_overview()` in `plot_sim_stat.py` read saved data and generates overview for Monte-Carlo simulations

## S1 guide V1 alignment

#### S1 has higher initial bias

 `run_sim_s1.py` -> `s1_guide.py` -> `initializations.py`

* In` s1_guide.py`: looped through a range of values for S1 initial bias. 
* Data saved in `/gpfs/gjor/data/Lab/kongd/simulations/results/align/s1_bias/`
* Function `plot_alignment_stat_range()` in `plot_sim_stat.py` reads saved data and plot the trend. 

#### S1 has smaller events

` run_sim.py ` -> ` main_multi_sensory.py`-> ` initializations.py `

* Similar to default case, but in `run_sim.py` , need to manually change `s1range` to take value of 0.4, 0.6, 0.8
* Data saved in `/gpfs/gjor/data/Lab/kongd/simulations/overlap_apr/`
* Function `plot_alignment_stat_range()` in `plot_sim_stat.py` reads saved data and make statistical tests. 

## RL has uncorrelated events

` run_sim_h.py` -> `multi_sensory_h.py` -> `initialization_h.py`

* In `run_sim_h.py`: Change `Hrl` to change the frequency of uncorrelated events in RL
* In `multi_sensory_h.py`: load default model parameters from `parameters_h.txt` 

#### RL events with normal amplitude disrupts selectivity

Data saved in `/gpfs/gjor/data/Lab/kongd/simulations/h_rl/rl_20_80/`

#### RL events with smaller amplitude recover selectivity

* Data saved in `/gpfs/gjor/data/Lab/kongd/simulations/h_rl/smaller_amp/`
* Function `plot_overview()` in `plot_sim_stat.py` read saved data and generates overview for Monte-Carlo simulations.

**Note that when saving the raw simulation data, the `parameters.txt` are saved by mistake!! The actual parameter setting used in simulations should be `parameters_h.txt` !!**

## Plotting 

`making_figures.py`: For each individual simulation, plot the weight matrices, etc.

`plot_sim_stat.py`: read from saved simulation results and make summary plots. 

- main functions:
  - `plot_overview()` : 
  - `plot_alignment_stat_range()`
  - `plot_alignment_stat_bias()`

# Organization of raw simulation data folder

Apart from the above-mentioned directories, there are other folders containing data for exploratory simulations (mostly parameter range exploration and alternative ways of generating events). If a folder has '(bug)' in its name, then it has severe bugs that messed up the entire simulations. 

`/gpfs/gjor/data/Lab/kongd/`

* `analysis`: Wide-Field data analysis (intermediate data or plots)
* `lh_event`: simulation data for recurrent model
* `simulation`: simulation data for 3-area-feedforward-model
  * `boundxxx`: changing upper bound of weights
  * `h_rl`: adding uncorrelated events to RL
  * `overlap_xxx`:
    * folders named 'v1_s1_20_x0_with_bias' usually denotes the participation rate of S1 events is 20%-x0%
    * Folders named 'theta_xxxcorr_xxx' denotes the threshold and correlation between v1 and s1

