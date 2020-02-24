
from control_plots    import s1_1d_control_plots, s2_1d_control_plots
from control_plots_2d import s1_2d_control_plots, s2_2d_control_plots
from matplotlib.backends.backend_pdf import PdfPages


def ana_s1_s2_control_plots(dst, plots_dir, opt_dict, label):
    """
    """

    file_plots = opt_dict["file_plots"]
    #s1_1D_control_plots(plots_dir, dst_full, opt_dict, 'all')
    #s2_1D_control_plots(plots_dir, dst_full, opt_dict, 'all')
    pp = PdfPages(plots_dir + str(label)+ file_plots)

    fig_s1 = s1_1d_control_plots(dst, plots_dir, opt_dict, 's1s2')
    pp.savefig(fig_s1)
    fig_s2, fig_s2_2 = s2_1d_control_plots(dst, plots_dir, opt_dict, 's1s2')
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
