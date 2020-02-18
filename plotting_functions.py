import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from invisible_cities.core.core_functions  import shift_to_bin_centers


def gaussC(x, mu, sigma, N, Ny):
    return N * np.exp(-0.5 *np.power((x - mu)/(sigma),2)) + Ny

def gauss(x, mu, sigma, N):
    return N * np.exp(-0.5 * np.power((x - mu)/(sigma),2))


def poisson_sigma(x, default=3):
    """
    Get the uncertainty of x (assuming it is poisson-distributed).
    Set *default* when x is 0 to avoid null uncertainties.
    """
    u = x**0.5
    u[x==0] = default
    return u

def plot_residuals_E_reso_gaussC(plots_dir, label, energy, e_nbins, e_range, mu, mu_u , sigma, sigma_u, N, N_u, N2,N2_u):

    resolution = 235*sigma/mu

    sns.set()
    sns.set_style("white")
    sns.set_style("ticks")

    fig = plt.figure(figsize=(9,7))

    global_linewidth    = 2
    global_linecolor    = "r"

    # compute y values from histogram
    e_bins       =  np.linspace(*  e_range   ,   e_nbins + 1)
    entries, e   =  np.histogram(energy, e_bins)
    e            =  shift_to_bin_centers(e)
    #e_u          =  np.diff(e)[0] * 0.5
    entries_u    =  poisson_sigma(entries)
    #entries_u    =  entries**0.5

    # compute bin width
    w= (e_range[1]- e_range[0])/e_nbins

    # compute residuals
    y_from_fit    = gaussC(e, mu, sigma, N*w, N2*w )
    residuals     = (y_from_fit - entries)/ entries_u
    y_from_fit_1  = gauss(e, mu, sigma,  N*w)
    y_from_fit_2  = N2*w

    # Plot
    frame_data = plt.gcf().add_axes((.1, .3,.8, .6))

    plt.errorbar    (e, entries, entries_u, 0, "p", c="k")
    plt.plot        (e, y_from_fit, lw=global_linewidth, color=global_linecolor   )
    plt.fill_between(e, y_from_fit_1,    0,     alpha=0.3, color='')
    plt.fill_between(e, y_from_fit_2,    0,     alpha=0.5, color='pink')

    leg1 = plt.gca().legend(('fit', 'data'), loc='upper right')
    textstr = '\n'.join((
        '$\mu={:.2f}      \pm {:.2f} $'     .format(mu,mu_u),
        '$\sigma 1={:.2f} \pm {:.2f}$'      .format(sigma, sigma_u),
        '$N 1={:.2f}      \pm {:.2f}$'      .format(N, N_u),
        '$N 2={:.2f}      \pm {:.2f}$'      .format(N2, N2_u),
        '$\sigma_E/E =        {:.2f} \%  $' .format(resolution,)))


    props = dict(boxstyle='square', facecolor='white', alpha=0.5)
    plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=14,
                   verticalalignment='top', bbox=props)
    frame_data.set_xticklabels([])
    plt.ylabel("Entries")
    plt.ylim(-10)

    # set my own xlimits
    #lims = plt.xlim()
    lims = plt.xlim(e_range[0], e_range[1])
    frame_res = plt.gcf().add_axes((.1, .1, .8, .2))
    plt.plot    (lims, [0,0], "-g", lw=0.7)  # linia en 00 verde
    plt.errorbar(e, residuals, 1, 0, linestyle='None', fmt='|', c="k")
    plt.ylim(-3.9,3.9)
    plt.xlim(e_range[0], e_range[1])
    plt.xlabel("E (pes)")
    #plt.show()

    #fix: add save as option
    #plt.savefig(f'{plots_dir}/fit_energy_reso_{label}.png')
    #print('plots saved in '+ plots_dir)

    return resolution, fig
