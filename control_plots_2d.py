import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns

from  invisible_cities.core.system_of_units_c import units

def s1_2d_control_plots(dst, plots_dir, opt_dict, label):
    """
    """

    rmax = int(opt_dict['rmax'])

    dt_max = int(opt_dict['dt_max'])
    dt_min = int(opt_dict['dt_min'])
    dt_bin = int(opt_dict['dt_bin'])

    s1e_min   = float(opt_dict["s1e_min"])
    s1e_max   = float(opt_dict["s1e_max"])
    s1e_bin   = int(opt_dict["s1e_bin"])

    s1w_min   = float(opt_dict["s1w_min"])
    s1w_max   = float(opt_dict["s1w_max"])
    s1w_bin   = int(opt_dict["s1w_bin"])

    s1h_min   = float(opt_dict["s1h_min"])
    s1h_max   = float(opt_dict["s1h_max"])
    s1h_bin   = int(opt_dict["s1h_bin"])

    s1e_range = (s1e_min, s1e_max)
    s1h_range = (s1h_min, s1h_max)
    s1w_range = (s1w_min, s1w_max)

    r_range   = (0,rmax)
    dt_range = (dt_min, dt_max)
    xy_range  = (-rmax,  rmax)


    fig = plt.figure(figsize=(15,25))

    ax      = fig.add_subplot(5, 2, 1)
    nevt, *_  = plt.hist2d(dst.S1t/units.mus, dst.S1e,(50, 50), [dt_range, s1e_range], cmap='coolwarm')
    plt.xlabel('S1t ($\mu$s)')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 2)
    nevt, *_  = plt.hist2d(dst.S1t/units.mus, dst.S1e,(50, 50), [dt_range, s1e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S1t ($\mu$s)')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 3)
    nevt, *_  = plt.hist2d(dst.DT, dst.S1e,(50, 50), [(0,400), s1e_range], cmap='coolwarm')
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 4)
    nevt, *_  = plt.hist2d(dst.DT, dst.S1e,(50, 50), [(0,400), s1e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 5)
    nevt, *_  = plt.hist2d(dst.DT, dst.S1h,(50, 50), [(0,400), s1h_range], cmap='coolwarm')
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S1h (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 6)
    nevt, *_  = plt.hist2d(dst.DT, dst.S1h,(50, 50), [(0,400), s1h_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S1h (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 7)
    nevt, *_  = plt.hist2d(dst.DT, dst.S1w/units.mus,(50, s1w_bin), [(0,400), s1w_range], cmap='coolwarm')
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S1w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 8)
    nevt, *_  = plt.hist2d(dst.DT, dst.S1w/units.mus,(50, s1w_bin), [(0,400), s1w_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S1w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 9)
    nevt, *_  = plt.hist2d(dst.R, dst.S1e,(50, 50), [r_range, s1e_range], cmap='coolwarm')
    plt.xlabel('R (mm)')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 10)
    nevt, *_  = plt.hist2d(dst.R, dst.S1e,(50, 50), [r_range, s1e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('R')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

#### new figure
    fig_2 = plt.figure(figsize=(15,25))

    ax      = fig_2.add_subplot(5, 2, 1)
    nevt, *_  = plt.hist2d(dst.Phi, dst.S1e,(50, 50), [(-1,1), s1e_range], cmap='coolwarm')
    plt.xlabel('Phi')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 2)
    nevt, *_  = plt.hist2d(dst.Phi, dst.S1e,(50, 50), [(-1,1), s1e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Phi ')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 3)
    nevt, *_  = plt.hist2d(dst.X, dst.Y,(50, 50), [xy_range, xy_range],cmap='coolwarm')
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 4)
    nevt, *_  = plt.hist2d(dst.X, dst.Y,(50, 50), [xy_range, xy_range], normed=True, weights=dst.S1e.values, cmap='coolwarm')
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.title(None)
    plt.colorbar().set_label("S1e (pes)")
    colors.LogNorm()

    ax      = fig_2.add_subplot(5, 2, 5)
    nevt, *_  = plt.hist2d(dst.S1e, dst.X,(50, 50), [s1e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S1e (mm)')
    plt.ylabel('X (mm)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 6)
    nevt, *_  = plt.hist2d(dst.S1e, dst.Y,(50, 50), [s1e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S1e (mm)')
    plt.ylabel('Y (mm)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    print('s1 2d plots saved in '+ plots_dir)
    return fig, fig_2


def s2_2d_control_plots(dst, plots_dir, opt_dict, label):
    """
    """

    rmax = int(opt_dict['rmax'])

    dt_max = int(opt_dict['dt_max'])
    dt_min = int(opt_dict['dt_min'])
    dt_bin = int(opt_dict['dt_bin'])

    s1e_min   = float(opt_dict["s1e_min"])
    s1e_max   = float(opt_dict["s1e_max"])
    s1e_bin   = int(opt_dict["s1e_bin"])

    s2e_min   = float(opt_dict["s2e_min"])
    s2e_max   = float(opt_dict["s2e_max"])
    s2e_bin   = int(opt_dict["s2e_bin"])

    s2w_min   = float(opt_dict["s2w_min"])
    s2w_max   = float(opt_dict["s2w_max"])
    s2w_bin   = int(opt_dict["s2w_bin"])

    s2h_min   = float(opt_dict["s2h_min"])
    s2h_max   = float(opt_dict["s2h_max"])
    s2h_bin   = int(opt_dict["s2h_bin"])

    s2q_min   = float(opt_dict["s2q_min"])
    s2q_max   = float(opt_dict["s2q_max"])
    s2q_bin   = int(opt_dict["s2q_bin"])

    nsipm_all_min  = int(opt_dict["nsipm_all_min"])
    nsipm_all_max  = int(opt_dict["nsipm_all_max"])
    nsipm_all_bin  = int(opt_dict["nsipm_all_bin"])

    nsipm_min  = int(opt_dict["nsipm_min"])
    nsipm_max  = int(opt_dict["nsipm_max"])
    nsipm_bin  = int(opt_dict["nsipm_bin"])

    r_range   = (0,rmax)
    dt_range = (dt_min, dt_max)
    xy_range  = (-rmax,  rmax)

    s1e_range = (s1e_min, s1e_max)
    s2e_range = (s2e_min, s2e_max)
    s2w_range = (s2w_min, s2w_max)
    s2h_range = (s2h_min, s2h_max)
    s2q_range       = (s2q_min,   s2q_max)
    nsipm_range     = (nsipm_min, nsipm_max)
    nsipm_all_range = (nsipm_all_min, nsipm_all_max)

    s1w_min   = float(opt_dict["s1w_min"])
    s1w_max   = float(opt_dict["s1w_max"])
    s1w_bin   = int(opt_dict["s1w_bin"])

    s1w_range = (s1w_min, s1w_max)

    fig = plt.figure(figsize=(15,25))
    ax      = fig.add_subplot(5, 2, 1)
    nevt, *_  = plt.hist2d(dst.S2t/units.mus, dst.S2e,(50, 50), [(400,800), s2e_range], cmap='coolwarm')
    plt.xlabel('S2t ($\mu$s)')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 2)
    nevt, *_  = plt.hist2d(dst.S2t/units.mus, dst.S2e,(50, 50), [(400,800), s2e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S1t ($\mu$s)')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 3)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2e,(50, 50), [(0,400), s2e_range], cmap='coolwarm')
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 4)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2e,(50, 50), [(0,400), s2e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 5)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2h,(50, 50), [(0,400), s2h_range], cmap='coolwarm')
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S2h (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 6)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2h,(50, 50), [(0,400), s2h_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S2h (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 7)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2w,(50, s2w_bin), [(0,400), s2w_range], cmap='coolwarm')
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S2w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 8)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2w,(50, s2w_bin), [(0,400), s2w_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('S2w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 9)
    nevt, *_  = plt.hist2d(dst.R, dst.S2e,(50, 50), [r_range, s2e_range], cmap='coolwarm')
    plt.xlabel('R (mm)')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig.add_subplot(5, 2, 10)
    nevt, *_  = plt.hist2d(dst.R, dst.S2e,(50, 50), [r_range, s2e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('R')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

### ------- New figure
    fig_2 = plt.figure(figsize=(15,25))

    ax      = fig_2.add_subplot(5, 2, 1)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S2w,(50, 50), [s2e_range, s2w_range], cmap='coolwarm')
    plt.xlabel('S2e (pes)')
    plt.ylabel('S2w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 2)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S2w,(50, 50), [s2e_range, s2w_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (pes)')
    plt.ylabel('S2w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 3)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S1w/units.mus,(50, s1w_bin), [s2e_range, s1w_range], cmap='coolwarm')
    plt.xlabel('S2e (pes)')
    plt.ylabel('S1w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 4)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S1w/units.mus,(50, s1w_bin), [s2e_range, s1w_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (pes)')
    plt.ylabel('S1w ($\mu$s)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 5)
    nevt, *_  = plt.hist2d(dst.Phi, dst.S2e,(50, 50), [(-1,1), s2e_range], cmap='coolwarm')
    plt.xlabel('Phi')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 6)
    nevt, *_  = plt.hist2d(dst.Phi, dst.S2e,(50, 50), [(-1,1), s2e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Phi ')
    plt.ylabel('S2e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 7)
    nevt, *_  = plt.hist2d(dst.X, dst.Y,(50, 50), [xy_range, xy_range], normed=True, weights=dst.S2e.values, cmap='coolwarm')
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.title('XY event distribution')
    plt.colorbar().set_label("Normed True, weighted by S2e")

    ax      = fig_2.add_subplot(5, 2, 8)
    nevt, *_  = plt.hist2d(dst.S2e, dst.X,(50, 50), [s2e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (mm)')
    plt.ylabel('X (mm)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 9)
    nevt, *_  = plt.hist2d(dst.S2e, dst.Y,(50, 50), [s2e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (mm)')
    plt.ylabel('Y (mm)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_2.add_subplot(5, 2, 10)
    nevt, *_  = plt.hist2d(dst.S2e, dst.R,(50, 50), [s2e_range, r_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (mm)')
    plt.ylabel('R (mm)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ### 3 figure

    fig_3 = plt.figure(figsize=(15,35))

    ax      = fig_3.add_subplot(6, 2, 1)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S1e,(s2e_bin, s2e_bin), [s2e_range, s1e_range], cmap='coolwarm')
    plt.xlabel('S2e (pes)')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 2)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S1e,(s2e_bin, s2e_bin), [s2e_range, s1e_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (pes)')
    plt.ylabel('S1e (pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 3)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2q,(dt_bin, s2q_bin), [dt_range, s2q_range], cmap='coolwarm')
    plt.xlabel('DT ($\mu$s)')
    plt.ylabel('S2q(pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 4)
    nevt, *_  = plt.hist2d(dst.DT, dst.S2q,(dt_bin, s2q_bin), [dt_range, s2q_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('DT ($\mu$s)')
    plt.ylabel('S2q(pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 5)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S2q,(s2e_bin, s2q_bin), [s2e_range, s2q_range], cmap='coolwarm')
    plt.xlabel('S2e (pes)')
    plt.ylabel('S2q(pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 6)
    nevt, *_  = plt.hist2d(dst.S2e, dst.S2q,(s2e_bin, s2q_bin), [s2e_range, s2q_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (pes)')
    plt.ylabel('S2q(pes)')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 7)
    nevt, *_  = plt.hist2d(dst.S2e, dst.Nsipm,(s2e_bin, nsipm_bin), [s2e_range, nsipm_range], cmap='coolwarm')
    plt.xlabel('S2e (pes)')
    plt.ylabel('N sipm')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 8)
    nevt, *_  = plt.hist2d(dst.S2e, dst.Nsipm,(s2e_bin, nsipm_bin), [s2e_range, nsipm_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2e (pes)')
    plt.ylabel('N sipm')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 9)
    nevt, *_  = plt.hist2d(dst.S2q, dst.Nsipm,(s2q_bin, nsipm_bin), [s2q_range, nsipm_range], cmap='coolwarm')
    plt.xlabel('S2q (pes)')
    plt.ylabel('N sipm')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 10)
    nevt, *_  = plt.hist2d(dst.S2q, dst.Nsipm,(s2q_bin, nsipm_bin), [s2q_range, nsipm_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('S2q (pes)')
    plt.ylabel('N sipm')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 11)
    nevt, *_  = plt.hist2d(dst.DT, dst.Nsipm,(dt_bin, nsipm_bin), [dt_range, nsipm_range], cmap='coolwarm')
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('N sipm')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    ax      = fig_3.add_subplot(6, 2, 12)
    nevt, *_  = plt.hist2d(dst.DT, dst.Nsipm,(dt_bin, nsipm_bin), [dt_range, nsipm_range], cmap='coolwarm', norm=colors.LogNorm())
    plt.xlabel('Drift time ($\mu$s)')
    plt.ylabel('N sipm')
    plt.title(None)
    plt.colorbar().set_label("Number of events")

    colors.LogNorm()


    print('s2 2d plots saved in '+ plots_dir)

    return fig, fig_2, fig_3
