import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

def key(s):
    """Normalise a state name for matching: drop hyphens, line breaks and spaces, lowercase."""
    return s.replace('-', '').replace('\n', '').replace(' ', '').lower()

def plot_correlation(df, cols, targets, methods=('pearson', 'spearman'), label='all states'):
    """Plot a heatmap of correlations between `cols` and each target column, one per method.

    targets: dict mapping a display name to a column, e.g. {'BEV share': 'bev_share_ytd26'}
    """
    features = df[cols]
    for method in methods:
        corr = pd.DataFrame({
            name: features.corrwith(df[col], method=method)
            for name, col in targets.items()
        }).T

        fig, ax = plt.subplots(figsize=(12, 4))
        sns.heatmap(corr, annot=True, vmin=-1, vmax=1, cmap='coolwarm', fmt='.2f', ax=ax)
        ax.set_title(f"{method.capitalize()} correlation - {label}")
        ax.tick_params(axis='x', labelrotation=45)
        ax.tick_params(axis='y', labelrotation=0)
        plt.setp(ax.get_xticklabels(), ha='right')

        plt.tight_layout()
        plt.show()

def to_count(s):
    """Convert a KBA count column to int, treating '-' as 0."""
    return pd.to_numeric(s.replace('-', 0), errors='raise').astype(int)

def p_test(df, cols, targets, method):
    """Correlation coefficient and p-value for every pair of `cols` and `targets` columns.

    method: 'pearson' or 'spearman'
    """
    tests = {'pearson': pearsonr, 'spearman': spearmanr}
    if method not in tests:
        raise ValueError(f"method must be 'pearson' or 'spearman', got {method!r}")
    test = tests[method]

    results = []
    for col in cols:
        for target in targets:
            result = test(df[col], df[target])
            results.append({
                'target': target,
                'feature': col,
                'method': method,
                'coef': result.statistic,
                'p_value': result.pvalue,
            })
    return pd.DataFrame(results)