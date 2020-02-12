# Utilities
import time
import shutil
import datetime
import random
import glob
import warnings

# Scientific modules
import numpy as np
import pandas as pd
import tables            as tb

# Plotting
import seaborn as sns
import matplotlib.colors as colors

# Fitting
from iminuit     import Minuit, describe
from probfit     import Extended, BinnedChi2
from probfit     import gaussian, linear, poly2, Chi2Regression

# krdiff
from krdiff.core.selection_histos       import plot_s1_and_s2, \
                                        plot_s1_variables, plot_s2_variables, \
                                        plot_Z_DT_variables, \
                                        plot_e_before_after_sel
from krdiff.core.histo_functions        import h1_alpha,\
                                        plot_residuals_E_reso_gauss,\
                                        plot_residuals_E_reso_double_gaussian,\
                                        plot_residuals_E_reso_gaussian_const
from krdiff.core.kr_types_old_icaros    import PlotLabels, FitType

# IC
#from   invisible_cities.io.dst_io              import load_dsts
from   invisible_cities.core .core_functions   import in_range
from   invisible_cities.core.system_of_units_c import units
from   invisible_cities.icaro.hst_functions    import hist2d_profile


# ICAROS
from krcal.core.core_functions                import time_delta_from_time
from krcal.core.core_functions                import phirad_to_deg
from krcal.core.core_functions                import NN
from krcal.core.core_functions                import timeit
