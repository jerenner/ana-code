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
from ana_v_ereso_lt_raw         import ana_v_ereso_lt_raw
from ana_s1_s2_control_plots    import ana_time_evol_and_map_plots
from detector_corrections       import write_map_to_file
from ana_apply_corr_plot_ereso  import ana_apply_corr_plot_ereso



print("Last updated on ", time.asctime())

def main(args = None):
    print('-----> Hi there! welcome and enjoy biking with ana-code! \n')
    print("Last updated on ", time.asctime())

    # to do: comprobar que el config existe
    args     = get_parser()
    opt_dict = vars(args)

    dir_input        = opt_dict["dir_in"]
    run              = opt_dict["run"]

    dir_out = opt_dict['dir_out'] + '/'+ opt_dict["run"]
    dst_out_dir = opt_dict['dir_out'] + '/'+ opt_dict["run"] +'/kdst-reduced/'

    recreate_dir   = opt_dict['recreate_dir']

    if(recreate_dir == 'y'):
        print(f're-creating dirs!')
    else:
        print(f'Not re-creating dirs!')

    plots_dir   = opt_dict['dir_out'] + '/'+ opt_dict["run"] + '/plots/'
    maps_dir    = opt_dict['dir_out'] + '/'+ opt_dict["run"] + '/maps/'
    file_in     = dst_out_dir +  'reduced_' + run + '_' + opt_dict["file_in"]

    create_dirs(dst_out_dir, recreate_dir)
    create_dirs(plots_dir,   recreate_dir)

    #------ Analisis: create reduced 1s1 and 1s2 dst for trigger 2 R<70 --------
    #rmax = int(opt_dict['rmax'])
    #rfid = int(opt_dict['rfid'])
    #ana_create_reduced_and_efi(dst_out_dir, plots_dir, dir_input, run, opt_dict)

    #------ Analisis: create reduced 1s1 and 1s2 dst --------
    rmax = int(opt_dict['rmax'])
    rfid = int(opt_dict['rfid'])

    fout_name = f'{dir_out}/summary_{run}.txt'
    fout = open(fout_name,'w')
    #fout.write(f"----------  Summary of run {run}  ----------\n")
    fout.write(f'run {run}\n')
    #dst_full, dst_s1s2, dst_r, dst_e = ana_create_reduced_and_efi(fout, dst_out_dir, plots_dir, dir_input, run, opt_dict)
    #ana_s1_s2_control_plots(dst_full, fout, plots_dir, opt_dict, 'run'+str(run)+'_full_',                   'full')
    #ana_s1_s2_control_plots(dst_s1s2, fout, plots_dir, opt_dict, 'run'+str(run)+'_s1s2_rmax'+str(rmax)+'_', 's1s2')
    #ana_s1_s2_control_plots(dst_r,    fout, plots_dir, opt_dict, 'run'+str(run)+'_rfid'+str(rfid)+'_',      'rfid')
    #ana_s1_s2_control_plots(dst_e,    fout, plots_dir, opt_dict, 'run'+str(run)+'_esig_',                   'esig')

    ##
    dst_r = pd.read_hdf(file_in)
    print(file_in)
    ana_v_ereso_lt_raw(dst_r, fout, plots_dir, opt_dict)

    #------ Analisis: read reduced dst and make plots -------
    #dst = pd.read_hdf(file_in)
    #print(f'Events in dst : {str(dst.event.nunique())}')
    #print('Reading reduced ntuple in: ' + file_in)
    #dst_r_esig = dst_r[in_range(dst_r.S2e,s2emin s2emax)]
    #ana_s1_s2_control_plots(dst_r, plots_dir, opt_dict, 'test_run'+str(run)+'_')

    #------ Analisis: read reduced dst and make Maps and plots -------
    #create_dirs(maps_dir)
    #dst = pd.read_hdf(file_in)
    #print(f'Events in dst : {str(dst.event.nunique())}')
    #print('Reading reduced ntuple in: ' + file_in)
    #label_file_plots = opt_dict["label_file_plots"]
    #map = ana_time_evol_and_map_plots(dst, plots_dir, opt_dict, 'run' + str(run) + '_time_ev_' + label_file_plots)
    #write_map_to_file(map, opt_dict, maps_dir + str(run)+ '_bootstrap_map.h5')

    #------ Analisis: Apply corrections and plot ------
    #dst = pd.read_hdf(file_in)
    #print(f'Events in dst : {str(dst.event.nunique())}')
    #print('Reading reduced ntuple in: ' + file_in)
    #ana_apply_corr_plot_ereso(dst, opt_dict, plots_dir)


    #------ Analisis: E reso vs R and Z ------

    print(f'-----> Closing output summary file in: {fout_name}\n')
    fout.close()

if __name__ == "__main__":
        main()
