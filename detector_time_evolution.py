import warnings

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns

from control_plots import labels

from krcal.core.fitmap_functions    import time_fcs_df
#from krcal.NB_utils.plt_functions   import plot_time_fcs
from krcal.core.selection_functions import get_time_series_df
from krcal.core.kr_types            import FitType
#from krcal.core.map_functions       import amap_average

from krcal.core.selection_functions  import select_xy_sectors_df
from krcal.core.selection_functions  import event_map_df
from krcal.core.fitmap_functions     import fit_map_xy_df
from krcal.core.map_functions        import tsmap_from_fmap
from krcal.core.map_functions        import amap_from_tsmap
from krcal.core.map_functions        import amap_average
from krcal.NB_utils.xy_maps_functions     import draw_xy_maps




def plot_e0_lf_chi2(fit_times):
    """
    """

    e_mean = np.array(fit_times.e0[0:8]).mean()
    up   = (0.005 * e_mean) + e_mean
    down = e_mean - (0.005 * e_mean)
    e_mean_lim_max = up * 1.01
    e_mean_lim_min = down -  (e_mean_lim_max - up)

    lt_mean = np.array(fit_times.lt[0:8]).mean()

    up_lt   = (0.1 * lt_mean) + lt_mean
    down_lt = lt_mean - (0.1 * lt_mean)
    lt_mean_lim_max = up_lt * 1.3
    lt_mean_lim_min = down_lt -  (lt_mean_lim_max - up_lt)

    fig  = plt.figure(figsize=(14, 12))
    plt.subplot(221)
    plt.errorbar(fit_times.ts, fit_times.e0, fit_times.e0u, 0, "p", c="k", capsize=2);
    plt.axhline(y = e_mean, color='grey', alpha=0.4, linestyle = 'dotted');
    plt.axhline(y = up, color='red', alpha=0.4, linestyle = 'dotted', label='0.5 % rel. uncert.');
    plt.axhline(y = down, color='red', alpha=0.4, linestyle = 'dotted');
    plt.ylim(e_mean_lim_min , e_mean_lim_max)
    labels('S2 energy (pes)','Entries','')
    plt.legend()

    plt.subplot(222)
    plt.errorbar(fit_times.ts, fit_times.lt, fit_times.ltu, 0, "p", c="k", capsize=2);
    plt.axhline(y = lt_mean, color='grey', alpha=0.4, linestyle = 'dotted');
    plt.axhline(y = up_lt, color='red', alpha=0.4, linestyle = 'dotted',  label='10 % rel. uncert.');
    plt.axhline(y = down_lt, color='red', alpha=0.4, linestyle = 'dotted');
    plt.ylim(lt_mean_lim_min , lt_mean_lim_max)
    labels('Lifetime ($\mu$s)','Entries','')
    plt.legend()


    plt.subplot(223)
    plt.errorbar(fit_times.ts, fit_times.c2, np.sqrt(fit_times.c2), 0, "p", c="k", capsize=2);
    labels('Chi2','Entries','')

    return fig


def fit_time_evolution(dst, opt_dict):
    """
    XY integrated
    get_time_series_df  --> returns time series and masks to divide file/run in branches
    time_fcs_df   --> fits lifetime for a time series
    plot_time_fcs
    """
    time_bin = int(opt_dict['time_bin'])
    z_bin = int(opt_dict['z_bin'])
    e_bin = int(opt_dict['e_bin'])
    dt_min   = float(opt_dict["dt_min"])
    dt_max   = float(opt_dict["dt_max"])
    s2e_sig_min   = float(opt_dict["s2e_sig_min"])
    s2e_sig_max   = float(opt_dict["s2e_sig_max"])

    ts, masks = get_time_series_df(time_bin, (dst.time.values[0], dst.time.values[-1]), dst)
    fit_times = time_fcs_df(ts, masks, dst,
                  nbins_z = z_bin,
                  nbins_e = e_bin,
                  range_z = (dt_min, dt_max),
                  range_e = (s2e_sig_min, s2e_sig_max),
                  energy  = 'S2e',
                  fit     = FitType.profile)


    return fit_times


def plot_xy_map_first_last_time():
    """
    """
"""

    first_time_map  = amap_from_tsmap(time_series_maps,
                      ts         = 0,
                      range_e    = e_range,
                      range_chi2 = chi2_range,
                      range_lt   = lt_range)
    last_time_map  = amap_from_tsmap(time_series_maps,
                      ts         = 0,
                      range_e    = e_range,
                      range_chi2 = chi2_range,
                      range_lt   = lt_range)

"""


