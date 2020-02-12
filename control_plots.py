import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns

from invisible_cities.core.core_functions  import shift_to_bin_centers
from invisible_cities.core .core_functions import weighted_mean_and_std
from  invisible_cities.core.system_of_units_c import units


plt.rcParams["figure.figsize"] = 10, 8
plt.rcParams["font.size"     ] = 14
sns.set()
sns.set_style("white")
sns.set_style("ticks")

def labels(xlabel, ylabel, title=""):
    """
    Return x and y labels in plot
    """
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title ( title)

def hist(*args, **kwargs):
    """
    Return output of histogram with shift bins
    """
    y, x, p = plt.hist(*args, **kwargs)
    return y, shift_to_bin_centers(x), p

def plot_stat(x, y):
    """
    Input x and y from a binned histogram
    Return mu and sigma statistics and add to the plot
    """

    mean, std = weighted_mean_and_std(x, y, \
    frequentist = True, unbiased = True)

    entries  =  f'Entries = {len(x)}'
    mean     =  r'$\mu$ = {:7.2f}'.format(mean)
    sigma    =  r'$\sigma$ = {:7.2f}'.format(std)
    stat     =  f'{entries}\n{mean}\n{sigma}'

    plt.legend([stat], loc='upper right')

def s1_1D_control_plots(plots_dir, dst, opt_dict, selection_label):
    """
    Input config file dictionary
    Return one pdf with X S1 related plots
    """
    s1e_min   = float(opt_dict["s1e_min"])
    s1e_max   = float(opt_dict["s1e_max"])
    s1e_bin   = int(opt_dict["s1e_bin"])

    s1w_min   = float(opt_dict["s1w_min"])
    s1w_max   = float(opt_dict["s1w_max"])
    s1w_bin   = int(opt_dict["s1w_bin"])

    s1h_min   = float(opt_dict["s1h_min"])
    s1h_max   = float(opt_dict["s1h_max"])
    s1h_bin   = int(opt_dict["s1h_bin"])

    s1e_range = (s1e_min, s1e_max)
    s1w_range = (s1w_min, s1w_max)
    s1h_range = (s1h_min, s1h_max)

    hist_type = 'stepfilled'
    col       = 'steelblue'
    col2      = 'lightblue'

    fig = plt.figure(figsize=(15,25))
    ax      = fig.add_subplot(5, 2, 1)
    y, x, p = hist(dst.S1e, bins = s1e_bin, range = s1e_range, histtype=hist_type, color=col)
    labels('S1e (pes)','Entries','')
    plot_stat(x,y)
    ax      = fig.add_subplot(5, 2, 2)
    y, x, p = hist(dst.S1e, bins = s1e_bin, range = s1e_range, histtype=hist_type, color=col2)
    labels('S1e (pes)','Entries','')
    plot_stat(x,y)
    ax.set_yscale('log')

    ax      = fig.add_subplot(5, 2, 3)
    y, x, p = hist(dst.S1w/units.mus, bins = s1w_bin, range = s1w_range, histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('Width ($\mu$s)','Entries','')
    ax      = fig.add_subplot(5, 2, 4)
    y, x, p = hist(dst.S1w/units.mus, bins = s1w_bin, range = s1w_range, histtype=hist_type, color=col2)
    labels('Width (mus)','Entries','')
    plot_stat(x,y)
    ax.set_yscale('log')

    ax      = fig.add_subplot(5, 2, 5)
    y,x,p = hist(dst.S1h, bins = s1h_bin, range = s1h_range, histtype=hist_type, color=col)
    labels('S1 height (pes)','Entries','')
    plot_stat(x,y)
    ax      = fig.add_subplot(5, 2, 6)
    y,x,p = hist(dst.S1h, bins = s1h_bin, range = s1h_range, histtype=hist_type, color=col2)
    labels('S1 height (pes)','Entries','')
    plot_stat(x,y)
    ax.set_yscale('log')

    x      = fig.add_subplot(5, 2, 7)
    y,x,p  = hist(dst.S1h/dst.S1e, bins = 100, range = (0,0.6), histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('S1height/s1e (pes)','Entries','')
    ax      = fig.add_subplot(5, 2, 8)
    y,x,p = hist(dst.S1h/dst.S1e, bins = 100, range = (0,0.6), histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('S1height/s1e (pes)','Entries','')
    ax.set_yscale('log')

    ax      = fig.add_subplot(5, 2, 9)
    y,x,p = hist(dst.S1t/units.mus, bins = 20, range = (0,400), histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('S1 time mus','Entries','')


    ax      = fig.add_subplot(5, 2, 10)
    y,x,p = hist(dst.S1t/units.mus, bins = 20, range = (0,400), histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('S1 time mus','Entries','')
    ax.set_yscale('log')

    plt.savefig(f'{plots_dir}/s1_plots_{selection_label}.png')
    print('plots saved in '+ plots_dir)
    #plt.show()   --> fix size of plot when showing


def s2_1D_control_plots(plots_dir, dst, opt_dict, selection_label):
    """
    Input directory of plots and config file dictionary
    Return one pdf with X S2 related plots
    """

## compute bins from range
    s2e_min   = float(opt_dict["s2e_min"])
    s2e_max   = float(opt_dict["s2e_max"])
    s2e_bin   = int(opt_dict["s2e_bin"])

    s2w_min   = float(opt_dict["s2w_min"])
    s2w_max   = float(opt_dict["s2w_max"])
    s2w_bin   = int(opt_dict["s2w_bin"])

    s2h_min   = float(opt_dict["s2h_min"])
    s2h_max   = float(opt_dict["s2h_max"])
    s2h_bin   = int(opt_dict["s2h_bin"])

    s2e_range = (s2e_min, s2e_max)
    s2w_range = (s2w_min, s2w_max)
    s2h_range = (s2h_min, s2h_max)

    hist_type = 'stepfilled'
    col       = 'crimson'
    col2      = 'lightcoral'

    fig = plt.figure(figsize=(13,35))

    ax      = fig.add_subplot(7, 2, 1)
    y,x,p = hist(dst.S2e, bins = s2e_bin, range = s2e_range, histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('S2e (pes)','Entries','')


    ax      = fig.add_subplot(7, 2, 2)
    y,x,p = hist(dst.S2e, bins = s2e_bin, range = s2e_range, histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('S2e (pes)','Entries','')
    ax.set_yscale('log')

    ax      = fig.add_subplot(7, 2, 3)
    y,x,p = hist(dst.S2h, bins =s2h_bin , range = s2h_range, histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('S2h (pes)','Entries','')


    ax      = fig.add_subplot(7, 2, 4)
    y,x,p = hist(dst.S2h, bins = s2h_bin, range = s2h_range, histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('S2h (pes)','Entries','')
    ax.set_yscale('log')

    ax      = fig.add_subplot(7, 2, 5)
    y,x,p = hist(dst.S2w, bins =s2w_bin , range = s2w_range, histtype=hist_type, color=col)
    labels('S2w ($\mu$s)','Entries','')


    ax      = fig.add_subplot(7, 2, 6)
    y,x,p = hist(dst.S2w, bins = s2w_bin, range = s2w_range, histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('S2w ($\mu$s)','Entries','')
    ax.set_yscale('log')

    ax      = fig.add_subplot(7, 2, 7)
    y,x,p = hist(dst.S2h/dst.S2e, bins = 100, range = (0,0.6), histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('S2height/s2e (pes)','Entries','')

    ax      = fig.add_subplot(7, 2, 8)
    y,x,p = hist(dst.S2h/dst.S2e, bins = 100, range = (0,0.6), histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('S2height/s2e (pes)','Entries','')
    ax.set_yscale('log')

    ax      = fig.add_subplot(7, 2, 9)
    y,x,p = hist(dst.S2t/units.mus, bins = 20, range = (400,800), histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('S2 time ($\mu$s)','Entries','')

    ax      = fig.add_subplot(7, 2, 10)
    y,x,p = hist(dst.S2t/units.mus, bins = 20, range = (400,800), histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('S2 time ($\mu$s)','Entries','')
    ax.set_yscale('log')

    ax      = fig.add_subplot(7, 2, 11)
    y,x,p = hist(dst.DT, bins = 100, range = (0,400), histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('Drit time ($\mu$s)','Entries','')

    ax      = fig.add_subplot(7, 2, 12)
    y,x,p = hist(dst.DT, bins = 100, range = (0,400), histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('Drift time ($\mu$s)','Entries','')
    ax.set_yscale('log')

    ax      = fig.add_subplot(7, 2, 13)
    y,x,p = hist(dst.Z, bins = 100, range = (0,400), histtype=hist_type, color=col)
    plot_stat(x,y)
    labels('Z (mm)','Entries','')

    ax      = fig.add_subplot(7, 2, 14)
    y,x,p = hist(dst.Z, bins = 100, range = (0,400), histtype=hist_type, color=col2)
    plot_stat(x,y)
    labels('Z (mm)','Entries','')
    ax.set_yscale('log')

    plt.savefig(f'{plots_dir}/s2_plots_{selection_label}.png')
    print('plots saved in '+ plots_dir)
