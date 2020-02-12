
# coding: utf-8

# In[1]:


## Calcular reso para low drift high drift and different R values


# # Selection Run 6721

# ## This Notebook:
#
# - Data: Run 6721
# - Selects:
#     - 1 S1 and 1 S2
#     - filters:
#         - R<40

# In[2]:


run = 6721
dir = 'data'


# In[3]:


print('Do you want to overwrite the directory for control plots? ')
answer = input()
if answer == 'yes':
    overwrite = True
else:
    overwrite = False
print(overwrite)


# ### Create directory for control plots

# In[4]:


import shutil

import time
import os
import sys

plots_path = '/Users/neus/current-work/selection_plots'
plots_dir  = plots_path+'/'+str(run)+'/'

if os.path.exists(plots_dir) and overwrite:
    shutil.rmtree(plots_dir)

try:
    os.makedirs(plots_dir)
except OSError:
    print (f'Creation of the directory {plots_dir} failed')
else:
    print (f'Successfully created the directory {plots_dir}')


# #### Run number and ranges for control plots

# In[5]:


RMAX      = 80
RFID      = 70
RCORE     = 50

s1e_range_raw = (0, 100)
s1e_range = (0,50)

s2e_range_raw     = (500, 8000)
s2e_range         = (3000, 6000)

s2q_range = (0, 350)
r_range   = (0,80)

dt_range  = (0, 350)

s1e_range_raw = (0, 100)
s1h_range = (0,10)
s1w_range=(0,0.8)
s1w_bin = 33

s2w_range = (0.,20)
s2w_bin = 41
s2h_range = (0.,3000)
s2h_bin = 50

s2q_range_raw = (0,1000)
Nsipm_range_raw = (0,256)
Nsipm_range = (0,25)

xy_range  = (-RMAX,  RMAX)


# In[6]:


fit_erange = (4500,5300)


# ## Selection

# In[7]:


# study cuts
s1e_range_sel = (1, 30)
s2e_range_sel = s2e_range  # ---> cut posat al principi del notebook
s2w_range_sel = (3, 15)
s2q_range_sel = (100, 250)
Nsipm_min_sel = 3


# ## Imports

# In[8]:



import datetime
import numpy as np
import pandas as pd
import tables            as tb
import random
import glob
import warnings
import seaborn as sns
import matplotlib.colors as colors
sns.set()
sns.set_style("white")
sns.set_style("ticks")

print("Last updated on ", time.asctime())


# ### Input/output

# In[9]:


path        = '/Users/neus/current-work/'+dir+'/'+str(run)+'/kdst/'
output_path = '/Users/neus/current-work/'+dir+'/'+str(run)+'/kdst-reduced/'
output_dst_filename = "".join([output_path, 'reduced_kdst.h5'])


# In[10]:


print(output_dst_filename)


# In[11]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = 10, 8
plt.rcParams["font.size"     ] = 14


# In[12]:


from iminuit     import Minuit, describe
from probfit     import Extended, BinnedChi2
from probfit     import gaussian, linear, poly2, Chi2Regression


# In[13]:


from numpy import pi, sqrt

from  invisible_cities.io.dst_io              import load_dsts
from  invisible_cities.core .core_functions   import in_range
from  invisible_cities.core.system_of_units_c import units


# In[14]:


from   invisible_cities.icaro.hst_functions       import hist2d_profile


# In[15]:


from krdiff.core.selection_histos       import plot_s1_and_s2, plot_s1_variables, plot_s2_variables, plot_Z_DT_variables, plot_e_before_after_sel
from krdiff.core.histo_functions        import h1_alpha, plot_residuals_E_reso_gauss, plot_residuals_E_reso_double_gaussian, plot_residuals_E_reso_gaussian_const


# In[16]:


import krcal.dev.corrections                  as corrections
import krcal.utils.hst_extend_functions       as hst
from   krcal.core import fit_functions_ic     as fitf
import invisible_cities.reco.corrections      as corrf


# In[17]:


from krcal.core.core_functions                import time_delta_from_time
from krcal.core.core_functions                import phirad_to_deg
from krcal.core.core_functions                import NN
from krcal.core.core_functions                import timeit
from krcal.core.core_functions                import data_frames_are_identical

from krcal.core.io_functions                  import filenames_from_paths
from krcal.core.io_functions                  import filenames_from_list
from krcal.core.io_functions                  import kdst_write
from krcal.core.io_functions                  import write_maps
from krcal.core.io_functions                  import read_maps
from krcal.core.io_functions                  import write_maps_ts
from krcal.core.io_functions                  import read_maps_ts

