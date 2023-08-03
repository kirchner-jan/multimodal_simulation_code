import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import style
style.use('seaborn')
import seaborn as sns
import os, sys
import json
import scipy.stats as stats
from clean_dir import*
import statannot
import pandas as pd


#%% helper function, reading from raw data folder, sorting 

def sort_ls(X,Y):
    y = [y for _,y in sorted(zip(X,Y))]
    x = [x for x,_ in sorted(zip(X,Y))]
    return x,y

def remove_nan(x):
    return x[~np.isnan(x)]

# get corr and thr parameter from folder name
def dirName_to_param(name):
    if name[:6] != 'theta_':
        print('Error: incorrect folder name. (no theta)')
    else:
        end_inx_thr = name.find('corr_')
        if end_inx_thr == -1:
            print('Error: incorrect folder name. (no corr)')
        else:
            thr = float(name[6:end_inx_thr])
            start_inx_corr = end_inx_thr + 5
            end_inx_corr = name.find('s1b')
            if end_inx_corr == -1:
                corr = float(name[start_inx_corr:])
                bool_mature = False
            else:
                corr = float(name[start_inx_corr:end_inx_corr])
                bool_mature = True
    param={'thr':thr, 'corr':corr,'bool_mature':bool_mature}
    return param

# get all alignment results in given path
def alignment_under_folder(result_path):
    #In case there are empty folders
    #remove_empty(result_path)
    param_dict = {}
    param_ls =[]
    stat_ls = []
    stat_dict = {}
    name_ls = [name for name in os.listdir(result_path) if name[0]=='t']
    for name in name_ls:
            param = dirName_to_param(name)
            param_ls.append(param)
            param_dict[name]=param
            f_name = result_path + name + "/stats.txt"

            stat = np.loadtxt(f_name, delimiter="\n", unpack=True)
            """
            stat = [rf_size_v1, spars_v1, topo_v1, align_v1,
                        rf_size_s1, spars_s1, topo_s1, align_s1,
                        proportions[0], proportions[1], proportions[2]]"""
            stat_ls.append(stat)
            stat_dict[name] = stat

    #print('num of simulations:',len(stat_ls))

    align_v1 = []
    topo = []
    for name in name_ls:
            param = param_dict[name]
            stat = stat_dict[name]
            #if param['bool_mature'] == True:
                #continue
            x = param['thr']
            y = param['corr']

            if x<=0.55 and x>=0.45 :
                align_v1.append(stat[3])
                topo.append(stat[2])
    print('number of data points:',len(align_v1))
    return np.array(align_v1), np.array(topo)

#%% main functions for overview plots

