# src/visualization.py

import matplotlib.pyplot as plt
import pandas as pd


def plot_trends(
    df: pd.DataFrame,
    slopes: dict,
    date_col: str = 'Date',
    score_col: str = 'Score',
    user_col: str = 'User',
    status: dict = None,
    figsize: tuple = (10, 6),
    out_path: str = None
):
    """
    Plot comparative wellness score trends for multiple users.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing `date_col`, `user_col`, and `score_col`.
    slopes : dict
        Mapping user -> numeric slope (from compute_slopes).
    date_col : str
        Name of the date column.
    score_col : str
        Name of the score column.
    user_col : str
        Name of the user identifier column.
    status : dict, optional
        Mapping user -> 'improving' or 'declining'. If None, inferred from `slopes`.
    figsize : tuple, optional
        Matplotlib figure size.
    out_path : str, optional
        If provided, saves the plot to this filepath.
    """
    # Infer status if not provided
    if status is None:
        status = {u: ('improving' if s >= 0 else 'declining') for u, s in slopes.items()}

    plt.figure(figsize=figsize)
    # Ensure chronological order
    df_sorted = df.sort_values(by=[date_col])

    for user, group in df_sorted.groupby(user_col):
        style = '-' if slopes.get(user, 0) >= 0 else '--'
        label = f"{user} ({status.get(user)})"
        plt.plot(
            group[date_col],
            group[score_col],
            style,
            label=label
        )

    plt.xlabel(date_col)
    plt.ylabel(score_col)
    plt.title('Comparative Wellness Score Trends')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    if out_path:
        plt.savefig(out_path, dpi=300)
    plt.show()
