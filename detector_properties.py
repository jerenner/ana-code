import numpy as np
import matplotlib.pyplot as plt

from iminuit     import Minuit, describe
from probfit     import BinnedChi2, Extended

from invisible_cities.core .core_functions import in_range
from plotting_functions import plot_residuals_E_reso_gaussC
from control_plots import labels, hist

def gaussC(x, mu, sigma, N, Ny):
    return N * np.exp(-0.5 *np.power((x - mu)/(sigma),2)) + Ny

def gauss(x, mu, sigma, N):
    return N * np.exp(-0.5 * np.power((x - mu)/(sigma),2))


def energy_resolution(plots_dir, dst, label=''):
    """
    Input s2 energy signal
    Return value for the energy resolution
    """

    fit_erange = (4500,5300)

    # To do: work in the plotting

    plt.figure(figsize=(7,5))
    #fig = plt.figure(figsize=(8,6))
    #ax      = fig.add_subplot(5, 2, 1)
    chi2 = BinnedChi2(gaussC, dst.S2e, bins = 50 , bound = fit_erange) #create cost function
    chi2.show(args={'mu':4900, 'sigma':70, 'N':400, 'Ny':25})  #another way to draw it

    plt.figure(figsize=(7,5))
    #ax      = fig.add_subplot(5, 2, 2)
    m = Minuit(chi2, mu=4900, sigma=70, N=400, Ny=25)
    m.migrad()
    chi2.show(m)
    #plt.show()

    mean     = minuit.values[0]
    mean_u   = minuit.errors[0]

    sigma    = minuit.values[1]
    sigma_u  = minuit.errors[1]

    N       = minuit.values[2]
    N_u     = minuit.errors[2]

    N2        = minuit.values[3]
    N2_u      = minuit.errors[3]

    print(f'Mean:  {mean:.2f}         +/- {mean_u:.2f} ')
    print(f'Sigma: {sigma:.2f}        +/- {sigma_u:.2f} ')
    print(f'N:     {N:.1f}            +/- {N_u:.1f} ')
    print(f'N2:    {N2:.1f}           +/- {N2_u:.1f} ')

    # Pass an Tuple instead of a long list of variables
    plt.style.use('classic')
    plot_residuals_E_reso_gaussC(plots_dir, label, dst.S2e, 50, fit_erange, mean, mean_u, sigma, sigma_u, N, N_u, N2, N2_u)

    # To do: write in another file or decide where
    #fout.write(f"Energy resolution   = {str(len(dst))}\n")

    #return reso, reso_u

def lifetime():
    """
    Input 2D distribution of s2 vs Z
    Return my calculation for lifetime without corrections
    """

    pass


def drift_velocity(plots_dir, dst, label=''):
    """
    Input Z distribution
    Return value for the drift velocity
    """
    # To do: make plotting of drift velocities as for energy resolution

    Z = dst[in_range(dst.Z, 305,350)].Z
    fit_z_range = (305,350)

    fig = plt.figure(figsize=(12,4))
    ax      = fig.add_subplot(1, 2, 1)
    (_) = hist(dst.DT, bins = 100, range = (0,400), histtype='stepfilled', color='crimson')
    labels('Drit time ($\mu$s)','Entries')
    plt.legend(loc='upper right')

    ax      = fig.add_subplot(1, 2, 2)
    (_) = hist(Z, bins = 100, range = fit_z_range, histtype='stepfilled', color='crimson')
    labels('Drit time ($\mu$s)','Entries')
    plt.legend(loc='upper right')
    plt.show()

    sigmoid  = lambda x, A, B, C, D: A / (1 + np.exp((x - B) / C)) + D
    mypdf = Extended(sigmoid)
    #describe(mypdf)
    chi2 = BinnedChi2(mypdf, Z, bins = 100 , bound= fit_z_range )#create cost function

    plt.figure(figsize=(7,5))
    chi2.show(args={'A':1400, 'B':330, 'C':1.1, 'D':43 , 'N':1}) #another way to draw it

    m = Minuit(chi2, A=800, B=330, C=1.3 , D=100 , N=1)
    m.migrad()
    my_parmloc = (0.60,0.90)
    #chi2.draw(m, parmloc=my_parmloc)
    plt.figure(figsize=(7,5))
    chi2.show(m, parmloc=my_parmloc)

    plt.savefig(f'{plots_dir}/fit_energy_reso_{label}.png')
    print('plots saved in '+ plots_dir)
