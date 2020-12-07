import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from invisible_cities.core.core_functions  import shift_to_bin_centers
from ana_stat import error_on_a_fraction

from stat_fit_pdf import *

def plot_residuals_Normalized(pdf_tot, pdf_sig, pdf_bkg,
                              energy, e_nbins, fit_range,
                              mu, mu_u,
                              sigma, sigma_u,
                              N, N_u,
                              C, C_u,
                              s, s_u,
                              chi2, cov,
                              plots_dir, label):

    # compute y values from histogram
    e_bins       =  np.linspace(*  fit_range   ,   e_nbins + 1)
    entries, e   =  np.histogram(energy, e_bins)
    e            =  shift_to_bin_centers(e)
    entries_u    =  poisson_sigma(entries)

    # compute bin width
    w= (fit_range[1]- fit_range[0])/e_nbins
    print(print(e[0]))

    # compute residuals
    y_from_tot_fit    = pdf_tot(e, mu, sigma, N*w, C*w, s, fit_range[0], fit_range[1])
    residuals         = (y_from_tot_fit - entries)/ entries_u
    y_from_sig_fit    = pdf_sig(e, mu, sigma,  N*w)
    y_from_bkg_fit    = pdf_bkg(e, C*w, s, fit_range[0], fit_range[1])

    # resolution
    resolution = 235*sigma/mu
    reso_u     = 235*error_on_a_fraction(sigma, sigma_u, mu, mu_u, cov)

    # compute x and y so that red lines goes till end of plot and not center of bin

    e_extra = np.hstack([e[0]-w, e, e[-1]+w])
    y_from_tot_fit_extra  = pdf_tot(e_extra, mu, sigma, N*w, C*w, s, fit_range[0], fit_range[1])
    y_from_bkg_fit_extra  = pdf_bkg(e_extra, C*w, s, fit_range[0], fit_range[1])

    # Plot

    sns.set()
    sns.set_style("white")
    sns.set_style("ticks")

    global_linewidth    = 2.5

    fig = plt.figure(figsize=(9,7))

    frame_data = plt.gcf().add_axes((.1, .3,.8, .6))

    plt.plot        (e_extra, y_from_tot_fit_extra,   lw=global_linewidth, color= 'r', label = 'Signal', zorder=1  )
    plt.errorbar    (e,       entries, entries_u,   0, "p", c="k", label = f'data {label}',zorder=5)
    plt.fill_between(e,       y_from_sig_fit,       0, alpha=0.3, color='none',     linewidth=0.0, zorder=4)
    plt.fill_between(e_extra, y_from_bkg_fit_extra, 0, alpha=0.5, color="none",      hatch='\\\\', edgecolor="darkgreen", linewidth=0.0, label = 'Background', zorder=3)
    plt.plot        (e,       y_from_bkg_fit, 0, alpha=0.5, color="darkgreen", zorder=2)

    plt.legend( loc='upper right', numpoints = 1, fontsize=15, frameon=False )


    textstr = '\n'.join((
        '$\mu={:.4f}      \pm {:.4f} $'     .format(mu,mu_u),
        '$\sigma ={:.4f} \pm {:.4f}$'      .format(sigma, sigma_u),
        '$N\_sig={:.0f}      \pm {:.0f}$'      .format(N, N_u),
        '$N\_bkg={:.0f}         \pm {:.0f}$'      .format(C, C_u),
       # '$s={:.2f}         \pm {:.2f}$'      .format(s, s_u),
        '$\sigma_E/E = ({:.2f} \pm {:.2f}) \%  $' .format(resolution,reso_u),
        f'$\chi^2 = {chi2:.2f}$'
    ))


    props = dict(boxstyle='square', facecolor='white', alpha=0.5)
    plt.gca().text(0.05, 0.85, textstr, transform=plt.gca().transAxes, fontsize=15,
                   verticalalignment='top', bbox=props)

    plt.gca().text(0.05, 0.95, 'NEXT-DEMO++', transform=plt.gca().transAxes, fontsize=17,fontweight='bold',
                   verticalalignment='top', bbox=props)

    frame_data.set_xticklabels([])

    plt.ylabel("Entries")
    plt.ylim(0)

    # set my own xlimits
    lims = plt.xlim(fit_range[0], fit_range[1])
    frame_res = plt.gcf().add_axes((.1, .1, .8, .2))
    plt.plot    (lims, [0,0], "black", lw=0.7, linestyle='dashed')  # linia en 00 verde
    plt.errorbar(e, residuals, 1, 0, "p", c="k")
    plt.ylim(-3.9,3.9)
    plt.xlim(fit_range[0], fit_range[1])
    plt.xlabel("E (MeV)")

    return resolution, fig

