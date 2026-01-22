import streamlit as st
from datetime import datetime as dt
import pandas as pd
import numpy as np

from asset import Asset
from analytics import AssetAnalytics
from data_loader import load_prices, get_default_benchmark
from risk import RiskElements
from plots import plot_prices, plot_returns, plot_monte_carlo, plot_monte_carlo_var

# =======================
# Nagłówek aplikacji
# =======================
first_name = "Michał"
last_name = "Szymik"
grupa = "GC03"

st.title("Financial Risk Analysis App")
st.caption(f"{last_name} | {first_name} | {grupa}")

# =======================
# PANEL BOCZNY (INPUT)
# =======================
st.sidebar.header("Ustawienia analizy")

tickers = st.sidebar.text_input("Tickery (oddzielone przecinkami)", value="AAPL.US")
start_date = st.sidebar.date_input("Data początkowa", value=dt(2018, 1, 1))
end_date = st.sidebar.date_input("Data końcowa", value=dt.today())
alpha = st.sidebar.slider("Poziom istotności (alpha)", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
n_days = st.sidebar.number_input("Liczba dni symulacji MC", min_value=10, max_value=500, value=252)
n_simulations = st.sidebar.number_input("Liczba ścieżek MC", min_value=100, max_value=5000, value=1000, step=100)

# =======================
# PRZYGOTOWANIE DANYCH
# =======================
ticker_list = [t.strip().lower() for t in tickers.split(",")]

if st.sidebar.button("Uruchom analizę"):
    try:
        prices_df = load_prices(tickers=ticker_list, start=start_date, end=end_date)
        
        # Tworzenie obiektów Asset
        assets = {ticker: Asset(ticker, prices_df) for ticker in ticker_list}
        
    except Exception as e:
        st.error(f"Błąd podczas wczytywania danych: {e}")
        st.stop()

    # =======================
    # Wykresy cen
    # =======================
    st.subheader("Dane cenowe")
    cols = st.columns(len(assets))
    for i, (ticker, asset) in enumerate(assets.items()):
        with cols[i]:
            st.pyplot(plot_prices(asset.prices, ticker))
    
    # =======================
    # Dane cenowe (tabela)
    # =======================
    st.subheader("Ceny zamknięcia")
    for ticker, asset in assets.items():
        st.markdown(f"**{ticker.upper()}**")
        st.dataframe(asset.prices.head(10))

    # =======================
    # Wykresy stóp zwrotu
    # =======================
    st.subheader("Stopy zwrotu")
    cols = st.columns(len(assets))
    for i, (ticker, asset) in enumerate(assets.items()):
        with cols[i]:
            st.pyplot(plot_returns(asset.returns, ticker))

    # =======================
    # Statystyki bazowe
    # =======================
    st.subheader("Statystyki bazowe")
    cols = st.columns(len(assets))
    for i, (ticker, asset) in enumerate(assets.items()):
        with cols[i]:
            st.markdown(f"**{ticker.upper()}**")
            stats_df = AssetAnalytics(asset.returns, alpha=alpha).basic_statistics()
            st.dataframe(stats_df, use_container_width=True)

    # =======================
    # Histogramy z kwantylami i dopasowanymi rozkładami
    # =======================
    st.subheader("Histogramy stóp zwrotu z benchmarkiem i dopasowanymi rozkładami")
    for ticker, asset in assets.items():
        benchmark_ticker = get_default_benchmark(ticker)
        benchmark_prices = load_prices(tickers=[benchmark_ticker], start=start_date, end=end_date)
        benchmark_returns = np.log(
            benchmark_prices[benchmark_ticker] / benchmark_prices[benchmark_ticker].shift(1)
        ).dropna().rename(benchmark_ticker)
        
        combined = pd.concat([benchmark_returns, asset.returns], axis=1, join="inner")
        fig = AssetAnalytics(combined.iloc[:, 1], benchmark=combined.iloc[:, 0], alpha=alpha).plot_hist_with_quantile_fit()
        st.pyplot(fig)

    # =======================
    # Historyczny VaR
    # =======================
    st.subheader("Historyczny VaR")
    cols = st.columns(len(assets))
    for i, (ticker, asset) in enumerate(assets.items()):
        risk = RiskElements(asset.returns)
        var_hist = risk.returns.quantile(alpha)  # bez print
        with cols[i]:
            st.metric(label=ticker, value=f"{var_hist:.4f}")

    # =======================
    # Monte Carlo i Monte Carlo VaR
    # =======================
    st.subheader("Monte Carlo")
    cols = st.columns(len(assets))
    for i, (ticker, asset) in enumerate(assets.items()):
        simulation = risk.monte_carlo_simulation(n_days=n_days, n_simulations=n_simulations)
        var_mc = RiskElements.monte_carlo_var(simulation, alpha)

        with cols[i]:
            st.metric(label=f"{ticker} Monte Carlo VaR", value=f"{var_mc:.4f}")
            st.pyplot(plot_monte_carlo(simulation, alpha))
            st.pyplot(plot_monte_carlo_var(simulation, var_mc, alpha))

            # --- tabela z wynikami Monte Carlo ---
            st.markdown(f"**Tabela pierwszych 10 scenariuszy MC dla {ticker}**")
            st.dataframe(simulation.head(10))


