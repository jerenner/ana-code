import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from iminuit     import Minuit, describe
from probfit     import BinnedChi2, Extended

from invisible_cities.core.core_functions import in_range
from plotting_functions import plot_residuals_E_reso_gaussC
from control_plots      import labels, hist
from plotting_functions import gaussC

def select_dst_ring_r_z(dst, bins_r, bins_z, index_r, index_z):
    #print(bins_r[index_r], bins_z[index_z])

    print(f'Cut in R range    = {bins_r[index_r]}, {bins_r[index_r+1]} \
          and Cut in Z range = {bins_z[index_z]}, {bins_z[index_z+1]}')

    sel_r = in_range(dst.R, bins_r[index_r], bins_r[index_r+1] )
    sel_z = in_range(dst.Z, bins_z[index_z], bins_z[index_z+1])
    sel   = sel_r & sel_z
    #print(sel)
    return dst[sel]

def select_dst_disk_r_z(dst, bins_r, bins_z, index_r, index_z):
    #print(bins_r[index_r], bins_z[index_z])

    print(f'Cut in R range    = {bins_r[0]}, {bins_r[index_r+1]} \
          and Cut in Z range = {bins_z[0]}, {bins_z[index_z+1]}')

    sel_r = in_range(dst.R, bins_r[0], bins_r[index_r+1] )
    sel_z = in_range(dst.Z, bins_z[0], bins_z[index_z+1])
    sel   = sel_r & sel_z
    return dst[sel]


def plot_fits(dst_inrange, corr, fit_erange, m, chi2_val):

    mean     = m.values[0]
    mean_u   = m.errors[0]

    sigma    = m.values[1]
    sigma_u  = m.errors[1]

    N       = m.values[2]
    N_u     = m.errors[2]

    N2        = m.values[3]
    N2_u      = m.errors[3]

    print(f'Mean:  {mean:.2f}         +/- {mean_u:.2f} ')
    print(f'Sigma: {sigma:.2f}        +/- {sigma_u:.2f} ')
    print(f'N:     {N:.1f}            +/- {N_u:.1f} ')
    print(f'N2:    {N2:.1f}           +/- {N2_u:.1f} ')


    plt.style.use('classic')
    reso, fig = plot_residuals_E_reso_gaussC('', '', dst_inrange.S2e*corr, 50, fit_erange, mean, mean_u, sigma, sigma_u, N, N_u, N2, N2_u, chi2_val)

    return reso, fig


def plot_e_resolution_vs_z_r(reso_list, file_plot):

    bins_r = (0,30,40,50,60,65)
    bins_z = (0,50,100,150,200,250,300)

    same_R_30 =  reso_list [0:6]
    same_R_40 =  reso_list [6:12]
    same_R_50 =  reso_list [12:18]
    same_R_60 =  reso_list [18:24]
    same_R_70 =  reso_list [24:30]

    same_Z_50  = [reso_list[i] for i in [0,6,12,18,24]]
    same_Z_100 = [reso_list[i] for i in[1,7,13,19,25]]
    same_Z_150 = [reso_list[i] for i in[2,8,14,20,26]]
    same_Z_200 = [reso_list[i] for i in[3,9,15,21,27]]
    same_Z_250 = [reso_list[i] for i in[4,10,16,22,28]]
    same_Z_300 = [reso_list[i] for i in[5,11,17,23,29]]

    r = (30,40,50,60,65)
    z = (50,100,150,200,250,300)

    pp = PdfPages(file_plot)
    fig = plt.figure(figsize=(9,7))

    #fig = plt.figure(figsize=(13,10))
    #ax      = fig.add_subplot(2, 2, 1)
    plt.plot(z, same_R_30, color='pink', marker='o', markeredgecolor='white', linestyle='dotted', label='R [0,30]')
    plt.plot(z, same_R_40, color='crimson', marker='o', markeredgecolor='white', linestyle='dotted', label='R [30,40]')
    plt.plot(z, same_R_50, color='fuchsia', marker='o', markeredgecolor='white', linestyle='dotted', label='R [40,50]')
    plt.plot(z, same_R_60, color='royalblue', marker='o', markeredgecolor='white', linestyle='dotted', label='R [50,60]')
    plt.plot(z, same_R_70, color='steelblue', marker='o', markeredgecolor='white', linestyle='dotted', label='R [60,70]')

    labels('Z (mm)','Resolution FWHM (%)','')
    plt.legend(loc='upper right', ncol=3)
    plt.xlim(0,350)
    plt.ylim(3.5,8.5)
    pp.savefig(fig)

    fig = plt.figure(figsize=(9,7))
    #ax      = fig.add_subplot(2, 2, 2)
    plt.plot(r, same_Z_50, color='yellow', marker='o', markeredgecolor='white', linestyle='dotted', label='Z [0,50]')
    plt.plot(r, same_Z_100, color='gold', marker='o', markeredgecolor='white', linestyle='dotted', label='Z [50,100]')
    plt.plot(r, same_Z_150, color='orange', marker='o', markeredgecolor='white', linestyle='dotted', label='Z [100,150]')
    plt.plot(r, same_Z_200, color='lightgreen', marker='o', markeredgecolor='white', linestyle='dotted', label='Z [150,200]')
    plt.plot(r, same_Z_250, color='yellowgreen', marker='o', markeredgecolor='white', linestyle='dotted', label='R [200,250]')
    plt.plot(r, same_Z_300, color='olive', marker='o', markeredgecolor='white', linestyle='dotted', label='R [250,300]')

    labels('R (mm)','Resolution FWHM (%)','')
    plt.legend(loc='upper right', ncol=3)
    plt.xlim(20,75)
    plt.ylim(4,7.5)
    pp.savefig(fig)
    pp.close()

    print(f'-----> Plot of energy resolution vs z and r saved in {file_plot}\n')

def energy_reso_vs_z_r(dst, corr, file_fits, file_plot, ring = 'yes'):
    """

    """

    pp = PdfPages(file_fits)

    fit_erange = (4700,5250)

    bins_r = (0,30,40,50,60,70)
    bins_z = (0,50,100,150,200,250,300)

    #bins_r = (0,30)
    #bins_z = (0,50,100)

    dst_list = []
    reso_list = []
    num = 0

    print(f'-----> Start fits to dst selected by r and z ranges\n')

    for i in range(len(bins_r)-1):
        for j in range(len(bins_z)-1):
            if ring == 'yes':
                dst_inrange = select_dst_ring_r_z(dst, bins_r, bins_z, i, j)
            elif ring == 'no':
                dst_inrange = select_dst_disk_r_z(dst, bins_r, bins_z, i, j)
            print(f'Region id = {num}, i index = {i}, j index = {j}')
            dst_list.append(dst_inrange)
            chi2 = BinnedChi2(gaussC, dst_inrange.S2e*corr, bins = 50 , bound = fit_erange)
            m = Minuit(chi2, mu = 4900, sigma = 70, N = 400, Ny = 25)
            m.migrad()
            reso, fig = plot_fits(dst_inrange, corr, fit_erange, m)
            reso_list.append(reso)
            pp.savefig(fig)
            num+=1
    print(f'-----> Fits saved in {file_fits}---->\n')
    pp.close()

    plot_e_resolution_vs_z_r(reso_list, file_plot)
