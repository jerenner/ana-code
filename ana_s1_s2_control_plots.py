
from matplotlib.backends.backend_pdf import PdfPages

from control_plots    import s1_1d_control_plots, s2_1d_control_plots
from control_plots    import plot_energy_region_selected
from control_plots_2d import s1_2d_control_plots, s2_2d_control_plots
from manage_data      import energy_selection
from manage_data      import radial_selection
from detector_time_evolution import fit_time_evolution, fit_time_evolution
from detector_time_evolution import plot_e0_lf_chi2, xy_time_evolution

def ana_s1_s2_control_plots(dst, fout, plots_dir, opt_dict, label, label_fout):
    """
    """

    file_plots = opt_dict["label_file_plots"]
    #s1_1D_control_plots(plots_dir, dst_full, opt_dict, 'all')
    #s2_1D_control_plots(plots_dir, dst_full, opt_dict, 'all')
    pp = PdfPages(plots_dir + str(label)+ file_plots)

    fig_s1 = s1_1d_control_plots(dst, fout, plots_dir, opt_dict, 's1s2', label_fout)
    pp.savefig(fig_s1)
    fig_s2, fig_s2_2 = s2_1d_control_plots(dst, fout, plots_dir, opt_dict, 's1s2',  label_fout)
    pp.savefig(fig_s2)
    pp.savefig(fig_s2_2)
    #s1_1D_control_plots(plots_dir, dst_r, opt_dict, f'r_{rfid}')
    #s2_1D_control_plots(plots_dir, dst_r, opt_dict, f'r_{rfid}')
    fig_s1_2d, fig_s2_2d_2 = s1_2d_control_plots(dst, plots_dir, opt_dict, '')
    pp.savefig(fig_s1_2d)
    pp.savefig(fig_s2_2d_2)
    fig_s2_2d, fig_s2_2d_2, fig_s2_2d_3  = s2_2d_control_plots(dst, plots_dir, opt_dict, '')
    pp.savefig(fig_s2_2d)
    pp.savefig(fig_s2_2d_2)
    pp.savefig(fig_s2_2d_3)

    pp.close()
    print(f'Plots saved in:\n')
    print(f'{plots_dir + str(label) + file_plots}')



def ana_time_evol_and_map_plots(dst, plots_dir, opt_dict, label):
    """
    """

    run      = int(opt_dict['run'])
    r_max    = int(opt_dict['r_max'])


    fout_name = plots_dir+'Energy_Cut.txt'
    fout = open(fout_name,'w')
    fout.write(f"----------  Energy cut run {run}  ----------\n")
    dst_out_dir = plots_dir

    dst_r        = radial_selection(dst, fout, dst_out_dir, run, 70, save=False)
    dst_e        = energy_selection(dst_r, opt_dict, fout, dst_out_dir, run, save=False)

    fit_times    = fit_time_evolution(dst_e, opt_dict)
    fig = plot_energy_region_selected(dst_e, opt_dict)
    fig2 = plot_e0_lf_chi2(fit_times)
    map, fig_nXY, fig_XY = xy_time_evolution(dst_e, opt_dict)

    pp = PdfPages(plots_dir + str(label)+'.pdf')
#    fig = plot_energy_region_selected(dst_e, opt_dict)
    pp.savefig(fig)
#    fig2 = plot_e0_lf_chi2(fit_times)
    pp.savefig(fig2)
    #fig_nXY, fig_XY = xy_time_evolution(dst_e, opt_dict)
    pp.savefig(fig_nXY)
    pp.savefig(fig_XY)

    pp.close()
    print(f'Plots saved in:\n')
    print(f'{plots_dir}{str(label)}.pdf')

    return map
