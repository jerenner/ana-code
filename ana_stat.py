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
