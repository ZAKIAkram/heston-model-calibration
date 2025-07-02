import pytest
import numpy as np

from heston_model.simulate_monte_carlo import simulate_black_scholes_mc
from heston_model.explicit_black_scholes import black_scholes_price



@pytest.fixture
def black_scholes_params():
    return [100., 0.05, 0.2, 1, 110.]


def test_simulate_black_scholes_mc(black_scholes_params):
    mc_price = simulate_black_scholes_mc(*black_scholes_params, n_paths=100000)
    bs_price = black_scholes_price(*black_scholes_params)
    assert np.isclose(mc_price, bs_price, rtol=1e-2), f"MC price {mc_price} differs from BS price {bs_price}"
    