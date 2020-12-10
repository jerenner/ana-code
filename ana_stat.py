import numpy  as np
import pandas as pd


def error_eff(ntot, eff):
    return np.sqrt(eff*(1-eff)/ntot)


def cov(x, y, w):

    """
    Weighted covariance
    note: weights must be all same sign, careful!
    """

    x_w  = np.average(x, weights=w)
    y_w  = np.average(y, weights=w)
    xy_w = np.average(x*y, weights=w)

    return xy_w - x_w * y_w
    #return np.sum(w * (x - x_w) * (y - y_w)) / np.sum(w)

def corr_pearson(x, y, w):
    """Weighted correlation"""
    return cov(x, y, w) / np.sqrt(cov(x, x, w) * cov(y, y, w))


def map_for_corr_calc(map):

    """
    Input: map
    Returns a map dataframe with x, y and e0 in columns
    """

    map_redone = np.zeros(shape=(len(map.e0)*len(map.e0),3))
    e0_flatten = map.e0.values.flatten()
    c = 0

    for i in range(len(map.e0)):
        for j in range(len(map.e0)):
            map_redone[c][0] = i;
            map_redone[c][1] = j;
            c += 1
    for i in range(len(e0_flatten)):
        map_redone[i][2] = e0_flatten[i]

    df = pd.DataFrame(map_redone)
    df.columns = ['x', 'y', 'e0']
    df = df.dropna()

    correlation = corr_pearson(df['x'], df['y'], df['e0'])
    print(f'corr  = {correlation}')

    return df, correlation


def map_for_corr_calc_pass_e0(map):

    """
    Input: map.e0 (to easier sns comparisons between maps)
    Returns a map dataframe with x, y and e0 in columns
    """

    map_redone = np.zeros(shape=(len(map)*len(map),3))
    e0_flatten = map.values.flatten()
    c = 0

    for i in range(len(map)):
        for j in range(len(map)):
            map_redone[c][0] = i;
            map_redone[c][1] = j;
            c += 1
    for i in range(len(e0_flatten)):
        map_redone[i][2] = e0_flatten[i]

    df = pd.DataFrame(map_redone)
    df.columns = ['x', 'y', 'e0']
    df = df.dropna()

    correlation = corr_pearson(df['x'], df['y'], df['e0'])
    print(f'corr = {correlation}')

    return correlation


"""
+- before the term 2rho would be negative when the variables a positively correlated
R * sqrt [ (relative_error_sigma)^2 +  (relative_error_mu)^2 - 2rho * relative_error_sigma *  relatvie_error_mu]

cov = rho *a_u*a_b
a/b

cov from minuit example:
minuit.print_matrix()
minuit.np_covariance()[0][1]
"""

def error_on_a_fraction(a, a_u, b, b_u, cov):
    value = a/b
    error =  a/b * np.sqrt(( a_u / a)**2 + ( b_u/ b )**2 - 2 * cov/(np.abs(a*b)))
    print(f'value = {value} +- {error}')
    return error



def error_on_a_fraction2(a, a_u, b, b_u):
    value = a/b
    error =  a/b * np.sqrt(( a_u/a)**2 + (b_u/b)**2)
    print(f'value = {value} +- {error}')
    return error
