# Financial Risk Analysis App

Aplikacja służy do analizy ryzyka finansowego wybranych instrumentów finansowych. Umożliwia wczytywanie danych cenowych, obliczanie stóp zwrotu, wizualizację danych, obliczanie historycznego Value at Risk (VaR) oraz symulacje Monte Carlo.

---

## Funkcjonalności

- Pobieranie danych cenowych z serwisu [Stooq](https://stooq.pl) dla wybranych tickerów.
- Obliczanie logarytmicznych stóp zwrotu.
- Wyświetlanie wykresów cen i stóp zwrotu.
- Podstawowe statystyki opisowe (średnia, odchylenie standardowe, min, max, kwantyle).
- Porównanie aktywa z benchmarkiem rynkowym (np. WIG, S&P 500, DAX).
- Wizualizacja rozkładów stóp zwrotu z dopasowaniem do teoretycznych rozkładów.
- Obliczanie historycznego Value at Risk (VaR).
- Symulacje Monte Carlo do prognozowania wartości instrumentu i wyznaczania VaR.

---

## Struktura projektu i opis plików

### 1. `asset.py`
Reprezentuje pojedyncze aktywo finansowe i oblicza jego logarytmiczne stopy zwrotu.

**Klasa `Asset`**  
- `ticker` – symbol instrumentu (np. `"AAPL.US"`).  
- `prices` – seria cen zamknięcia po przygotowaniu danych.  
- `returns` – logarytmiczne stopy zwrotu (`log(P_t / P_{t-1})`).  

**Metody prywatne:**  
- `_prepare_prices(prices)` – usuwa braki danych i wybiera kolumnę odpowiednią dla tickera, jeśli podano DataFrame.  
- `_calculate_log_returns()` – oblicza logarytmiczne stopy zwrotu.  

---

### 2. `analytics.py`
Analiza statystyczna aktywów oraz wykresy histogramów.

**Klasa `AssetAnalytics`**  
- `returns` – seria stóp zwrotu aktywa.  
- `benchmark` – opcjonalny benchmark do porównania.  
- `alpha` – poziom istotności (np. 0.05).  

**Metody:**  
- `basic_statistics()` – zwraca podstawowe statystyki opisowe: średnia, odchylenie standardowe, min, max, kwantyle.  
- `plot_hist_with_quantile_fit()` – tworzy histogram stóp zwrotu z:
  - zaznaczonym kwantylem `alpha`,  
  - wypełnieniem obszaru poniżej kwantyla,  
  - dopasowaniem do rozkładów teoretycznych: `norm`, `laplace`, `hypsecant`,  
  - testem zgodności K-S dla dopasowania.  

---

### 3. `data_loader.py`
Pobieranie i przygotowanie danych cenowych z internetu.

**Funkcje:**  
- `working_days(start, end)` – zwraca indeks dni roboczych z WIG w zadanym okresie.  
- `all_days(start, end)` – zwraca wszystkie dni kalendarzowe w zadanym okresie.  
- `load_prices(tickers, start, end, freq='WD')` – pobiera ceny zamknięcia dla listy tickerów, obsługuje:
  - `WD` → tylko dni robocze,  
  - inne interwały (`1W`, `ME`, itd.) → resampling.  
- `get_default_benchmark(ticker)` – zwraca domyślny benchmark dla tickera:
  - `.US` → `^SPX`,  
  - `.DE` → `DAX`,  
  - inne → `WIG`.  

---

### 4. `plots.py`
Wizualizacja danych finansowych i wyników symulacji Monte Carlo.

**Funkcje:**  
- `plot_prices(prices, ticker)` – wykres cen zamknięcia.  
- `plot_returns(returns, ticker)` – wykres logarytmicznych stóp zwrotu.  
- `plot_monte_carlo(simulation, alpha, max_paths=1000)` – wykres Monte Carlo:  
  - lewy panel: ścieżki, średnia, kwantyle,  
  - prawy panel: histogram końcowych wartości.  
- `plot_monte_carlo_var(simulation, var_mc, alpha)` – wykres Monte Carlo z zaznaczonym VaR, każda ścieżka w innym kolorze.  

---

### 5. `risk.py`
Obliczenia ryzyka i symulacje Monte Carlo dla aktywów.

**Klasa `RiskElements`**  
- `returns` – stopy zwrotu aktywa.  
- `mu` – średnia stóp zwrotu.  
- `sigma` – odchylenie standardowe stóp zwrotu.  

**Metody:**  
- `historical_var(alpha)` – oblicza historyczny VaR (kwantyl `alpha`).  
- `monte_carlo_simulation(n_days, n_simulations, start_value=1.0, distribution=st.norm)` – generuje multiplikatywne ścieżki Monte Carlo, dopasowując rozkład teoretyczny do danych.  
- `monte_carlo_var(simulation, alpha)` – oblicza VaR z końcowych wartości symulacji.  

---

### 6. `app.py`
Interfejs użytkownika w Streamlit.

**Sekcje:**  
1. Nagłówek aplikacji – imię, nazwisko, grupa.  
2. Panel boczny – konfiguracja analizy:
   - tickery, zakres dat, alpha, liczba dni i ścieżek MC.  
3. Przygotowanie danych – wczytywanie cen, tworzenie obiektów `Asset`.  
4. Wykresy cen i stóp zwrotu – dla każdego aktywa.  
5. Statystyki bazowe – wyświetlane za pomocą `AssetAnalytics.basic_statistics()`.  
6. Histogramy stóp zwrotu – z kwantylami i dopasowanymi rozkładami.  
7. Historyczny VaR – z `RiskElements.historical_var()`.  
8. Monte Carlo – symulacje, wykresy i VaR MC.  
9. Tabela wyników Monte Carlo – pierwsze 10 scenariuszy dla każdej symulacji.  

---

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone <URL_REPOZYTORIUM>
cd <KATALOG_PROJEKTU>

streamlit run app.py

