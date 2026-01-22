import pandas as pd
from datetime import datetime as dt
from tqdm import tqdm

def working_days(start, end):
    """
    Zwraca indeks dni roboczych na podstawie notowań indeksu WIG (Stooq).
    Wykorzystywane do dopasowania kalendarza notowań.
    """
    index_dates = pd.read_csv(
        filepath_or_buffer = "https://stooq.pl/q/d/l/?s=wig&i=d",
        usecols = ['Data'],
        index_col = 'Data',
        parse_dates = True
    ).truncate(before = start, after = end)
    
    return index_dates

def all_days(start, end):
    """
    Zwraca indeks wszystkich dni kalendarzowych w zadanym okresie.
    """
    index_dates = pd.DataFrame(
        index = pd.date_range(start = start, end = end, freq = 'D')
    )

    return index_dates

def load_prices(tickers, start, end, freq='WD'):
    """
    Wczytuje dane cenowe z serwisu Stooq dla listy tickerów.

    Parametry:
    - tickers: lista symboli (np. ['AAPL.US', 'MSFT.US'])
    - start, end: zakres dat
    - freq:
        'WD'  -> tylko dni robocze
        inne  -> resampling do zadanej częstotliwości

    Zwraca:
    - DataFrame z cenami zamknięcia
    """

    freqs = ('WD', '1W', '2W', '3W', 'ME', '2M')
    if freq not in freqs:
        raise ValueError(f'Nieobsługiwany interwał: {freq}, użyj np. {freqs}')

    # baza dat
    if freq == 'WD':
        df_merged = working_days(start, end)
    else:
        df_merged = all_days(start, end)

    for ticker in tqdm(tickers, desc='Pobieranie danych...'):
        url = f"https://stooq.pl/q/d/l/?s={ticker.lower()}&i=d"

        df_temp = pd.read_csv(
            url,
            index_col='Data',
            parse_dates=True
        )

        # normalizacja nazwy kolumny z ceną zamknięcia
        close_col = None
        for col in df_temp.columns:
            if "zamk" in col.lower() or "close" in col.lower():
                close_col = col
                break

        if close_col is None:
            raise ValueError(f"Nie znaleziono kolumny z cenami w danych dla {ticker}")

        df_temp = df_temp[[close_col]].rename(columns={close_col: ticker})
        df_temp = df_temp.truncate(before=start, after=end)

        df_merged = pd.merge(
            left=df_merged,
            right=df_temp,
            how='left',
            left_index=True,
            right_index=True
        )

    df_merged = df_merged.ffill().dropna()

    if freq == 'WD':
        return df_merged
    else:
        return df_merged.asfreq(freq)
    
def get_default_benchmark(ticker):
    """
    Zwraca domyślny benchmark rynkowy dla danego instrumentu.
    """
    ticker = ticker.lower()

    if ticker.endswith(".us"):
        return "^spx" 
    elif ticker.endswith(".de"):
        return "dax"
    else:
        return "wig"