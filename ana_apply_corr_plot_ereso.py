from detector_corrections      import apply_corrections
from energy_resolution_vs_z_r  import energy_reso_vs_z_r


def ana_apply_corr_plot_ereso(dst, opt_dict, plots_dir):
    """
    """

    file_map          = opt_dict["file_map"]
    file_fits         = opt_dict["file_fits"]
    file_e_vs_z_r     = opt_dict["file_e_vs_z_r"]
    is_ring           = opt_dict["is_ring"]

    print(f'in main ring = {is_ring}')
    corr = apply_corrections(dst, file_map)
    print(f'-----> Corrections applied, time spent = \n')

    energy_reso_vs_z_r(dst, corr, plots_dir+'ring_'+is_ring+'_'+file_fits, plots_dir+'ring_'+is_ring+'_'+file_e_vs_z_r, ring = is_ring)
