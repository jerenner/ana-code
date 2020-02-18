from krcal.core.fitmap_functions    import time_fcs_df
from krcal.NB_utils.plt_functions   import plot_time_fcs
from krcal.core.selection_functions import get_time_series_df

from krcal.core.map_functions   import amap_average

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


def plot_e0_lf_chi2(fitted_map_time,range_chi2,range_e0,range_lt)):
    """
    """

    pass

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

def time_evolution_plots():
    """
    XY integrated
    get_time_series_df  --> returns time series and masks to divide file/run in branches
    time_fcs_df   --> fits lifetime for a time series
    plot_time_fcs
    """
    """
    ts2, masks2 = get_time_series_df(20, (sel_dst.time.values[0],sel_dst.time.values[-1]), sel_dst)
    fitted_map_time = time_fcs_df(ts2, masks2, sel_dst,
                  nbins_z = 15,
                  nbins_e = 25,
                  range_z = (10, 320),
                  range_e = (3500, 6000),
                  energy  = 'S2e',
                  fit     = FitType.profile)


    plot_e0_lf_chi2(fitted_map_time,range_chi2,range_e0,range_lt)
    para el plot: fps2.ts
    fps2.e0u ----> preparar en el notebook
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
