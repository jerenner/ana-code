
from matplotlib.backends.backend_pdf import PdfPages

import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns

from iminuit     import Minuit, describe
from probfit     import BinnedChi2, Extended

from invisible_cities.core.core_functions import in_range
from plotting_functions import plot_residuals_E_reso_gaussC
from control_plots      import labels, hist
from plotting_functions import gaussC
from energy_resolution_vs_z_r import plot_fits



def ana_v_ereso_lt_raw(dst, plots_dir, opt_dict):
    """
    """
    run              = opt_dict["run"]

    pp = PdfPages(plots_dir+'/fit_ereso_dv_lt_'+run+'.pdf')
    fig_e = energy_resolution(dst, plots_dir, opt_dict)
    #pp.savefig(fig_e)
    #fig_dv = drift_velocity(dst, plots_dir, opt_dict)
    #pp.savefig(fig_dv)
    #pp.close()
    #print(f'Plots saved in:\n')
    #print(f'{plots_dir}/fit_ereso_dv_lt_{run}.pdf')

def energy_resolution(dst, plots_dir, opt_dict):

    run              = opt_dict["run"]
    fit_e_min   = float(opt_dict["fit_e_min"])
    fit_e_max   = float(opt_dict["fit_e_max"])
    fit_seed    = float(opt_dict["fit_seed"])
    fit_erange = (fit_e_min, fit_e_max)

    chi2 = BinnedChi2(gaussC, dst.S2e, bins = 50 , bound = fit_erange)
    m = Minuit(chi2, mu = fit_seed, sigma = 90, N = 10, Ny = 0)
    m.migrad()
    reso, fig = plot_fits(dst, 1, fit_erange, m)

    print(f'Resolution = {reso}')
    plt.savefig(f'{plots_dir}/fit_energy_reso_{run}.pdf')
    plt.savefig(f'/Users/neus/current-work/ana-reso/fit_energy_reso_{run}.pdf')
    print(f'plots saved in {plots_dir}fit_energy_reso_{run}.pdf')
    print(f'plots saved in /Users/neus/current-work/ana-reso/fit_energy_reso_{run}.pdf')

    return fig

def drift_velocity(dst, plots_dir, opt_dict):

    length_demo = 310

    run              = opt_dict["run"]
    fit_z_min   = float(opt_dict["fit_z_min"])
    fit_z_max   = float(opt_dict["fit_z_max"])
    fit_z_range = (fit_z_min, fit_z_max)

    print(f'fit z range =  {fit_z_range}')

    Z = dst[in_range(dst.Z, fit_z_min, fit_z_max)].Z
    sigmoid  = lambda x, A, B, C, D: A / (1 + np.exp((x - B) / C)) + D
    mypdf = Extended(sigmoid)
    #describe(mypdf)
    bx2 = BinnedChi2(mypdf, Z, bins = 50 , bound= fit_z_range )#create cost function
    #bx2.show(args={'A':1400, 'B':340, 'C':1.1, 'D':43 , 'N':0.1}) #another way to draw it
    m = Minuit(bx2, A=1400, B=340, C=1.1, D=43, N=0.1)
    m.migrad()
    my_parmloc = (0.60,0.90)
    bx2.draw(m, parmloc=my_parmloc)


    v = length_demo/m.args[1]
    print(v)
    v_err = (length_demo-2)/(m.args[1]-m.errors[1])
    v_u = v - v_err
    print(f"Drift velocity = {v:.4f} +/- {v_u:.4f} ")

    plt.savefig(f'{plots_dir}/fit_drift_vel_{run}.pdf')
    print(f'plots saved in {plots_dir}/fit_drift_vel_{run}.pdf')
