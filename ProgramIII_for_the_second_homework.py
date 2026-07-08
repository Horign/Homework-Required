import numpy as np
def monte_carlo_stock(S0, mu, sigma, T, N_sim, N_step):
    dt = T / N_step
    rand = np.random.normal(0, np.sqrt(dt), (N_sim, N_step))
    drift = (mu - 0.5 * sigma ** 2) * dt
    shock = sigma * rand
    log_returns = drift + shock
    log_path = np.cumsum(log_returns, axis=1)
    price_path = S0 * np.exp(log_path)
    price_path = np.hstack([np.full((N_sim,1), S0), price_path])
    return price_path
paths = monte_carlo_stock(S0=100, mu=0.08, sigma=0.2, T=1, N_sim=5000, N_step=252)
print("shape of path：", paths.shape)