def plot_residuals_E_reso_gaussC(plots_dir, label, energy, e_nbins, e_range, mu, mu_u , sigma, sigma_u, N, N_u, N2,N2_u, chi2_val):

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

    plt.errorbar    (e, entries, entries_u, 0, "p", c="k", label = 'data')
    plt.plot        (e, y_from_fit, lw=global_linewidth, color=global_linecolor, label = 'fit'  )
    plt.fill_between(e, y_from_fit_1,    0,     alpha=0.3, color='')
    plt.fill_between(e, y_from_fit_2,    0,     alpha=0.5, color='pink')
    plt.legend( loc='upper right', numpoints = 1 )


    textstr = '\n'.join((
        '$\mu={:.2f}      \pm {:.2f} $'     .format(mu,mu_u),
        '$\sigma 1={:.2f} \pm {:.2f}$'      .format(sigma, sigma_u),
        '$N 1={:.2f}      \pm {:.2f}$'      .format(N, N_u),
        '$N 2={:.2f}      \pm {:.2f}$'      .format(N2, N2_u),
        '$\sigma_E/E =        {:.2f} \%  $' .format(resolution,),
        f'$\chi^2 = {chi2_val:.2f}$'
    ))



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

def plot_residuals_E_reso_gauss(plots_dir, label, energy, e_nbins, e_range, mu, mu_u , sigma, sigma_u, N, N_u, chi2_val, cov):

    resolution = 235*sigma/mu
    reso_u     = 235*error_on_a_fraction(sigma, sigma_u, mu, mu_u, cov)

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
    y_from_fit    = gauss(e, mu, sigma, N*w)
    residuals     = (y_from_fit - entries)/ entries_u
    y_from_fit_1  = gauss(e, mu, sigma,  N*w)
    #y_from_fit_2  = N2*w
    # Plot
    frame_data = plt.gcf().add_axes((.1, .3,.8, .6))

    plt.errorbar    (e, entries, entries_u, 0, "p", c="k", label = f'data {label}')
    plt.plot        (e, y_from_fit, lw=global_linewidth, color=global_linecolor, label = 'fit'  )
    plt.fill_between(e, y_from_fit_1,    0,     alpha=0.3, color='')
    #plt.fill_between(e, y_from_fit_2,    0,     alpha=0.5, color='pink')
    plt.legend( loc='upper right', numpoints = 1 )

    textstr = '\n'.join((
        '$\mu={:.3f}      \pm {:.4f} $'     .format(mu,mu_u),
        '$\sigma 1={:.3f} \pm {:.4f}$'      .format(sigma, sigma_u),
        '$N 1={:.2f}      \pm {:.2f}$'      .format(N, N_u),
        #'$N 2={:.2f}      \pm {:.2f}$'      .format(N2, N2_u),
        '$\sigma_E/E = ({:.2f} \pm {:.2f}) \%  $' .format(resolution,reso_u),
        f'$\chi^2 = {chi2_val:.2f}$'
    ))


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
    plt.xlabel("E (MeV)")
    #plt.show()

    #fix: add save as option
    #plt.savefig(f'{plots_dir}/fit_energy_reso_{label}.png')
    #print('plots saved in '+ plots_dir)

    return resolution, fig


def plot_residuals_E_reso_gaussC_v2(plots_dir, label, energy, e_nbins, e_range, mu, mu_u , sigma, sigma_u, N, N_u, N2, N2_u, chi2_val, cov):

    resolution = 235*sigma/mu
    reso_u     = 235*error_on_a_fraction(sigma, sigma_u, mu, mu_u, cov)

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

    plt.errorbar    (e, entries, entries_u, 0, "p", c="k", label = f'data {label}')
    plt.plot        (e, y_from_fit, lw=global_linewidth, color=global_linecolor, label = 'fit'  )
    plt.fill_between(e, y_from_fit_1,    0,     alpha=0.3, color='')
    plt.fill_between(e, y_from_fit_2,    0,     alpha=0.5, color='pink')
    plt.legend( loc='upper right', numpoints = 1 )

    textstr = '\n'.join((
        '$\mu={:.3f}      \pm {:.4f} $'     .format(mu,mu_u),
        '$\sigma 1={:.3f} \pm {:.4f}$'      .format(sigma, sigma_u),
        '$N 1={:.2f}      \pm {:.2f}$'      .format(N, N_u),
        '$N 2={:.2f}      \pm {:.2f}$'      .format(N2, N2_u),
        '$\sigma_E/E = ({:.2f} \pm {:.2f}) \%  $' .format(resolution,reso_u),
        f'$\chi^2 = {chi2_val:.2f}$'
    ))


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
    plt.xlabel("E (MeV)")
    #plt.show()

    #fix: add save as option
    #plt.savefig(f'{plots_dir}/fit_energy_reso_{label}.png')
    #print('plots saved in '+ plots_dir)

    return resolution, fig



