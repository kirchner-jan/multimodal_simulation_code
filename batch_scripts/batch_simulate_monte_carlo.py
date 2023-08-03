#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" The goal here is to sketch the code for the co-refinement of V1 and S1 via their interaction through RL
    Big questions here: emergence of multisensory cells... like one RL cell being sensitive to both a neighborhood of v1 and s1 neurons...
    If S1-RL is already refined, how this would influence the refinement between V1 and RL? 
    Deyue Kong and Marina Wosniack, using Monica's and Varsha's previous codes.
    - refactored and extended by Jan Kirchner in May 2021
"""
#%%
import os, json , time , datetime , numpy , multiprocessing , random
from tools.biased_weights import biased_weights
from tools.runSimulation import runSimulation
# =============================================================================
# from analysis.making_figures import making_figures
# from analysis.making_stats import making_stats
# =============================================================================
#%%
def getPrmsMats():
    # load all the other parameters from a text file
    with open('parameters/parameters.txt') as f: prms = json.load(f)
    # generate biased weight matrices
    mats = dict()
    mats['W_v1'] = biased_weights(prms['N_v1'], prms['W_initial_v1'], prms['bias_v1'], prms['spread_v1'])
    mats['W_s1'] = biased_weights(prms['N_s1'], prms['W_initial_s1'], prms['bias_s1'], prms['spread_s1'])
    return prms , mats
#%%
def worker(num):
    # print(i)
    numpy.random.seed(random.randint(1,99999999))
    prms , mats = getPrmsMats()
    # set the output path
    prms['path'] = 'simulations/monte_carlo/'
    prms['path_main'] = prms['path'] + str(datetime.datetime.now()) + '_' + str(round(numpy.random.rand() , 5))
    os.makedirs(prms['path_main'] , exist_ok=True)
    # Monte Carlo sample parameters
    prms['corr_thres'] = numpy.random.uniform(low=0.25,high=0.75) # 0.5 # 
    prms['spatio_temp_corr'] = numpy.random.uniform(low=0.0,high=1.0)
    prms['logFlag'] = (num == 0)
    # run the simulation
    simOutput = runSimulation(prms , mats)
    numpy.save(prms['path_main'] + '/simOutput_' + str(round(numpy.random.rand() , 5)) +'.npy' , simOutput)
    #making_figures(simOutput[3]['path_main'], simOutput[3]['W_thres'],
    #           simOutput[4]['W_v1'], simOutput[4]['W_s1'],
    #           simOutput[1], simOutput[2], simOutput[0])
    #making_stats(simOutput[3]['path_main'], simOutput[4]['W_v1'], simOutput[4]['W_s1'],
             #simOutput[3]['W_thres'][1]/5, simOutput[3]['N_v1'])
    return 
#%%
if __name__ == '__main__':
    for xx in numpy.arange(50):
        jobs = []   
        numpy.warnings.filterwarnings('ignore', category=numpy.VisibleDeprecationWarning)
        for i in numpy.arange(40):
            time.sleep(1)
            p = multiprocessing.Process(target=worker, args=(i,))
            jobs.append(p)
            p.start()
        for j in jobs:
            j.join()
