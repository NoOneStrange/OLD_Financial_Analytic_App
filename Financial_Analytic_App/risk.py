import numpy as np
import pandas as pd
from scipy import stats as st

class RiskElements():
    def __init__(self, returns: pd.Series):
        self.returns = returns.dropna()
        self.mu = self.returns.mean()
        self.sigma = self.returns.std()

    def historical_var(self, alpha: float):
        """Historyczny VaR"""
        return self.returns.quantile(alpha)

    def monte_carlo_simulation(
        self, 
        n_days: int, 
        n_simulations: int, 
        start_value: float = 1.0,
        distribution=st.norm
    ) -> pd.DataFrame:
        """
        Poprawna symulacja Monte Carlo:
        - dopasowanie teoretycznego rozkładu do empirycznych log-returns
        - multiplikatywne generowanie ścieżek
        """
        # dopasowanie rozkładu
        params = distribution.fit(self.returns)
        fitted_dist = distribution(*params)

        # przygotowanie pustej tablicy
        simulation = pd.DataFrame(
            columns=[f't_{t}' for t in range(n_days + 1)],
            index=[f's_{i:05}' for i in range(1, n_simulations + 1)]
        )

        # symulacja ścieżek
        for t in range(n_days + 1):
            if t == 0:
                simulation.iloc[:, t] = start_value
            else:
                simulation.iloc[:, t] = simulation.iloc[:, t-1] * np.exp(fitted_dist.rvs(size=n_simulations))

        return simulation

    @staticmethod
    def monte_carlo_var(simulation: pd.DataFrame, alpha: float):
        """VaR z końcowych wartości symulacji MC"""
        final_values = simulation.iloc[:, -1]
        return final_values.quantile(alpha)