def plot_residuals_E_reso_gaussPoly1(plots_dir, label, energy, e_nbins, e_range, mu, mu_u , sigma, sigma_u, N, N_u, A, A_u, B, B_u, chi2_val, cov):

    resolution = 235*sigma/mu
    reso_u     = 235*error_on_a_fraction(sigma, sigma_u, mu, mu_u, cov)

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
    print(f'bin width = {w}')

    # compute residuals
    y_from_fit    = gaussPoly1(e, mu, sigma, N*w, A*w, B*w )
    residuals     = (y_from_fit - entries)/ entries_u
    y_from_fit_1  = gauss(e, mu, sigma,  N*w)
    y_from_fit_2  = poly1(e, A*w, B*w)

    # Plot
    frame_data = plt.gcf().add_axes((.1, .3,.8, .6))

    plt.errorbar    (e, entries, entries_u, 0, "p", c="k", label = f'data {label}')
    plt.plot        (e, y_from_fit, lw=global_linewidth, color=global_linecolor, label = 'fit'  )
    plt.fill_between(e, y_from_fit_1,    0,     alpha=0.3, color='')
    plt.fill_between(e, y_from_fit_2,    0,     alpha=0.5, color='pink')
    plt.legend( loc='upper right', numpoints = 1 )

    textstr = '\n'.join((
        '$\mu={:.3f}      \pm {:.4f} $'     .format(mu,mu_u),
        '$\sigma 1={:.3f} \pm {:.4f}$'      .format(sigma, sigma_u),
        '$N 1={:.2f}      \pm {:.2f}$'      .format(N, N_u),
        '$A 2={:.2f}      \pm {:.2f}$'      .format(A, A_u),
        '$B 2={:.4f}      \pm {:.4f}$'      .format(B, B_u),
        '$\sigma_E/E = ({:.2f} \pm {:.2f}) \%  $' .format(resolution,reso_u),
        f'$\chi^2 = {chi2_val:.2f}$'
    ))


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
    plt.xlabel("E (MeV)")
    #plt.show()

    #fix: add save as option
    #plt.savefig(f'{plots_dir}/fit_energy_reso_{label}.png')
    #print('plots saved in '+ plots_dir)

    return resolution, fig


#to be continued with notebook: /Users/neus/current-work/NB/NB-Zeffect-JulyCM/Ereso_Zeffect_lowEL_Run4_15_15.ipynb
def plot_residuals_E_reso_gaussExp(plots_dir, zlabel, energy, e_nbins, e_range, mu, mu_u , sigma, sigma_u, N, N_u, C, C_u, s, s_u, chi2, cov):


    resolution = 235*sigma/mu
    reso_u     = 235*error_on_a_fraction(sigma, sigma_u, mu, mu_u, cov)

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
    y_from_fit    = gaussExp(e, mu, sigma, N*w, C*w, s )
    residuals     = (y_from_fit - entries)/ entries_u
    y_from_fit_1  = gauss(e, mu, sigma,  N*w)
    y_from_fit_2  = bkgExp(e, C*w, s)

    # Plot
    frame_data = plt.gcf().add_axes((.1, .3,.8, .6))

    plt.errorbar    (e, entries, entries_u, 0, "p", c="k", label = f'data {zlabel}')
    plt.plot        (e, y_from_fit, lw=global_linewidth, color=global_linecolor, label = 'fit'  )
    plt.fill_between(e, y_from_fit_1,    0,     alpha=0.3, color='')
    plt.fill_between(e, y_from_fit_2,    0,     alpha=0.5, color='pink')
    plt.legend( loc='upper right', numpoints = 1 )


    textstr = '\n'.join((
        '$\mu={:.3f}      \pm {:.4f} $'     .format(mu,mu_u),
        '$\sigma 1={:.3f} \pm {:.4f}$'      .format(sigma, sigma_u),
        '$N 1={:.2f}      \pm {:.2f}$'      .format(N, N_u),
        '$C={:.0E}         \pm {:.0E}$'      .format(C, C_u),
        '$s={:.2f}         \pm {:.2f}$'      .format(s, s_u),
        '$\sigma_E/E = ({:.2f} \pm {:.2f}) \%  $' .format(resolution,reso_u),
        f'$\chi^2 = {chi2:.2f}$'
    ))


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
    plt.xlabel("E (MeV)")
    #plt.show()

    #fix: add save as option
    #plt.savefig(f'{plots_dir}/fit_energy_reso_{label}.png')
    #print('plots saved in '+ plots_dir)

    return resolution, fig