from krcal.core.ranges_and_bins_functions     import kr_ranges_and_bins

from krcal.core.histo_functions               import h1, h1d, h2, h2d, profile1d, plot_histo
from krcal.core.kr_types                      import PlotLabels, FitType


# ### Load kdst

# In[18]:


files_all = [path + f for f in os.listdir(path) if os.path.isfile( os.path.join(path, f) )]
dst_full         = load_dsts(files_all, "DST", "Events")


# In[19]:


print(files_all[0])


# In[72]:


len(files_all)


# #### There are duplicated events because of the multiplicity both in s1 and s2

# In[21]:


unique_events = ~dst_full.event.duplicated()

number_of_S2s_full  = np.size         (unique_events)
number_of_evts_full = np.count_nonzero(unique_events)

print(f"Total number of S2s   : {number_of_S2s_full} ")
print(f"Total number of events: {number_of_evts_full}")


# In[22]:


n = plot_s1_and_s2(dst_full)


# In[23]:


fnS1 = n[1]/np.sum(n)
print(f'fraction of S1s = {fnS1}')

print(f'1 S1s candidates = {n[1]}')
print(f'2 S1s candidates = {n[2]}')


# In[24]:


dst_full[20:32]


# In[25]:


test = dst_full.groupby('event').first().reset_index()

num_s1_1 = test[test.nS1 == 1]
num_s1_2 = test[test.nS1 == 2]

print(len(num_s1_1))
print(len(num_s1_2))
test[test.event == 3548876]


# In[26]:


dst_full.columns


# ### Select events with 1 S1 and 1 S2 and Fiducial cut <40

# In[104]:


RALL = 70
RFID = 40


# In[74]:


number_of_evts_full


# In[119]:


dst1s1    = dst_full[in_range(dst_full.nS1, 1,2)]
dst1s2    = dst1s1  [in_range(dst1s1.nS2,   1,2)]
dstRALL   = dst1s2  [in_range(dst1s2.R,     0, RALL)]
dst       = dst1s2  [in_range(dst1s2.R,     0, RFID)]

ev_sig_region = len(dst[in_range(dst.S2e, 4500, 5500)])

print('--------------------- Efficiencies: ')
print(f"Events 1s11s2                    : {len(dst1s2)}  ({len(dst1s2)/number_of_evts_full:.3f} %) ")
print(f"Events 1s11s2 & R<{RALL}             : {len(dstRALL)}   ({len(dstRALL)/number_of_evts_full:.3f} %)")
print(f"Events 1s11s2 & R<{RFID}             : {len(dst)}   ({len(dst)/number_of_evts_full:.3f} %)")
print(f"Events 1s11s2 & R<{RFID} & E sig     : {ev_sig_region}   ({ev_sig_region/number_of_evts_full:.3f} %)")


# #### Control plot energy

# In[120]:


fig = plt.figure(figsize=(13,35))