def plot_overview():
    # define the data folder to read from, and foler to save plots

    #result_path = "/gpfs/gjor/data/Lab/kongd/simulations/overlap_12022021/s1_v1_20_80_with_bias/"
    result_path = "/gpfs/gjor/data/Lab/kongd/simulations/h_rl/smaller_amp/h_freq10.0/"
    #result_path = "/gpfs/gjor/data/Lab/kongd/simulations/bound200/s1_v1_20_80_with_bias/"

    #save_path = "/gpfs/gjor/personal/kongd/results/bound200/range_20_80/"
    #save_path = "/gpfs/gjor/personal/kongd/results/overlap_18022021/range_20_40/"
    #save_path = "/gpfs/gjor/personal/kongd/results/h_rl/rl_20_80/h_freq10.0/"
    save_path = "/gpfs/gjor/personal/kongd/results/h_rl/smaller_amp/h_freq10.0/"
    os.makedirs(save_path, exist_ok=True)

    name_ls = [name for name in os.listdir(result_path) if name[0]=='t']

    param_dict = {}
    param_ls =[]
    stat_ls = []
    stat_dict = {}
    for name in name_ls:
        param = dirName_to_param(name)
        param_ls.append(param)
        param_dict[name]=param
        f_name = result_path + name + "/stats.txt"

        stat = np.loadtxt(f_name, delimiter="\n", unpack=True)
        """
        stat = [rf_size_v1, spars_v1, topo_v1, align_v1,
                    rf_size_s1, spars_s1, topo_s1, align_s1,
                    proportions[0], proportions[1], proportions[2]]"""
        stat_ls.append(stat)
        stat_dict[name] = stat

    print('num of simulations:',len(stat_ls))

    # no early s1 mature, bimodal ratio
    x_ls =[]
    y_ls =[]
    c_ls_ratio = []
    c_ls_rf_v1 = []
    c_ls_rf_s1 = []
    topo_v1 = []
    align_v1 = []

    
    for name in name_ls:
        param = param_dict[name]
        stat = stat_dict[name]
        #if param['bool_mature'] == True:
            #continue
        x = param['thr']
        y = param['corr']

        # for 2D-plot
        
        x_ls.append(x)
        y_ls.append(y)
        c_ls_ratio.append(stat[-1])
        if np.isnan(stat[0]):
            c_ls_rf_v1.append(0)
        else:
            c_ls_rf_v1.append(stat[0])
        if np.isnan(stat[4]):
            c_ls_rf_s1.append(0)
        else:
            c_ls_rf_s1.append(stat[4])
            #c_ls_rf_s1.append(stat[4])
        topo_v1.append(stat[2])
        align_v1.append(stat[3])

        # for 1D-plot

    print('num of data points:',len(x_ls))


    # for plotting analytical prediction (optional)
    with open('parameters.txt') as f:
        variables = json.load(f)
    N = variables["N_v1"]
    l_range = variables["L_range_v1"]
    l_ls = np.arange(l_range[0]*N,l_range[1]*N+1)
    c_ls = []
    for k in range(N):
        res = 0
        for l in l_ls:
            res+= (l - min(min(N-k,k),min(N-l,l)))/N
        c_k = res/(l_ls[-1]-l_ls[0])
        c_ls.append(c_k)

    slope = N/np.sum(c_ls)* np.mean(l_range)
    pred = slope * np.array(x_ls )

    fig = plt.figure()
    plt.scatter(x_ls,y_ls,c=c_ls_ratio,cmap='viridis',label='Simulations',vmin=0, vmax=100)
    plt.plot(x_ls,pred,label='Prediction')
    plt.ylim([np.min(y_ls)-0.05,np.max(y_ls)+0.05])
    #plt.xlim([0.2,0.9])
    plt.colorbar()
    plt.xlabel('Threshold')
    plt.ylabel('Spatial temporal correlation')
    plt.title('Ratio of bimodal neurons')
    plt.legend()
    plt.savefig(save_path + "ratio.png")
    plt.close(fig)


    fig1 = plt.figure()
    plt.scatter(x_ls,y_ls,c=c_ls_rf_v1,cmap='viridis',vmin=0, vmax=50)
    plt.colorbar()
    plt.xlabel('Threshold')
    plt.ylabel('Spatial temporal correlation')
    plt.title('V1 receptive field size')
    plt.savefig(save_path + "rf_v1.png")
    plt.close(fig1)

    fig2 = plt.figure()
    plt.scatter(x_ls,y_ls,c=c_ls_rf_s1,cmap='viridis',vmin=0, vmax=50)
    plt.colorbar()
    plt.xlabel('Threshold')
    plt.ylabel('Spatial temporal correlation')
    plt.title('S1 receptive field size')
    plt.savefig(save_path + "rf_s1.png")
    plt.close(fig2)

    fig3 = plt.figure()
    plt.scatter(x_ls,y_ls,c=align_v1,cmap='viridis',vmin=0, vmax=1)
    plt.colorbar()
    plt.xlabel('Threshold')
    plt.ylabel('Spatial temporal correlation')
    plt.title('V1 alignment')
    plt.xlim([np.min(x_ls),np.max(x_ls)])
    plt.savefig(save_path + "align_v1.png")
    plt.close(fig3)

    fig4 = plt.figure()
    plt.scatter(x_ls,y_ls,c=topo_v1,cmap='viridis')
    plt.colorbar()
    plt.xlabel('Threshold')
    plt.ylabel('Spatial temporal correlation')
    plt.title('V1 topography')
    plt.savefig(save_path + "topo_v1.png")
    plt.close(fig4)



