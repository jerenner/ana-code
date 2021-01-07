import numpy  as np
import probfit

def gausstext(params, errors, mu1, mu2):
    mean  = np.array([params[1], errors[1]])
    sigma = np.array([params[2], errors[2]])
    
    label  = f'R({mu1} keV) = {sigma[0]/mean[0] * 235:.2f}%\n'
    label += f'R({mu2} keV) = {sigma[0]/mean[0] * 235 * np.sqrt(mu1/mu2):.2f}%'
    
    return label

def expo(x, tau):
        a0 = 1/(tau*(np.exp(-fit_range[0]/tau)-np.exp(-fit_range[1]/tau)))
        return a0*np.exp(-x/tau)
    
def expo_and_gauss(x, const, mean, amp, mu, sigma):
    if sigma <= 0.:
        return np.inf
    
    return const * np.exp(-x*mean) + amp/(2*np.pi)**.5/sigma * np.exp(-0.5*(x-mu)**2./sigma**2.)

def find_numb_of_events_ml_unbinned_wide(fit_result, fit_range, exp, gauss, e_min, e_max, pars):

    s_wide     = fit_result.values['Ns']
    err_s_wide = fit_result.errors['Ns']
    b_wide     = fit_result.values['Nb']
    err_b_wide = fit_result.errors['Nb']
    mu         = fit_result.values['mu']
    err_mu     = fit_result.errors['mu']
    sigma      = fit_result.values['sigma']
    err_sigma  = fit_result.errors['sigma']
    tau        = fit_result.values['tau']
    err_tau    = fit_result.errors['tau']
    cov_sb     = fit_result.covariance['Ns', 'Nb']
    
    cov_smu     = fit_result.covariance['Ns', 'mu']
    cov_ssigma  = fit_result.covariance['Ns', 'sigma']
    cov_musigma = fit_result.covariance['mu', 'sigma']
    covbtau     = fit_result.covariance['Nb', 'tau']

    integral_sig  = integrate.quad(gauss, e_min, e_max, args=(mu, sigma, s_wide))
    integral_bckg = integrate.quad(exp, e_min, e_max, args=(tau, b_wide))

    s = integral_sig[0]
    b = integral_bckg[0]
    tot = s+b
    
    def der_g_ns(x, mu, sigma, ns):
        return 1/(2*np.pi)**.5/sigma * np.exp(-0.5*(x-mu)**2./sigma**2.)
    def der_g_mu(x, mu, sigma, ns):
        return ns/(2*np.pi)**.5 * np.exp(-0.5*(x-mu)**2./sigma**2.) * (x-mu)/sigma**3
    def der_g_sigma(x, mu, sigma, ns):
        return ns * np.exp(-0.5*(x-mu)**2./sigma**2.)*(x-mu)**2/(2*np.pi)**.5/sigma**4 - ns*np.exp(-0.5*(x-mu)**2./sigma**2.)/(2*np.pi)**.5/sigma**2

    der_i_ns    = integrate.quad(der_g_ns,    e_min, e_max, args=(mu, sigma, s_wide))
    der_i_mu    = integrate.quad(der_g_mu,    e_min, e_max, args=(mu, sigma, s_wide))
    der_i_sigma = integrate.quad(der_g_sigma, e_min, e_max, args=(mu, sigma, s_wide))
    
    var_s = (der_i_ns[0]*err_s_wide)**2 + (der_i_mu[0]*err_mu)**2 + (der_i_sigma[0]*err_sigma)**2 + 2*der_i_mu[0]*der_i_sigma[0]*cov_musigma + 2*der_i_mu[0]*der_i_ns[0]*cov_smu + 2*der_i_sigma[0]*der_i_ns[0]*cov_ssigma
    
    def der_e_nb(x, tau, nb):
        a0 = 1/(tau*(np.exp(-fit_range[0]/tau)-np.exp(-fit_range[1]/tau)))
        return a0*np.exp(-x/tau)
    def der_e_tau(x, tau, nb):
        den = np.exp(-e_min_plot_one/tau) - np.exp(-e_max_plot_one/tau)
        exp = np.exp(-x/tau)
        return b_wide*(-1/tau**2*exp/den  + 1/tau*(x/tau**2*exp/den-exp/den**2/tau**2*(e_min_plot_one*np.exp(-e_min_plot_one/tau) - e_max_plot_one*np.exp(-e_max_plot_one/tau))))
    
    der_i_nb = integrate.quad(der_e_nb, e_min, e_max, args=(tau, b_wide))
    der_i_tau = integrate.quad(der_e_tau, e_min, e_max, args=(tau, b_wide))
    
    var_b = (der_i_nb[0]*err_b_wide)**2 + (der_i_tau[0]*err_tau)**2 + 2*der_i_tau[0]*der_i_nb[0]*covbtau

    return (tot, s, b, np.sqrt(var_s), np.sqrt(var_b))

def sig_and_bckg_after_cut_MC(df_tracks, threshold, pdf, e_min_one, e_max_one, pars, fPrint = False, elabel='energy_z'):
    df_after_cut = df_tracks[df_tracks.eblob2.values > threshold]
    energy = df_after_cut[elabel].values
    
    unbinned_likelihood = probfit.UnbinnedLH(pdf, energy, extended=True)
    pars = dict(Ns=len(energy[coref.in_range(energy, e_min_one, e_max_one)]), Nb=len(energy), tau=pars['tau'], mu=pars['mu'], sigma=pars['sigma'])
    #pars = dict(Ns=1000, Nb=300, tau=65, mu=1592, sigma=5)
    fit_range = [e_min_one, e_max_one]

    minuit = iminuit.Minuit(unbinned_likelihood, pedantic=False, print_level=fPrint, **pars)
    minuit.migrad()
    
    if fPrint:
        unbinned_likelihood.show(minuit, bins=80, parts=True);
        minuit.print_fmin()
        minuit.matrix(correlation=True)

    n_tot_after, s_after, b_after, err_s, err_b = find_numb_of_events_ml_unbinned_wide(minuit, fit_range, norm_expo, gauss, e_min_one, e_max_one, pars)
    print('Between {0} and {1}, number of signal = {2} +- {3}, background = {4} +- {5}'.format(e_min_one, e_max_one, s_after, err_s, b_after, err_b))
    
    return (n_tot_after, s_after, b_after, err_s, err_b)
