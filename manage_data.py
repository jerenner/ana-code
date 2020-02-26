import os
import shutil
import numpy  as np
import pandas as pd

from  invisible_cities.io.dst_io import load_dsts
from  invisible_cities.core .core_functions import in_range

def save_dst_to_file(dst, dir_file):
    """
    Input path and file name to write a dst
    Output dst written to disk
    """
    dst = dst.sort_values('event')
    store = pd.HDFStore(dir_file, "w", complib=str("zlib"), complevel=4)
    store.put('dataframe', dst, format='table', data_columns=True)
    store.close()


def create_dirs(dir):
    """
    Input directory name
    Output creates directory
    """
    #  to do: si escribimos ENTER que sea equivalente a NO

    print('Do you want to overwrite? :' + dir)
    answer = input()
    if answer == 'y':
        overwrite = True
    else:
        overwrite = False
    print(overwrite)

    if os.path.exists(dir) and overwrite:
        shutil.rmtree(dir)
    try:
        os.makedirs(dir)
    except OSError:
        print (f'Creation of dir: {dir} failed')
    else:
        print (f'Successfully created dir: {dir}')


def load_data(fout, dir_in, run):
    """
    Input path to all dst files
    Return a merged dst
    ------
    Note: In the kdst there are duplicated events because of the
    multiplicity from both s1 and s2
    Note two: dst.event.nunique returns int. (Panda.Series.nunique)
    if used in Panda.Dataframe.nunique returns Series with unique entries
    """

    path        = dir_in + '/' + run + '/kdst/'
    files_all   = [path + f for f in os.listdir(path) \
                  if os.path.isfile( os.path.join(path, f) )]
    dst         = load_dsts(files_all, "DST", "Events")

    # count number of number of unique entries
    unique_events = ~dst.event.duplicated()
    #unique_events = dst.event.nunique()
    nunique_events = dst.event.nunique()

    print(nunique_events)

    num_of_S2s  = np.size         (unique_events)
    num_of_evts = np.count_nonzero(unique_events)

    print(num_of_evts)
    fout.write(f"Entries in dst    = {str(len(dst))}\n")
    fout.write(f"Number of S2s     = {num_of_S2s} \n")
    fout.write(f"Number of events  = {num_of_evts}\n")

    return dst

def s1s2_selection(dst, fout, dst_out_dir, run, save=False):
    """
    Input one file with a dst dataframe and run number
    Returns dst and writes to disk a reduced dst with events that pass
    the 1s1 and 1s2 selection criteria
    """

    dst_s1  = dst     [in_range(dst.nS1,    1,2)]
    dst_s2  = dst_s1  [in_range(dst_s1.nS2, 1,2)]

    tot_ev  = dst.   event.nunique()
    s1_ev   = dst_s1.event.nunique()
    s1s2_ev = dst_s2.event.nunique()

    eff_s1   = s1_ev   / tot_ev
    eff_s2   = s1s2_ev / tot_ev
    eff_s1s2 = s1s2_ev / s1_ev

    fout.write(f'Abs. Eff 1s1:          {np.round(eff_s1*100,2)}%   ({s1_ev}   / {tot_ev})\n')
    fout.write(f'Abs. Eff 1 s1&s2:      {np.round(eff_s2*100,2)}%   ({s1s2_ev} / {tot_ev})\n')
    fout.write(f'Rel. eff 1s2 from 1s1: {np.round(eff_s1s2*100,2)}%   ({s1s2_ev} / {s1_ev})\n')


    if save:
        dir_file_name = f'{dst_out_dir}/reduced_{run}_kdst.h5'
        save_dst_to_file(dst_s2, dir_file_name)
        print(f'Save reduced kdst with 1s1 and 1s2 in: {dir_file_name}')

    return dst_s2

def radial_selection(dst,rfid, fout, dst_out_dir, run, save=False):
    """
    Input a dst
    Return dst with radial requirement applied
    """

    rfid     = int(rfid)
    dst_rfid = dst[in_range(dst.R,0,rfid)]
    tot_ev   = dst.event.nunique()
    rfid_ev  = dst_rfid.event.nunique()
    eff      = rfid_ev/tot_ev

    fout.write(f'Rel. Eff R < {rfid}: {np.round(eff*100,2)}%  ({rfid_ev} / {tot_ev})\n')

    if save:
        dir_file_name = f'{dst_out_dir}/reduced_{run}_kdst_{rfid}.h5'
        save_dst_to_file(dst_rfid, dir_file_name)
        print(f'Save reduced kdst with R < {rfid} : {dir_file_name}')

    return dst_rfid

def energy_selection(dst, opt_dict, fout, dst_out_dir, run, save=False):
    """
    Input a dst
    Return dst with energy range requirement applied
    """

    emin   = float(opt_dict["s2e_sig_min"])
    emax   = float(opt_dict["s2e_sig_max"])
    dst_e = dst[in_range(dst.S2e,emin,emax)]

    tot_ev     = dst.event.nunique()
    energy_ev  = dst_e.event.nunique()
    eff        = energy_ev/tot_ev

    fout.write(f'Rel. Eff e = [{emin, emax}]: {np.round(eff*100,2)}%    ({energy_ev} / {tot_ev}\n)')

    if save:
        dir_file_name = f'{dst_out_dir}/reduced_{run}_kdst_emin{emin}_emax{emax}.h5'
        save_dst_to_file(dst_e, dir_file_name)
        print(f'Save reduced kdst with e = [{emin,emax}]: {dir_file_name}')

    return dst_e
