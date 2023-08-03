# This will combine the statistics of RFs from many simulations to make the
# statistical analysis... Things that I am changing: the amount of correlations
# and average event size.

# wosniack September 2019

#!/Users/wosniack/anaconda3/envs/working/bin/python3
#%%
import numpy as np
#matplotlib notebook
import matplotlib.pyplot as plt
import pandas as pd
import os, sys
import glob
import csv
from matplotlib import style
style.use('seaborn')
# defining things for the figures
SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font',  size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes',  titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes',  labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick',  labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick',  labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend',  fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure',  titlesize=BIGGER_SIZE)  # fontsize of the figure title
#%%
path1 = '/Volumes/gjor/personal/wosniackm/LH-project/Multi-sensory/Results_2020/s1_v1_20_80_with_bias/fix_theta/'
#%%
# Auxiliar function to load the data discarding hidden files
def listdir_nohidden(path):
    #return glob.glob(os.path.join(path + '[.pdf]', '*'))
    files = [fn for fn in glob.glob(os.path.join(path + '*')) if not os.path.basename(fn).endswith('.pdf')]
    return files
#%%
all_results = pd.DataFrame()
dir_list = listdir_nohidden(path1)
#%%      corr_thres = float(folder[118:121])       ]
ind = 0
total_files = len(dir_list)
info_sum = np.zeros((total_files, 13))
column_names = ['theta_v1', 'correlation', 'rf_size_v1', 'spars_v1', 'topo_v1',
                'align_v1', 'rf_size_s1', 'spars_s1', 'topo_s1', 'align_s1',
                'prop_v1', 'prop_s1', 'prop_bimodal']
for folder in dir_list:
    os.chdir(folder)
    with open('stats.txt', newline='') as csvfile:
          readrow = pd.read_csv(csvfile, header=None)
          try:
              corr_thres = float(folder[124:128])
          except:
              corr_thres = float(folder[124:127])
        #  try:
        #      corr_thres = float(folder[127:131])
        #  except:
        #      corr_thres = float(folder[127:130])
        #  try:
        #      corr_thres = float(folder[118:122])
        #  except:
        #      corr_thres = float(folder[118:121])
          try:
              correlation = float(folder[-3:])
          except:
              correlation = float(folder[-1:])
          info_sum[ind, 0] = corr_thres
          info_sum[ind, 1] = correlation
          info_sum[ind, 2:13] = readrow[0][0:11]
          ind = ind + 1
#%%
folder[124:126]
info_sum[np.isnan(info_sum)] = 0
np.shape(info_sum)
#folder
corr_thres
# Now organizing all the data into a dataframe
df_summary = pd.DataFrame(data=info_sum, columns=column_names)
#%%
np.sum(df_summary['theta_v1'] == 0.35)
list_theta_u = np.unique(df_summary['theta_v1'])
#list_correlation = [0, 0.2, 0.4, 0.6,  0.8,  1]
list_correlation = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
list_theta_u
#list_theta_u
# Analyzing the components separately
filtered_stats = np.zeros((len(list_theta_u), len(list_correlation), 13))
error_stats = np.zeros((len(list_theta_u), len(list_correlation), 13))
list_theta_u = np.unique(df_summary['theta_v1'])
#list_correlation = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
aux1 = 0
aux2 = 0
for theta_u in list_theta_u:
    ind = df_summary['theta_v1'] == theta_u
    aux2 = 0
    for corr in list_correlation:
        temp_stats = np.zeros((1,13))
        ind2 = df_summary['correlation'] == corr
        temp_stats = np.append(temp_stats, df_summary[ind*ind2],axis=0)
        filtered_stats[aux1, aux2, :] = np.mean(temp_stats[1:], axis=0)
        error_stats[aux1, aux2, :] = np.std(temp_stats[1:], axis=0)
        if np.isnan(filtered_stats[aux1, aux2, 2]):
            filtered_stats[aux1, aux2, 2] = 0
        if np.isnan(filtered_stats[aux1, aux2, 6]):
            filtered_stats[aux1, aux2, 6] = 0
        if filtered_stats[aux1, aux2, 5] < 0 or np.isnan(filtered_stats[aux1, aux2, 5]):
            filtered_stats[aux1, aux2, 5] = 0
        if filtered_stats[aux1, aux2, 9] < 0 or np.isnan(filtered_stats[aux1, aux2, 9]):
            filtered_stats[aux1, aux2, 9] = 0
        if filtered_stats[aux1, aux2, 4] < 0 or np.isnan(filtered_stats[aux1, aux2, 4]):
            filtered_stats[aux1, aux2, 4] = 0
        if filtered_stats[aux1, aux2, 8] < 0 or np.isnan(filtered_stats[aux1, aux2, 8]):
            filtered_stats[aux1, aux2, 8] = 0

        aux2 = aux2 + 1
    aux1 = aux1 + 1
