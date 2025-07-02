import numpy as np

from src.heston_model.calibration import calibrate_heston


def test_calibrate_heston():
    market_data = np.array([0.2, 0.1, 0.3, -0.5, 0.05])
    params = calibrate_heston(market_data)
    assert isinstance(params, dict)
    # assert set(params.keys()) == {"kappa", "theta", "sigma", "rho", "v0"}



