import numpy as np

def simulate_heston_mc(S0, T, r, kappa, theta, ksi, rho, v0, K, n_paths=10000, n_steps=100, option_type="call"):
    dt = T / n_steps
    prices = np.full(n_paths, S0, dtype=np.float64)
    v = np.full(n_paths, v0, dtype=np.float64)
    for _ in range(n_steps):
        z1 = np.random.normal(size=n_paths)
        z2 = z1 * rho + np.sqrt(1 - rho ** 2) * np.random.normal(size=n_paths)
        v += kappa * (theta - v) * dt + ksi * np.sqrt(v * dt) * z2
        prices *= np.exp((r - 0.5 * v) * dt + np.sqrt(v * dt) * z1)
    if option_type == "call":
        payoffs = np.maximum(prices - K, 0.)
    else:
        payoffs = np.maximum(K - prices, 0.)
    return np.exp(-r * T) * np.mean(payoffs)


def simulate_black_scholes_mc(S0, r, sigma, T, K, n_paths=100000, n_steps=100, option_type="call"):
    dt = T / n_steps
    prices = np.full(n_paths, S0, dtype=np.float64)
    for _ in range(n_steps):
        prices *= np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * np.random.normal(size=n_paths))
    if option_type == "call":
        payoffs = np.maximum(prices - K, 0)
    else:
        payoffs = np.maximum(K - prices, 0)
    return np.exp(-r * T) * np.mean(payoffs)


def main():
    print(simulate_heston_mc(100., 1, 0.05, 0.1, 0.5, 0.1, 0.2, 0.2, 110))
    print(simulate_black_scholes_mc(100, 0.05, 0.2, 1, 110))

if __name__ == "__main__":
    main()