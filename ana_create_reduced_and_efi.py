from manage_data               import load_data, create_dirs, s1s2_selection
from manage_data               import radial_selection, energy_selection

def ana_create_reduced_and_efi(dst_out_dir, plots_dir, dir_input, run, opt_dict):
    """
    """
    rmax = int(opt_dict['rmax'])
    rfid = int(opt_dict['rfid'])

    fout_name = plots_dir+'summary.txt'
    fout = open(fout_name,'w')
    fout.write(f"----------  Summary of run {run}  ----------\n")

    dst_full = load_data(fout, dir_input, run)
    dst_s1s2 = s1s2_selection(dst_full, fout, dst_out_dir, run, rmax = rmax, save=True)
    dst_r    = radial_selection(dst_s1s2, fout, dst_out_dir, run, rfid = rfid, save=True)
    dst_e    = energy_selection(dst_r, opt_dict, fout, dst_out_dir, run, save=True)

    print(f'-----> Closing output summary file in: {fout_name}\n')
    fout.close()
    return dst_full, dst_s1s2, dst_r, dst_e
