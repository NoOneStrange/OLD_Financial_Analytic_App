import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

def plot_prices(prices: pd.Series, ticker: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(prices.index, prices.values)
    ax.set_title(f"Ceny instrumentu: {ticker}")
    ax.set_xlabel("Data")
    ax.set_ylabel("Cena")
    ax.grid(True)
    return fig

def plot_returns(returns: pd.Series, ticker: str):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(returns.index, returns.values)
    ax.set_title(f"Logarytmiczne stopy zwrotu: {ticker}")
    ax.set_xlabel("Data")
    ax.set_ylabel("Stopa zwrotu")
    ax.grid(True)
    return fig

def plot_monte_carlo(simulation: pd.DataFrame, alpha: float, max_paths: int = 1000):
    """
    Poprawny wykres Monte Carlo (multiplikatywne ścieżki):
    - lewy panel: ścieżki, średnia, kwantyle
    - prawy panel: histogram końcowy
    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(18, 5),
        sharey=True,
        gridspec_kw={"width_ratios": [3, 1]}
    )

    # --- lewy panel: ścieżki ---
    ax[0].plot(simulation.head(max_paths).T, color="grey", alpha=0.05)
    ax[0].plot(simulation.mean(axis=0), color="red", linestyle="--", label="E(V)")
    ax[0].plot(simulation.quantile(alpha, axis=0), color="green", linestyle="--", label=f"q_{alpha}")
    ax[0].plot(simulation.quantile(1-alpha, axis=0), color="green", linestyle="--", label=f"q_{1-alpha}")
    ax[0].set_title("Symulacja Monte Carlo")
    ax[0].set_xlabel("Dzień")
    ax[0].set_ylabel("Wartość")
    ax[0].legend()
    ax[0].grid(True)

    # --- prawy panel: histogram końcowy ---
    final_values = simulation.iloc[:, -1]
    ax[1].hist(final_values, bins=int(len(final_values)**0.5), orientation="horizontal", density=True, color="grey")
    ax[1].axhline(final_values.mean(), color="red", linestyle="--", label="E(V)")
    ax[1].axhline(final_values.quantile(alpha), color="green", linestyle="--", label=f"q_{alpha}")
    ax[1].axhline(final_values.quantile(1-alpha), color="green", linestyle="--", label=f"q_{1-alpha}")
    ax[1].legend()
    ax[1].grid(True)

    return fig

def plot_monte_carlo_var(simulation: pd.DataFrame, var_mc: float, alpha: float):
    """
    Wykres Monte Carlo z zaznaczonym VaR, każda ścieżka w innym kolorze.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    n_paths = simulation.shape[0]

    # --- losowe kolory dla ścieżek ---
    colors = np.random.rand(n_paths, 3)  # RGB: [0-1,0-1,0-1]

    for i, path in enumerate(simulation.itertuples(index=False)):
        ax.plot(range(simulation.shape[1]), path, color=colors[i], alpha=0.5)

    # --- średnia ścieżek ---
    ax.plot(simulation.mean(axis=0), color="black", linestyle="--", linewidth=2, label="Średnia (E[V])")

    # --- VaR ---
    ax.axhline(var_mc, linestyle="--", color="red", linewidth=2, label=f"VaR (alpha={alpha})")

    ax.set_title("Monte Carlo z Value at Risk")
    ax.set_xlabel("Dzień")
    ax.set_ylabel("Wartość")
    ax.legend()
    ax.grid(True)
    
    return fig