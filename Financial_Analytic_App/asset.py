import numpy as np
import pandas as pd

class Asset:
    """
    Klasa reprezentująca pojedyncze aktywo finansowe.
    Odpowiada za przechowywanie cen i obliczanie stóp zwrotu.
    """

    def __init__(self, ticker, prices):
        """
        Parametry:
        - ticker: symbol instrumentu
        - prices: seria lub DataFrame z cenami zamknięcia
        """
        self.ticker = ticker
        self.prices = self._prepare_prices(prices)
        self.returns = self._calculate_log_returns()

    def _prepare_prices(self, prices):
        """
        Przygotowuje dane cenowe:
        - jeśli DataFrame → wybiera kolumnę tickera
        - usuwa braki danych
        """
        if isinstance(prices, pd.DataFrame):
            prices = prices[self.ticker]
        
        return prices.dropna()
    
    def _calculate_log_returns(self):
        returns = np.log(self.prices / self.prices.shift(1))
        
        return returns.dropna()