def plot_alignment_stat_range():
    
    result_path = "/gpfs/gjor/data/Lab/kongd/simulations/overlap_apr/"
    
    save_path = "/gpfs/gjor/personal/kongd/results/overlap_apr/align_stat/range/"


    os.makedirs(save_path,exist_ok=True)

    align_2080, topo_2080= alignment_under_folder(result_path + "s1_v1_20_80_with_bias/")
    align_2060 , topo_2060= alignment_under_folder(result_path + "s1_v1_20_60_with_bias/")
    align_2040 , topo_2040= alignment_under_folder(result_path + "s1_v1_20_40_with_bias/")

    align_2040 = remove_nan(align_2040)
    align_2060 = remove_nan(align_2060)
    align_2080 = remove_nan(align_2080)
    topo_2040 = remove_nan(topo_2040)
    topo_2060 = remove_nan(topo_2060)
    topo_2080 = remove_nan(topo_2080)

    print(align_2080)
    align_all = [ align_2040, align_2060, align_2080]
    df = pd.DataFrame(data = align_all)
    df = df.T
    df.columns = ['20-40%', '20-60%', '20-80%']
    #print(df)


    stat, p = stats.mannwhitneyu(align_2080,align_2060)
    
    print('80_60 align',stat,p)
    stat, p = stats.mannwhitneyu(align_2080,align_2040)
    
    print('80_40 align',stat,p)
    stat, p = stats.mannwhitneyu(align_2060,align_2040)
    
    print('60_40 align',stat,p)


    
    order = ['20-40%', '20-60%', '20-80%']
    ax = sns.boxplot(data = df)
    ax = sns.stripplot(data = df)
    test_results = statannot.add_stat_annotation(ax, data = df,test='Mann-Whitney',\
    box_pairs=[('20-80%', '20-40%')],comparisons_correction=None, text_format='star',loc='outside', verbose=2)
    ax.set_xticks([0, 1,2])
    ax.set_xticklabels(['20-40%', '20-60%', '20-80%'])
    ax.set_ylabel('V1 alignment')
    ax.set_xlabel('S1 participation rate')
    plt.savefig(save_path + "box_compare_align_range.png")



def plot_alignment_stat_bias():
    result_path = "/gpfs/gjor/data/Lab/kongd/simulations/results/align/s1_bias/"
    save_path = "/gpfs/gjor/personal/kongd/results/overlap_12022021/align_stat/bias/"
    os.makedirs(save_path, exist_ok=True)

    name_ls = [name for name in os.listdir(result_path) if name[0]=='t']
    #print(name_ls)

    curve_ls = []
    topo_curve_ls = []
    for name in name_ls:
        points_ls = [point for point in os.listdir(result_path + name + "/" ) if point[0]=='s']
        bias_ls = []
        align_ls = []
        topo_ls = []

        #sort in ascending order of bias
        for point in points_ls:
            bias = float(point[point.find('s1b')+4 : point.find('_trial')])*0.01
            bias_ls.append(bias)
        bias_ls, points_ls = sort_ls(bias_ls,points_ls)
        
        for point in points_ls:
            
            f_name = result_path + name + "/" + point + "/stats.txt"
            stat = np.loadtxt(f_name, delimiter="\n", unpack=True)
            #print('stat',stat)
            align_ls.append(stat[3])
            topo_ls.append(stat[2])
            
        curve_ls.append(align_ls)
        topo_curve_ls.append(topo_ls)
    
    curve_mean = np.nanmean(curve_ls,axis=0)
    sd = np.nanstd(curve_ls,axis=0)

    fig = plt.figure()
    for curve in curve_ls:
        plt.scatter(bias_ls, curve,color='grey')
    plt.plot(bias_ls,curve_mean,color='b')
    plt.fill_between(bias_ls, curve_mean-sd, curve_mean+sd, color='b', alpha=0.3)
    plt.xlabel('S1 bias')
    plt.ylabel('V1 alignment')
    plt.savefig(save_path + "compare_align_bias.png")
    plt.close(fig)





plot_overview()
plot_alignment_stat_range()
plot_alignment_stat_bias()