#%%
plt.subplots(1,3, figsize=(20,5))
plt.subplot(1,3,1)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,12], s=120, edgecolor='k', linewidth=1,cmap='YlGn', vmin=0, vmax=100)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('% of bimodal neurons')
plt.subplot(1,3,2)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation,
                c=filtered_stats[ind][:][:,10], s=120, edgecolor='k', linewidth=1,cmap='Reds', vmin=0, vmax=100)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('% of unimodal neurons V1')
plt.subplot(1,3,3)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation,
                c=filtered_stats[ind][:][:,11], s=120, edgecolor='k', linewidth=1,cmap='Reds', vmin=0, vmax=100)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('% of unimodal neurons S1')
plt.savefig(path1 + 'cmap_percentages2.pdf')
#%%
plt.subplots(1,2, figsize=(15,5))
plt.subplot(1,2,1)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,12], s=120, edgecolor='k', linewidth=1,cmap='YlGn', vmin=0, vmax=100)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('% of bimodal neurons')
plt.subplot(1,2,2)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation,
                c=(filtered_stats[ind][:][:,10] + filtered_stats[ind][:][:,11]), s=120, edgecolor='k', linewidth=1,cmap='Purples', vmin=0, vmax=100)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('% of unimodal neurons')
plt.savefig(path1 + 'cmap_percentages1.pdf')
#%%
# Average plots...
plt.subplots(3, 3, figsize = (15,10))
for ind in range(len(list_theta_u)):
    plt.subplot(3, 3, ind + 1)
    plt.plot(list_correlation,filtered_stats[ind][:][:,10],'--D', color='tab:red', mew = 0.75, mec = 'k', label='Uni V1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,10], error_stats[ind][:][:,10], ls='none', color='tab:red', alpha=0.5)
    plt.plot(list_correlation,filtered_stats[ind][:][:,11],'--^', color='tab:blue', mew = 0.75, mec = 'k', label='Uni S1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,11], error_stats[ind][:][:,11], ls='none', color='tab:blue', alpha=0.5)
    plt.plot(list_correlation,filtered_stats[ind][:][:,12],'--o', color='tab:green', mew = 0.75, mec = 'k', label='Bimodal')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,12], error_stats[ind][:][:,12], ls='none', color='tab:green', alpha=0.5)
    plt.xlim([-0.05,1.05])
    plt.ylim([-5, 105])
    if ind == 0:
        plt.legend()
    plt.xlabel('Correlation')
    plt.ylabel('% of neurons')
    plt.gca().set_title(r'$\theta_u =$ ' + str(list_theta_u[ind]))
    #plt.text(0.8, 80, list_theta_u[ind])
plt.tight_layout()
plt.savefig(path1 + 'sum_stats_percentage.pdf')

#%%
plt.subplots(1,2, figsize=(15,5))
plt.subplot(1,2,1)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,2], s=120, edgecolor='k', linewidth=1,cmap='Reds', vmin=0, vmax=50)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('Average Receptive field size of V1')
plt.subplot(1,2,2)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,6], s=120, edgecolor='k', linewidth=1,cmap='Blues', vmin=0, vmax=50)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('Average Receptive field size of S1')
plt.savefig(path1 + 'cmap_rf_size.pdf')
#%%
plt.subplots(3, 3, figsize = (15,10))
for ind in range(len(list_theta_u)):
    plt.subplot(3, 3, ind + 1)
    plt.plot(list_correlation,filtered_stats[ind][:][:,2],'--D', ms=6,color='tab:red', mew = 0.75, mec = 'k', label='V1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,2], error_stats[ind][:][:,2], ls='none', color='tab:red', alpha=0.5)
    plt.plot(list_correlation,filtered_stats[ind][:][:,6],'--^',ms=6, color='tab:blue', mew = 0.75, mec = 'k', label='S1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,6], error_stats[ind][:][:,6], ls='none', color='tab:blue', alpha=0.5)
    #plt.plot(list_correlation,filtered_stats[ind][:][:,12],'o', color='tab:green', mew = 0.75, mec = 'k', label='Bimodal')
    #plt.errorbar(list_correlation, filtered_stats[ind][:][:,12], error_stats[ind][:][:,12], ls='none', color='tab:green', alpha=0.5)
    plt.xlim([-0.05,1.05])
    plt.ylim([-5, 105])
    if ind == 0:
        plt.legend()
    plt.xlabel('Correlation')
    plt.ylabel('Average Receptive field size')
    plt.gca().set_title(r'$\theta_u =$ ' + str(list_theta_u[ind]))
    #plt.text(0.8, 80, list_theta_u[ind])
plt.tight_layout()
plt.savefig(path1 + 'sum_stats_size.pdf')

#%%
plt.subplots(1,2, figsize=(15,5))
plt.subplot(1,2,1)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,5], s=120, edgecolor='k', linewidth=1,cmap='Reds', vmin=0, vmax=1)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('Alignment of V1')
plt.subplot(1,2,2)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,9], s=120, edgecolor='k', linewidth=1,cmap='Blues', vmin=0, vmax=1)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('Alignment of S1')
plt.savefig(path1 + 'cmap_alignment.pdf')
#%%
#alignment stats
plt.subplots(3, 3, figsize = (15,10))
for ind in range(len(list_theta_u)):
    plt.subplot(3, 3, ind + 1)
    plt.plot(list_correlation,filtered_stats[ind][:][:,5],'--D', ms=6,color='tab:red', mew = 0.75, mec = 'k', label='V1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,5], error_stats[ind][:][:,5], ls='none', color='tab:red', alpha=0.5)
    plt.plot(list_correlation,filtered_stats[ind][:][:,9],'^--',ms=6, color='tab:blue', mew = 0.75, mec = 'k', label='S1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,9], error_stats[ind][:][:,9], ls='none', color='tab:blue', alpha=0.5)
    #plt.plot(list_correlation,filtered_stats[ind][:][:,12],'o', color='tab:green', mew = 0.75, mec = 'k', label='Bimodal')
    #plt.errorbar(list_correlation, filtered_stats[ind][:][:,12], error_stats[ind][:][:,12], ls='none', color='tab:green', alpha=0.5)
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05])
    if ind == 0:
        plt.legend()
    plt.xlabel('Correlation')
    plt.ylabel('Alignment')
    plt.gca().set_title(r'$\theta_u =$ ' + str(list_theta_u[ind]))
    #plt.text(0.8, 80, list_theta_u[ind])
