from krcal.core.selection_functions  import select_xy_sectors_df
from krcal.core.selection_functions  import event_map_df
from krcal.core.fitmap_functions     import fit_map_xy_df

from krcal.core.map_functions        import tsmap_from_fmap
from krcal.core.map_functions        import amap_from_tsmap
from krcal.core.map_functions        import add_mapinfo
from krcal.core.io_functions         import write_complete_maps

from krcal.map_builder.map_builder_functions  import e0_xy_correction
from invisible_cities.reco.corrections_new    import apply_all_correction
from invisible_cities.reco.corrections_new    import read_maps   #  ---> check file to see NEW dependencies

def create_corrections_map():
    """
    Input dst
    Return dst with applied apply corrections from ICAROS package
    """
    """

    nbins_z    = 25
    nbins_e    = 25
    z_range    = (10,350)
    e_range    = (3800,5300)
    nmin       = 60  #?

    r_max = 70

    # estudios en funcion de XY

    # calcular mapa

    bootstrap = calculate_map(dst        = sel_dst ,
                     XYbins     = (number_of_bins ,
                                   number_of_bins),
                     nbins_z    = nbins_z         ,
                     nbins_e    = nbins_e         ,
                     z_range    = z_range         ,
                     e_range    = e_range         ,
                     chi2_range = chi2_range      ,
                     lt_range   = lt_range        ,
                     fit_type   = FitType.unbined ,
                     nmin       = nmin            ,
                     x_range    = x_range         ,
                     y_range    = y_range         )

    check_failed_fits(maps      = bootstrap          ,
                  maxFailed = maxFailed     ,
                  nbins     = number_of_bins,
                  rmax      = r_max         ,
                  rfid      = r_max         )

    draw_xy_maps(bootstrap, e0lims  = (3500,5500))
    bootstrap = add_mapinfo(asm        = bootstrap,
                   xr         = (-70, 70),
                   yr         = (-70, 70),
                   nx         = 40       ,
                   ny         = 40       ,
                   run_number = 6721     )

    regularized_maps = regularize_map(maps = bootstrap,                    ,
                                  x2range = chi2_range)
    regularized_maps = relative_errors(am = regularized_maps)
    regularized_maps = remove_peripheral(map   = regularized_maps,
                                     nbins = number_of_bins  ,
                                     rmax  = r_max           ,
                                     rfid  = r_max           )

    draw_xy_maps(regularized_maps,
             e0lims  = (4200,5000),
             ltlims  = (0, 100000),
             eulims  = (0.0,  0.03),
             lulims  = (0, 0.4),
             figsize=(14,10))

    bootstrap = add_mapinfo(asm        = bootstrap,
                   xr         = (-70, 70),
                   yr         = (-70, 70),
                   nx         = 40       ,
                   ny         = 40       ,
                   run_number = 6721     )

    bootstrap_f = '/Users/neus/current-work/ana-results/6721/maps/bootstrap_test_6721.h5'
    write_complete_maps(asm  = bootstrap  ,
                    filename = bootstrap_f)

    """
    pass


def apply_corrections(dst, map_file):
        """
        ### E0 correction:
        - Computes the energy vector corrected by geometry in bins of XY
        (from the XY map above).
        - e0_xy_correction The signal correction factor f (x, y) is simply the inverse of the
        mean of the gaussian distribution in each (x, y) bin, normalized to
        a constant factor which can be chosen as
        the maximum energy bin: E0M = emaps.e0 / norm.e0
        """

        map = read_maps(map_file)
        geom_corr = e0_xy_correction(map)

        total_correction = apply_all_correction(map, apply_temp=True)
        corr_geo = geom_corr(dst.X, dst.Y)
        corr_tot = total_correction(dst.X, dst.Y, dst.Z, dst.time)

        return corr_tot
