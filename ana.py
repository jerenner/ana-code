import os
import sys
import time
import pandas as pd
from argparse_configuration import get_parser
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

from manage_data                import create_dirs
from detector_properties        import drift_velocity, energy_resolution
from detector_corrections       import apply_corrections
from energy_resolution_vs_z_r   import energy_reso_vs_z_r
from ana_create_reduced_and_efi import ana_create_reduced_and_efi
from ana_s1_s2_control_plots    import ana_s1_s2_control_plots
from ana_s1_s2_control_plots    import ana_time_evolution_plots

print("Last updated on ", time.asctime())

def main(args = None):
    print('-----> Hi there! Let\'s look at control plots,\
    energy resolution, drift velocity and lifetime!\n')
    print("Last updated on ", time.asctime())

    # to do: comprobar que el config existe
    args     = get_parser()
    opt_dict = vars(args)

    dir_input        = opt_dict["dir_in"]
    run              = opt_dict["run"]
    label_file_plots = opt_dict["label_file_plots"]

    dst_out_dir = opt_dict['dir_out'] + '/'+ opt_dict["run"] +'/kdst-reduced/'
    plots_dir   = opt_dict['dir_out'] + '/'+ opt_dict["run"] + '/plots/'
    file_in     = dst_out_dir +  'reduced_' + run + '_' + opt_dict["file_in"]


    rfid = int(opt_dict['rfid'])

    create_dirs(plots_dir)
    create_dirs(dst_out_dir)

    #------ Analisis: create reduced 1s1 and 1s2 dst --------
    #dst_full, dst_s1s2, dst_r, dst_e = ana_create_reduced_and_efi(dst_out_dir, plots_dir, dir_input, run, opt_dict)
    #ana_s1_s2_control_plots(dst_full, plots_dir, opt_dict, 'run'+str(run)+'_full_')
    #ana_s1_s2_control_plots(dst_s1s2, plots_dir, opt_dict, 'run'+str(run)+'_s1s2_')
    #ana_s1_s2_control_plots(dst_r, plots_dir, opt_dict, 'run'+str(run)+'_rfid'+str(rfid)+'_')
    #ana_s1_s2_control_plots(dst_e, plots_dir, opt_dict, 'run'+str(run)+'_esig_')

    #------ Analisis: read reduced dst and make plots -------
    dst_r = pd.read_hdf(file_in)
    print('Reading reduced ntuple in: ' + file_in)
    #dst_r_esig = dst_r[in_range(dst_r.S2e,s2emin s2emax)]
    #ana_s1_s2_control_plots(dst_r, plots_dir, opt_dict, 'test_run'+str(run)+'_')
    ana_time_evolution_plots(dst_r, plots_dir, opt_dict, 'run'+str(run)+'_time_ev_'+label_file_plots)
    #------ Analisis: Apply corrections and plot ------

    #------ Analisis: E reso vs R and Z ------


if __name__ == "__main__":
        main()
