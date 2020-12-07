import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from invisible_cities.core.core_functions  import shift_to_bin_centers
from ana_stat import error_on_a_fraction

def line(x, m, c):
    return m * x + c

def gaussC(x, mu, sigma, N, Ny):
    return N * np.exp(-0.5 * np.power((x - mu)/(sigma), 2)) + Ny

def gauss(x, mu, sigma, N):
    return N * np.exp(-0.5 * np.power((x - mu)/(sigma), 2))

def gauss_reso(x, mu, reso, N):
    return N * np.exp(-0.5 * np.power((x - mu)/(mu*reso/2.35), 2))


## Polynomial 1
def poly1(x, A, B):
    return A + B* x

def gaussPoly1(x, mu, sigma, N, A, B) :
    return gauss(x, mu, sigma, N) + poly1(x, A, B)


def gaussPoly1_reso(x, mu, reso, N, A, B) :
    return gauss_reso(x, mu, reso, N) + poly1(x, A, B)


def gaussExpo_reso(x, mu, reso, N, C, s) :
    return gauss_reso(x, mu, reso, N) + bkg_exp(x, C, s)


## Polynomial 2
def poly2(x, A, B, C):
    return A + B * x + C * np.power (x, 2)

def gaussPoly2(x, mu, sigma, N, A, B, C) :
    return gauss(x, mu, sigma, N) + poly2(x, A, B, C)


## Polynomial 3
def poly3(x, A, B, C, D):
    return A + B* x + C*  np.power (x, 2) +  D * np.power (x, 3)

def gaussPoly3(x, mu, sigma, N, A, B, C, D) :
    return gauss(x, mu, sigma, N) + poly3(x, A, B, C, D)

## Exponential
def bkg_exp(x, C, s):
    return C * np.exp(x * s)

### parece que para el plotting teníamos que poner la normalizacion, REVISAR
def gaussNorm(x, mu, sigma, N):
    return (N*np.exp(-0.5 * np.power((x - mu)/(sigma),2 ))/( sigma * np.sqrt( 2 * np.pi)))


def gaussExp(x, mu, sigma, N, C, s) :
    return gaussNorm(x, mu, sigma, N) + bkg_exp(x, C, s)

def expNorm(x, C, s, xmin, xmax):
    return C * s * np.exp(-x * s) /  (np.exp(-s * xmin) - np.exp(-s * xmax))

## Fit to Gaussian +  Exponential both normalized
def gaussExp_Norm(x, mu, sigma, N, C, s, xmin, xmax) :
    return gaussNorm(x, mu, sigma, N) + expNorm(x, C, s, xmin, xmax)


##
def poisson_sigma(x, default=3):
    """
    Get the uncertainty of x (assuming it is poisson-distributed).
    Set *default* when x is 0 to avoid null uncertainties.
    """
    u = x**0.5
    u[x==0] = default
    return u
