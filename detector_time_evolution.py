import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns

from control_plots import labels

from krcal.core.fitmap_functions    import time_fcs_df
from krcal.NB_utils.plt_functions   import plot_time_fcs
from krcal.core.selection_functions import get_time_series_df
from krcal.core.kr_types            import FitType
from krcal.core.map_functions   import amap_average




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
    """
    plt.figure(figsize=(8,5))
    sns.set()
    sns.set_style("white")
    sns.set_style("ticks")
    nXY = event_map_df(KXY)
    ax  = sns.heatmap(nXY, square=True,cmap='coolwarm')
    """
    pass


def xy_time_evolution_plots():
        """
        Obtain a time-series of maps (tsm) from a fit-map (fmap).
        """
        """
        # estudios en funcion de XY
        number_of_bins = 20
        print('Number of XY bins: ', number_of_bins, '(', sel_dst.event.nunique(), 'events)')
        XYbins     = (number_of_bins , number_of_bins)
        xbins = np.linspace(*x_range, XYbins[0]+1)
        ybins = np.linspace(*y_range, XYbins[1]+1)

        KXY = select_xy_sectors_df(sel_dst, xbins, ybins)
        # KXY is a DataFrameMap = Dict[int, List[DataFrame]]
        nXY = event_map_df(KXY)    # To do: obtenir el valor mes menut
        plot_num_ev_xy(nXY)

        # ?? estas 3 funciones donde se usan

        ## estamos usando 10 time bins, podemos tener falta de estadistica
        #cuando binamos demasiado ambos XY y tiempo
        fitted_map_xy = fit_map_xy_df(selection_map = KXY,
                             event_map     = nXY,
                             n_time_bins   = 10,
                             time_diffs    = dst.time.values,
                             nbins_z       = nbins_z,
                             nbins_e       = nbins_e,
                             range_z       = z_range,
                             range_e       = e_range,
                             energy        = 'S2e',
                             z             = 'Z',
                             fit           = fit_type,
                             n_min         = nmin)

        #Obtain a time-series of maps (tsm) from a fit-map (fmap).
        time_series_maps = tsmap_from_fmap(fitted_map_xy)

        ### Select a map from the time-series ts (here only one time bin ts=0)
        # To do: make a movie for all ts

        plot_xy_map_first_last_time()
        plot_xy_all_time_movie()
        plot_xy_average_time()

    """
        pass