def plot_num_ev_xy(nXY):
    """
    """
    fig  = plt.figure(figsize=(14, 12))
    plt.subplot(221)
    sns.set()
    sns.set_style("white")
    sns.set_style("ticks")
    ax  = sns.heatmap(nXY, square=True,cmap='coolwarm')

    return fig


def xy_time_evolution(dst, opt_dict):
    """
    Obtain a time-series of maps (tsm) from a fit-map (fmap).
    """

        # estudios en funcion de XY
    xy_num_bins = int(opt_dict["xy_num_bins"])
    r_max   = int(opt_dict["r_max"])
    z_bin   = int(opt_dict["z_bin"])
    e_bin   = int(opt_dict["e_bin"])
    dt_sig_min   = int(opt_dict["dt_sig_min"])
    dt_sig_max   = int(opt_dict["dt_sig_max"])
    s2e_sig_min  = int(opt_dict["s2e_sig_min"])
    fit_type     = str(opt_dict["fit_type"])

    z_range = (dt_sig_min, dt_sig_max)
    e_range = (s2e_sig_min, s2e_sig_min)
    x_range = (-r_max,r_max)
    y_range = (-r_max,r_max)

    # ? understand what it is used for
    nmin    = 60

    print('Number of XY bins: ', xy_num_bins, '(', dst.event.nunique(), 'events)')
    XYbins     = (xy_num_bins , xy_num_bins)

    xbins = np.linspace(*x_range, XYbins[0]+1)
    ybins = np.linspace(*y_range, XYbins[1]+1)

    KXY     = select_xy_sectors_df(dst, xbins, ybins)
    # KXY is a DataFrameMap = Dict[int, List[DataFrame]]
    nXY     = event_map_df(KXY)    # To do: obtenir el valor mes menut
    fig_nXY = plot_num_ev_xy(nXY)

    ## estamos usando 10 time bins, podemos tener falta de estadistica
    #cuando binamos demasiado ambos XY y tiempo
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fitted_map_xy = fit_map_xy_df(selection_map = KXY,
                             event_map     = nXY,
                             n_time_bins   = 1,
                             time_diffs    = dst.time.values,
                             nbins_z       = z_bin,
                             nbins_e       = e_bin,
                             range_z       = z_range,
                             range_e       = e_range,
                             energy        = 'S2e',
                             z             = 'Z',
                             fit           = fit_type,
                             n_min         = nmin)

    print()
    #Obtain a time-series of maps (tsm) from a fit-map (fmap)
    # here only one element as in the above function n_time_bins = 1
    time_series_maps = tsmap_from_fmap(fitted_map_xy)

    # Select a map from the time-series time_series_maps
    # (here only one time bin ts=0)
    # ? to understand : estos límites para que se usan
    chi2_range = (0,10)
    lt_range   = (0, 1e6)
    map = amap_from_tsmap(time_series_maps,
                          ts         = 0,
                          range_e    = e_range,
                          range_chi2 = chi2_range,
                          range_lt   = lt_range)
    average_map = amap_average(map)
    # obtain limits for the plot from the average values:20%up and down
    e0_limits_up   = amap_average(map).e0*1.1
    e0_limits_down = amap_average(map).e0/1.1
    e0_limits = (e0_limits_down, e0_limits_up)

    eu_limits_up = amap_average(map).e0u*2
    eu_limits_down = amap_average(map).e0u/1.5
    eu_limits = (eu_limits_down, eu_limits_up)

    lt_limits_up   = amap_average(map).lt*2
    lt_limits_down = amap_average(map).lt/2
    lt_limits      = (lt_limits_down, lt_limits_up)

    ltu_limits_up   = amap_average(map).lt*2
    ltu_limits_down = amap_average(map).lt/1.1
    ltu_limits      = (ltu_limits_down, ltu_limits_up)

    fig_XY = draw_xy_maps(map,
                e0lims  = e0_limits,
                ltlims  = lt_limits,
                eulims  = (0, eu_limits_up),
                lulims  = (0, ltu_limits_up),
                figsize=(12,10), cmap='coolwarm')

    # To do: make a movie for all ts
    #plot_xy_all_time_movie()
    #plot_xy_average_time()
    return map, fig_nXY, fig_XY
