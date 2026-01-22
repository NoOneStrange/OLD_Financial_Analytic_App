import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st

class AssetAnalytics:
    def __init__(self, returns, benchmark = None, alpha = 0.05):
        self.returns = returns
        self.benchmark = benchmark
        self.alpha = alpha

    def basic_statistics(self):
        stats = self.returns.describe(percentiles=[self.alpha, 1-self.alpha]).drop(['50%','count']).map(lambda x: f'{x:.2%}')

        return stats
    
    def plot_hist_with_quantile_fit(self):
        asset_returns = self.returns
        benchmark = self.benchmark
        alpha = self.alpha

        nbins = int(len(asset_returns) ** 0.5)
        fig, ax = plt.subplots(figsize=(7, 4))

        if benchmark is not None:
            ax.hist(
                benchmark,
                bins=nbins,
                density=True,
                alpha=0.4,
                color="grey",
                label=benchmark.name
            )

        ax.hist(
            asset_returns,
            bins=nbins,
            density=True,
            alpha=0.5,
            color="green",
            label=asset_returns.name
        )

        # kwantyl
        q = asset_returns.quantile(alpha)
        ymin, ymax = ax.get_ylim()
        
        ax.annotate(
            f"q_{alpha:.2f} = {q:.2%}",
            xy=(q, 0),
            xytext=(q, ymax * 0.9),
            ha="center",
            arrowprops=dict(arrowstyle="->"),
            bbox=dict(boxstyle="round", fc="white")
        )
        ax.fill_betweenx([0, ymax], asset_returns.min(), q, alpha=0.2)

        # dopasowane rozkłady
        x = np.linspace(asset_returns.min(), asset_returns.max(), 300)
        for name, color in zip(["norm", "hypsecant", "laplace"], ["red", "orange", "purple"]):
            dist = getattr(st, name)
            params = dist.fit(asset_returns)
            fitted = dist(*params)
            ks = st.kstest(asset_returns, fitted.cdf)
            ax.plot(
                x,
                fitted.pdf(x),
                linestyle="--",
                color=color,
                label=f"{name}, K-S={ks.statistic:.3f}"
            )

        ax.set_title(asset_returns.name)
        ax.set_xlabel("Stopa zwrotu")
        ax.set_ylabel("Gęstość")
        ax.legend()

        return fig