plt.tight_layout()
plt.savefig(path1 + 'sum_stats_alignment.pdf')

list_theta_u
list_correlation
filtered_stats[ind][:][:,4]
#%%
plt.subplots(1,2, figsize=(15,5))
plt.subplot(1,2,1)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,4], s=120, edgecolor='k', linewidth=1,cmap='Reds', vmin=0, vmax=1)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('Topography of V1')
plt.subplot(1,2,2)
for ind in range(len(list_theta_u)):
    plt.scatter(len(list_correlation)*[list_theta_u[ind]], list_correlation, c=filtered_stats[ind][:][:,8], s=120, edgecolor='k', linewidth=1,cmap='Blues', vmin=0, vmax=1)
plt.colorbar()
plt.xlabel('Input threshold')
plt.ylabel('Correlation')
plt.title('Topography of S1')
plt.savefig(path1 + 'cmap_topography.pdf')

#%%
#plt.scatter(list_theta_u,list_correlation,c=filtered_stats[:][:][:,4])
# now for the relationship in a scatterplot...
#%%
#Topography stats
plt.subplots(3, 3, figsize = (15,10))
for ind in range(len(list_theta_u)):
    plt.subplot(3, 3, ind + 1)
    plt.plot(list_correlation,filtered_stats[ind][:][:,4],'--D', ms=6,color='tab:red', mew = 0.75, mec = 'k', label='V1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,4], error_stats[ind][:][:,4], ls='none', color='tab:red', alpha=0.5)
    plt.plot(list_correlation,filtered_stats[ind][:][:,8],'--^',ms=6, color='tab:blue', mew = 0.75, mec = 'k', label='S1')
    plt.errorbar(list_correlation, filtered_stats[ind][:][:,8], error_stats[ind][:][:,8], ls='none', color='tab:blue', alpha=0.5)
    #plt.plot(list_correlation,filtered_stats[ind][:][:,12],'o', color='tab:green', mew = 0.75, mec = 'k', label='Bimodal')
    #plt.errorbar(list_correlation, filtered_stats[ind][:][:,12], error_stats[ind][:][:,12], ls='none', color='tab:green', alpha=0.5)
    plt.xlim([-0.05,1.05])
    plt.ylim([-0.05,1.05])
    if ind == 0:
        plt.legend()
    plt.xlabel('Correlation')
    plt.ylabel('Topography')
    plt.gca().set_title(r'$\theta_u =$ ' + str(list_theta_u[ind]))
    #plt.text(0.8, 80, list_theta_u[ind])
plt.tight_layout()
plt.savefig(path1 + 'sum_stats_topography.pdf')
#%%


def f(a, b, x, c):

    print(x)

params = {
    'x':3463, 'a': 1, 'b': 2, 'c': 3,
}

f(**params)

params['x']
history = {
    param_name: np.empty(timelength)
    for param_name in params.keys()
}

for idx in sim_steps:



    tracked = {
        'voltage': voltage,

    }
    for param_name, value in tracked.items():
        history[param_name][idx] = value

        #%%
