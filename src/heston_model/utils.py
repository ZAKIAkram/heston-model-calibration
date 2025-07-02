import numpy as np

from scipy.optimize import brentq
from simulate_monte_carlo import simulate_black_scholes_mc

def implied_vol(price, S, K, T, r, option_type="call"):
    def objective(sigma):
        return simulate_black_scholes_mc(S, r, sigma, T, K, option_type=option_type) - price
    try:
        return brentq(objective, 1e-6, 3.0, maxiter=100)
    except ValueError:
        return np.nan
    