ax      = fig.add_subplot(7, 2, 1)
(_) = h1(dst.S2e, bins = 100, range = (300,90000), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')

ax      = fig.add_subplot(7, 2, 2)
(_) = h1(dst.S2e, bins = 100, range = (300,90000), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 3)
(_) = h1(dst.S2e, bins = 100, range = s2e_range_raw, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')

ax      = fig.add_subplot(7, 2, 4)
(_) = h1(dst.S2e, bins = 100, range = s2e_range_raw, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 5)
(_) = h1(dst.S2e, bins = 100, range = s2e_range, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')

ax      = fig.add_subplot(7, 2, 6)
(_) = h1(dst.S2e, bins = 100, range = s2e_range, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 7)
(_) = h1(dst.S2e, bins = 100, range = [4400, 5400], histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')

ax      = fig.add_subplot(7, 2, 8)
(_) = h1(dst.S2e, bins = 100, range = [4400, 5400], histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper left')
ax.set_yscale('log')


# #### RAW S1 control plots

# ##### Note :S1t in nanosecons

# In[76]:


fig = plt.figure(figsize=(15,25))

ax      = fig.add_subplot(5, 2, 1)
(_) = h1(dst.S1e, bins = 100, range = s1e_range_raw, histtype='stepfilled', color='steelblue',
             lbl='')
plot_histo(PlotLabels('S1e (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(5, 2, 2)
(_) = h1(dst.S1e, bins = 100, range = s1e_range_raw, histtype='stepfilled', color='lightblue',
             lbl='')
plot_histo(PlotLabels('S1e (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(5, 2, 3)
(_) = h1(dst.S1w/units.mus, bins = s1w_bin, range = s1w_range, histtype='stepfilled', color='steelblue',
             lbl='')
plot_histo(PlotLabels('Width (mus)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(5, 2, 4)
(_) = h1(dst.S1w/units.mus, bins = s1w_bin, range = s1w_range, histtype='stepfilled', color='lightblue',
             lbl='')
plot_histo(PlotLabels('Width (mus)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(5, 2, 5)
(_) = h1(dst.S1h, bins = 100, range = s1h_range, histtype='stepfilled', color='steelblue',
             lbl='')
plot_histo(PlotLabels('S1 height (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(5, 2, 6)
(_) = h1(dst.S1h, bins = 100, range = s1h_range, histtype='stepfilled', color='lightblue',
             lbl='')
plot_histo(PlotLabels('S1 height (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(5, 2, 7)
(_) = h1(dst.S1h/dst.S1e, bins = 100, range = (0,0.6), histtype='stepfilled', color='steelblue',
             lbl='')
plot_histo(PlotLabels('S1height/s1e (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(5, 2, 8)
(_) = h1(dst.S1h/dst.S1e, bins = 100, range = (0,0.6), histtype='stepfilled', color='lightblue',
             lbl='')
plot_histo(PlotLabels('S1height/s1e (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(5, 2, 9)
(_) = h1(dst.S1t/units.mus, bins = 20, range = (0,400), histtype='stepfilled', color='steelblue',
             lbl='')
plot_histo(PlotLabels('S1 time mus','Entries',''), ax)
plt.legend(loc='upper left')

ax      = fig.add_subplot(5, 2, 10)
(_) = h1(dst.S1t/units.mus, bins = 20, range = (0,400), histtype='stepfilled', color='lightblue',
             lbl='')
plot_histo(PlotLabels('S1 time mus','Entries',''), ax)
plt.legend(loc='upper left')
ax.set_yscale('log')

plt.savefig(plots_dir + '/S1_all_'+str(run)+'.png')


# In[30]:


fig = plt.figure(figsize=(15,35))

ax      = fig.add_subplot(7, 2, 1)
nevt, *_  = plt.hist2d(dst.S1t/units.mus, dst.S1e,(50, 50), [dt_range, s1e_range], cmap='coolwarm')
plt.xlabel('S1t ($\mu$s)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 2)
nevt, *_  = plt.hist2d(dst.S1t/units.mus, dst.S1e,(50, 50), [dt_range, s1e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S1t ($\mu$s)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 3)
nevt, *_  = plt.hist2d(dst.DT, dst.S1e,(50, 50), [(0,400), s1e_range], cmap='coolwarm')
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 4)
nevt, *_  = plt.hist2d(dst.DT, dst.S1e,(50, 50), [(0,400), s1e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 5)
nevt, *_  = plt.hist2d(dst.DT, dst.S1h,(50, 50), [(0,400), s1h_range], cmap='coolwarm')
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S1h (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 6)
nevt, *_  = plt.hist2d(dst.DT, dst.S1h,(50, 50), [(0,400), s1h_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S1h (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 7)
nevt, *_  = plt.hist2d(dst.DT, dst.S1w/units.mus,(50, s1w_bin), [(0,400), s1w_range], cmap='coolwarm')
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S1w ($\mu$s)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 8)
nevt, *_  = plt.hist2d(dst.DT, dst.S1w/units.mus,(50, s1w_bin), [(0,400), s1w_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S1w ($\mu$s)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 9)
nevt, *_  = plt.hist2d(dst.R, dst.S1e,(50, 50), [r_range, s1e_range], cmap='coolwarm')
plt.xlabel('R (mm)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 10)
nevt, *_  = plt.hist2d(dst.R, dst.S1e,(50, 50), [r_range, s1e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('R')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 11)
nevt, *_  = plt.hist2d(dst.Phi, dst.S1e,(50, 50), [(-1,1), s1e_range], cmap='coolwarm')
plt.xlabel('Phi')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 12)
nevt, *_  = plt.hist2d(dst.Phi, dst.S1e,(50, 50), [(-1,1), s1e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Phi ')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 13)
nevt, *_  = plt.hist2d(dst.X, dst.Y,(50, 50), [xy_range, xy_range],cmap='coolwarm')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.title(None)
plt.colorbar().set_label("Number of events")

#ax      = fig.add_subplot(7, 2, 12)
#nevt, *_  = plt.hist2d(dst.X, dst.Y,(50, 50), [xy_range, xy_range], normed=True, weights=dst.S1e.values, cmap='coolwarm')
#plt.xlabel('X (mm)')
#plt.ylabel('Y (mm)')
#plt.title(None)
#plt.colorbar().set_label("S1e (pes)")

plt.savefig(plots_dir + '/S1_2D_all_'+str(run)+'.png')


# In[31]:


fig = plt.figure(figsize=(13,35))

ax      = fig.add_subplot(7, 2, 1)
(_) = h1(dst.S2e, bins = 100, range = s2e_range_raw, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 2)
(_) = h1(dst.S2e, bins = 100, range = s2e_range_raw, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 3)
(_) = h1(dst.S2h, bins =s2h_bin , range = s2h_range, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2h (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 4)
(_) = h1(dst.S2h, bins = s2h_bin, range = s2h_range, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2h (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 5)
(_) = h1(dst.S2w, bins =s2w_bin , range = s2w_range, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2w ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 6)
(_) = h1(dst.S2w, bins = s2w_bin, range = s2w_range, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2w ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 7)
(_) = h1(dst.S2h/dst.S2e, bins = 100, range = (0,0.6), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2height/s2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 8)
(_) = h1(dst.S2h/dst.S2e, bins = 100, range = (0,0.6), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2height/s2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 9)
(_) = h1(dst.S2t/units.mus, bins = 20, range = (400,800), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2 time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 10)
(_) = h1(dst.S2t/units.mus, bins = 20, range = (400,800), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2 time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 11)
(_) = h1(dst.DT, bins = 100, range = (0,400), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('Drit time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 12)
(_) = h1(dst.DT, bins = 100, range = (0,400), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('Drift time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')


ax      = fig.add_subplot(7, 2, 13)
(_) = h1(dst.Z, bins = 100, range = (0,400), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('Z (mm)','Entries',''), ax)
plt.legend(loc='upper left')

ax      = fig.add_subplot(7, 2, 14)
(_) = h1(dst.Z, bins = 100, range = (0,400), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('Z (mm)','Entries',''), ax)
plt.legend(loc='upper left')
ax.set_yscale('log')

plt.savefig(plots_dir + '/S2_all_'+str(run)+'.png')


# #### Cut in ths_sum_s2si = 5 pes

# In[116]:


fig = plt.figure(figsize=(13,35))
ax      = fig.add_subplot(7, 2, 2)
(_) = h1(dst.S2q, bins = 10, range = (0,10), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2 Charge (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

plt.savefig(plots_dir + '/S2_Charge_'+str(run)+'.png')


# In[33]:


fig = plt.figure(figsize=(13,35))

ax      = fig.add_subplot(7, 2, 1)
(_) = h1(dst.S2q, bins = 100, range = s2q_range_raw, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2 Charge (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 2)
(_) = h1(dst.S2q, bins = 100, range = s2q_range_raw, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2 Charge (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 3)
(_) = h1(dst.Nsipm, bins = 50, range = Nsipm_range, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('Num Sipm','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 4)
(_) = h1(dst.Nsipm, bins = 256, range = Nsipm_range_raw, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('Num Sipm ','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')


# In[113]:


Nsipm_range


# In[34]:


fig = plt.figure(figsize=(15,35))

ax      = fig.add_subplot(7, 2, 1)
nevt, *_  = plt.hist2d(dst.S2t/units.mus, dst.S2e,(50, 50), [(400,800), s2e_range], cmap='coolwarm')
plt.xlabel('S2t ($\mu$s)')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 2)
nevt, *_  = plt.hist2d(dst.S2t/units.mus, dst.S2e,(50, 50), [(400,800), s2e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S1t ($\mu$s)')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 3)
nevt, *_  = plt.hist2d(dst.DT, dst.S2e,(50, 50), [(0,400), s2e_range], cmap='coolwarm')
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 4)
nevt, *_  = plt.hist2d(dst.DT, dst.S2e,(50, 50), [(0,400), s2e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 5)
nevt, *_  = plt.hist2d(dst.DT, dst.S2h,(50, 50), [(0,400), s2h_range], cmap='coolwarm')
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S2h (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 6)
nevt, *_  = plt.hist2d(dst.DT, dst.S2h,(50, 50), [(0,400), s2h_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S2h (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 7)
nevt, *_  = plt.hist2d(dst.DT, dst.S2w,(50, s2w_bin), [(0,400), s2w_range], cmap='coolwarm')
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S2w ($\mu$s)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 8)
nevt, *_  = plt.hist2d(dst.DT, dst.S2w,(50, s2w_bin), [(0,400), s2w_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S2w ($\mu$s)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 9)
nevt, *_  = plt.hist2d(dst.R, dst.S2e,(50, 50), [r_range, s2e_range], cmap='coolwarm')
plt.xlabel('R (mm)')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 10)
nevt, *_  = plt.hist2d(dst.R, dst.S2e,(50, 50), [r_range, s2e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('R')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 11)
nevt, *_  = plt.hist2d(dst.Phi, dst.S2e,(50, 50), [(-1,1), s2e_range], cmap='coolwarm')
plt.xlabel('Phi')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 12)
nevt, *_  = plt.hist2d(dst.Phi, dst.S2e,(50, 50), [(-1,1), s2e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Phi ')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")


# In[35]:


s2e_range


# In[36]:


fig = plt.figure(figsize=(20,10))
ax      = fig.add_subplot(2, 3, 1)
nevt, *_  = plt.hist2d(dst.X, dst.Y,(50, 50), [xy_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.title('XY event distribution')
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(2, 3, 2)
nevt, *_  = plt.hist2d(dst.S1e, dst.X,(50, 50), [s1e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S1e (mm)')
plt.ylabel('X (mm)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(2, 3, 3)
nevt, *_  = plt.hist2d(dst.S1e, dst.Y,(50, 50), [s1e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S1e (mm)')
plt.ylabel('Y (mm)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(2, 3, 4)
nevt, *_  = plt.hist2d(dst.S2e, dst.X,(50, 50), [s2e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (mm)')
plt.ylabel('X (mm)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(2, 3, 5)
nevt, *_  = plt.hist2d(dst.S2e, dst.Y,(50, 50), [s2e_range, xy_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (mm)')
plt.ylabel('Y (mm)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(2, 3, 6)
nevt, *_  = plt.hist2d(dst.S2e, dst.R,(50, 50), [s2e_range, r_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (mm)')
plt.ylabel('R (mm)')
plt.title(None)
plt.colorbar().set_label("Number of events")

colors.LogNorm()

plt.savefig(plots_dir + '/S2_XY_'+str(run)+'.png')


# ### XY event distribution

# ### Energy/Q distributions

# In[37]:


fig = plt.figure(figsize=(15,35))

ax      = fig.add_subplot(7, 2, 1)
nevt, *_  = plt.hist2d(dst.S2e, dst.S1e,(50, 50), [s2e_range, s1e_range], cmap='coolwarm')
plt.xlabel('S2e (pes)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 2)
nevt, *_  = plt.hist2d(dst.S2e, dst.S1e,(50, 50), [s2e_range, s1e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (pes)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")


ax      = fig.add_subplot(7, 2, 3)
nevt, *_  = plt.hist2d(dst.DT, dst.S2q,(50, 50), [dt_range, s2q_range], cmap='coolwarm')
plt.xlabel('DT ($\mu$s)')
plt.ylabel('S2q(pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 4)
nevt, *_  = plt.hist2d(dst.DT, dst.S2q,(50, 50), [dt_range, s2q_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('DT ($\mu$s)')
plt.ylabel('S2q(pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 5)
nevt, *_  = plt.hist2d(dst.S2e, dst.S2q,(50, 50), [s2e_range, s2q_range], cmap='coolwarm')
plt.xlabel('S2e (pes)')
plt.ylabel('S2q(pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 6)
nevt, *_  = plt.hist2d(dst.S2e, dst.S2q,(50, 50), [s2e_range, s2q_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (pes)')
plt.ylabel('S2q(pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 7)
nevt, *_  = plt.hist2d(dst.S2e, dst.Nsipm,(50, 26), [s2e_range, Nsipm_range], cmap='coolwarm')
plt.xlabel('S2e (pes)')
plt.ylabel('N sipm')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 8)
nevt, *_  = plt.hist2d(dst.S2e, dst.Nsipm,(50, 26), [s2e_range, Nsipm_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (pes)')
plt.ylabel('N sipm')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 9)
nevt, *_  = plt.hist2d(dst.S2q, dst.Nsipm,(50, 26), [s2q_range, Nsipm_range], cmap='coolwarm')
plt.xlabel('S2q (pes)')
plt.ylabel('N sipm')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 10)
nevt, *_  = plt.hist2d(dst.S2q, dst.Nsipm,(50, 26), [s2q_range, Nsipm_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2q (pes)')
plt.ylabel('N sipm')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 11)
nevt, *_  = plt.hist2d(dst.DT, dst.Nsipm,(50, 26), [(0, 320), Nsipm_range], cmap='coolwarm')
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('N sipm')
plt.title(None)
plt.colorbar().set_label("Number of events")

ax      = fig.add_subplot(7, 2, 12)
nevt, *_  = plt.hist2d(dst.DT, dst.Nsipm,(50, 26), [(0, 320), Nsipm_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('N sipm')
plt.title(None)
plt.colorbar().set_label("Number of events")

plt.savefig(plots_dir + '/S2_Charge_XY_'+str(run)+'.png')


# #### Plots for talks

# In[38]:


fig = plt.figure(figsize=(15,35))

ax      = fig.add_subplot(7, 2, 1)
nevt, *_  = plt.hist2d(dst.S2e, dst.S1e,(50, 60), [(3000, 6000), (0,60)], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (pes)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

plt.savefig(plots_dir + '/S2_Charge_XY_'+str(run)+'.png')


# In[39]:


fig = plt.figure(figsize=(15,35))
ax      = fig.add_subplot(7, 2, 6)
nevt, *_  = plt.hist2d(dst.S2e, dst.S2q,(50, 50), [s2e_range, s2q_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (pes)')
plt.ylabel('S2q(pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")

plt.savefig(plots_dir + '/S2_Charge_XY_'+str(run)+'.png')


# In[40]:


fig = plt.figure(figsize=(15,35))
ax      = fig.add_subplot(7, 2, 8)
nevt, *_  = plt.hist2d(dst.S2e, dst.Nsipm,(50, 26), [s2e_range, Nsipm_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('S2e (pes)')
plt.ylabel('N sipm')
plt.title(None)
plt.colorbar().set_label("Number of events")


# In[117]:


fig = plt.figure(figsize=(15,35))
ax      = fig.add_subplot(7, 2, 4)
nevt, *_  = plt.hist2d(dst.DT, dst.S2e,(50, 50), [(0,350), s2e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")


# In[42]:


fig = plt.figure(figsize=(15,35))
ax      = fig.add_subplot(7, 2, 4)
nevt, *_  = plt.hist2d(dst.DT, dst.S1e,(50, 50), [(0,350), s1e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('Drift time ($\mu$s)')
plt.ylabel('S1e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")


# #### No cut in R

# In[43]:


fig = plt.figure(figsize=(15,35))
ax      = fig.add_subplot(7, 2, 10)
nevt, *_  = plt.hist2d(dst1s2.R, dst1s2.S2e,(50, 50), [r_range, s2e_range], cmap='coolwarm', norm=colors.LogNorm())
plt.xlabel('R (mm)')
plt.ylabel('S2e (pes)')
plt.title(None)
plt.colorbar().set_label("Number of events")


# #### Energy Resolution Fits

# In[44]:


def mypdf_gauss_const(x, mu, sigma, N, Ny):
    return N*np.exp(-0.5*np.power((x - mu)/(sigma),2)) + Ny


# In[45]:


def mypdf_gauss(x, mu, sigma, N):
    return N*np.exp(-0.5*np.power((x - mu)/(sigma),2))


# In[46]:


def mypdf_double_gauss(x, mux, sigmax, Nx, sigmay, Ny):
    return Nx*np.exp(-0.5*np.power((x - mux)/(sigmax),2)) + Ny*np.exp(-0.5*np.power((x)/(sigmay),2))



# In[47]:


fit_erange


# ### Fit 1 Gaussian

# In[48]:


plt.figure(figsize=(8,6))
bx2_Core40_my_gauss = BinnedChi2(mypdf_gauss, dst.S2e, bins = 50 , bound=fit_erange) #create cost function
bx2_Core40_my_gauss.show(args={'mu':4900, 'sigma':70, 'N':400})  #another way to draw it
plt.show()


# In[49]:


plt.figure(figsize=(8,6))
m_Core40_my_gauss = Minuit(bx2_Core40_my_gauss, mu=4900, sigma=70, N=400)
m_Core40_my_gauss.migrad()
bx2_Core40_my_gauss.show(m_Core40_my_gauss)
plt.show()


# In[50]:


mean_gauss_Core40     = m_Core40_my_gauss.values[0]
mean_gauss_Core40_u   = m_Core40_my_gauss.errors[0]

sigma_gauss_Core40    = m_Core40_my_gauss.values[1]
sigma_gauss_Core40_u  = m_Core40_my_gauss.errors[1]

N_gauss_Core40        = m_Core40_my_gauss.values[2]
N_gauss_Core40_u      = m_Core40_my_gauss.errors[2]

print(f'Mean:  {mean_gauss_Core40:.2f}         +/- {mean_gauss_Core40_u:.2f} ')
print(f'Sigma: {sigma_gauss_Core40:.2f}        +/- {sigma_gauss_Core40_u:.2f} ')
print(f'N:     {N_gauss_Core40:.1f}            +/- {N_gauss_Core40_u:.1f} ')


# In[51]:


plt.style.use('classic')
plot_residuals_E_reso_gauss(dst.S2e, 50, fit_erange, mean_gauss_Core40, mean_gauss_Core40_u, sigma_gauss_Core40, sigma_gauss_Core40_u, N_gauss_Core40, N_gauss_Core40_u, 'e-reso-gauss-core40-Run-'+str(run))


# ### Fit Gaussian + const

# In[52]:


plt.figure(figsize=(8,6))
bx2_Core70_my_gauss_const = BinnedChi2(mypdf_gauss_const,dst.S2e , bins = 50 , bound=fit_erange) #create cost function
bx2_Core70_my_gauss_const.show(args={'mu':4900, 'sigma':70, 'N':400, 'Ny':25})  #another way to draw it
plt.show()


# In[53]:


plt.figure(figsize=(8,6))
m_Core70_my_gauss_const = Minuit(bx2_Core70_my_gauss_const, mu=4900, sigma=70, N=400, Ny=25)
m_Core70_my_gauss_const.migrad()
bx2_Core70_my_gauss_const.show(m_Core70_my_gauss_const)
plt.show()


# In[54]:


mean_gauss_const_Core70     = m_Core70_my_gauss_const.values[0]
mean_gauss_const_Core70_u   = m_Core70_my_gauss_const.errors[0]

sigma_gauss_const_Core70    = m_Core70_my_gauss_const.values[1]
sigma_gauss_const_Core70_u  = m_Core70_my_gauss_const.errors[1]

N_gauss_const_Core70        = m_Core70_my_gauss_const.values[2]
N_gauss_const_Core70_u      = m_Core70_my_gauss_const.errors[2]

N2_gauss_const_Core70        = m_Core70_my_gauss_const.values[3]
N2_gauss_const_Core70_u      = m_Core70_my_gauss_const.errors[3]


print(f'Mean:  {mean_gauss_const_Core70:.2f}         +/- {mean_gauss_const_Core70_u:.2f} ')
print(f'Sigma: {sigma_gauss_const_Core70:.2f}        +/- {sigma_gauss_const_Core70_u:.2f} ')
print(f'N:     {N_gauss_const_Core70:.1f}            +/- {N_gauss_const_Core70_u:.1f} ')
print(f'N2:    {N2_gauss_const_Core70:.1f}           +/- {N2_gauss_const_Core70_u:.1f} ')


# In[55]:


plt.style.use('classic')
plot_residuals_E_reso_gaussian_const(dst.S2e, 50, fit_erange, mean_gauss_const_Core70, mean_gauss_const_Core70_u, sigma_gauss_const_Core70, sigma_gauss_const_Core70_u, N_gauss_const_Core70, N_gauss_const_Core70_u, N2_gauss_const_Core70, N2_gauss_const_Core70_u,
                                     'e-reso-gauss-const-core40-Run-'+str(run))


# ### Fit 2 Gaussians

# In[56]:


plt.figure(figsize=(8,6))
bx2_Core70_my_double_gauss = BinnedChi2(mypdf_double_gauss,dst.S2e , bins = 50 , bound=fit_erange) #create cost function
bx2_Core70_my_double_gauss.show(args={'mux':4900, 'sigmax':70, 'Nx':400, 'sigmay':300, 'Ny':0.1})  #another way to draw it
plt.show()


# In[57]:


plt.figure(figsize=(8,7))
m_Core70_my_double_gauss = Minuit(bx2_Core70_my_double_gauss, mux=4900, sigmax=77, Nx=400, sigmay=100, Ny=3)
m_Core70_my_double_gauss.migrad()
bx2_Core70_my_double_gauss.show(m_Core70_my_double_gauss)
plt.show()


# In[58]:


mean_double_Core70     = m_Core70_my_double_gauss.values[0]
mean_double_Core70_u   = m_Core70_my_double_gauss.errors[0]

sigma_double_Core70    = m_Core70_my_double_gauss.values[1]
sigma_double_Core70_u  = m_Core70_my_double_gauss.errors[1]

N_double_Core70        = m_Core70_my_double_gauss.values[2]
N_double_Core70_u      = m_Core70_my_double_gauss.errors[2]

sigma2_double_Core70    = m_Core70_my_double_gauss.values[3]
sigma2_double_Core70_u  = m_Core70_my_double_gauss.errors[3]

N2_double_Core70        = m_Core70_my_double_gauss.values[4]
N2_double_Core70_u      = m_Core70_my_double_gauss.errors[4]


print(f'Mean:  {mean_double_Core70:.2f}         +/- {mean_double_Core70_u:.2f} ')
print(f'Sigma: {sigma_double_Core70:.2f}        +/- {sigma_double_Core70_u:.2f} ')
print(f'N:     {N_double_Core70:.0f}            +/- {N_double_Core70_u:.0f} ')

print(f'Sigma2: {sigma2_double_Core70:.2f}        +/- {sigma2_double_Core70_u:.2f} ')
print(f'N2:     {N2_double_Core70:.0f}            +/- {N2_double_Core70_u:.0f} ')


# In[59]:


plt.style.use('classic')
plot_residuals_E_reso_double_gaussian(dst.S2e, 50, fit_erange, mean_double_Core70, mean_double_Core70_u, sigma_double_Core70, sigma_double_Core70_u, N_double_Core70, N_double_Core70_u, sigma2_double_Core70,sigma2_double_Core70_u, N2_double_Core70,N2_double_Core70_u,'e-reso-double-gauss-core40-Run-'+str(run))


# ### Drift velocity

# In[60]:


Z = dst[in_range(dst.Z, 305,350)].Z
fit_z_range = (305,350)


# In[61]:


fig = plt.figure(figsize=(12,4))
ax      = fig.add_subplot(1, 2, 1)
(_) = h1(dst.DT, bins = 100, range = (0,400), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('Drit time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(1, 2, 2)
(_) = h1(Z, bins = 100, range = fit_z_range, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('Drit time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')


# In[62]:


sigmoid  = lambda x, A, B, C, D: A / (1 + np.exp((x - B) / C)) + D


# In[63]:


mypdf = Extended(sigmoid)
describe(mypdf)
bx2 = BinnedChi2(mypdf, Z, bins = 100 , bound= fit_z_range )#create cost function
bx2.show(args={'A':1400, 'B':330, 'C':1.1, 'D':43 , 'N':1}) #another way to draw it
plt.show()


# In[64]:


m = Minuit(bx2, A=800, B=330, C=1.3 , D=100 , N=1)
m.migrad()
my_parmloc = (0.60,0.90)
bx2.draw(m, parmloc=my_parmloc)
plt.savefig('/Users/neus/current-work/diffusion/plots-drift-lifetime/drift-velocity-'+str(run)+'.png')
plt.show()


# #### Drift region size: 310 mm

# In[65]:


v = 310/m.args[1]
print(v)


# In[66]:


v_err = (310-2)/(m.args[1]-m.errors[1])
v_u = v - v_err


# In[67]:


print(f"Drift velocity = {v:.4f} +/- {v_u:.4f} ")


# In[68]:


print("Last updated on ", time.asctime())


# ### Control plots Cut in E and Fiducial

# In[69]:


fit_erange


# In[70]:


dstE       = dst[in_range(dst.S2e,4500,5300)]


# In[71]:


fig = plt.figure(figsize=(13,35))

ax      = fig.add_subplot(7, 2, 1)
(_) = h1(dstE.S2e, bins = 100, range = s2e_range_raw, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 2)
(_) = h1(dstE.S2e, bins = 100, range = s2e_range_raw, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 3)
(_) = h1(dstE.S2h, bins =s2h_bin , range = s2h_range, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2h (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 4)
(_) = h1(dstE.S2h, bins = s2h_bin, range = s2h_range, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2h (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 5)
(_) = h1(dstE.S2w, bins =s2w_bin , range = s2w_range, histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2w ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 6)
(_) = h1(dstE.S2w, bins = s2w_bin, range = s2w_range, histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2w ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 7)
(_) = h1(dstE.S2h/dstE.S2e, bins = 100, range = (0,0.6), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2height/s2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 8)
(_) = h1(dstE.S2h/dstE.S2e, bins = 100, range = (0,0.6), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2height/s2e (pes)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 9)
(_) = h1(dstE.S2t/units.mus, bins = 20, range = (400,800), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('S2 time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 10)
(_) = h1(dstE.S2t/units.mus, bins = 20, range = (400,800), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('S2 time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')

ax      = fig.add_subplot(7, 2, 11)
(_) = h1(dstE.DT, bins = 100, range = (0,400), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('Drit time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 12)
(_) = h1(dstE.DT, bins = 100, range = (0,400), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('Drift time ($\mu$s)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')


ax      = fig.add_subplot(7, 2, 13)
(_) = h1(dstE.Z, bins = 100, range = (0,400), histtype='stepfilled', color='crimson',
             lbl='')
plot_histo(PlotLabels('Z (mm)','Entries',''), ax)
plt.legend(loc='upper right')

ax      = fig.add_subplot(7, 2, 14)
(_) = h1(dstE.Z, bins = 100, range = (0,400), histtype='stepfilled', color='lightcoral',
             lbl='')
plot_histo(PlotLabels('Z (mm)','Entries',''), ax)
plt.legend(loc='upper right')
ax.set_yscale('log')
