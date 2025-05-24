# src/analysis.py

import pandas as pd
import numpy as np


def compute_slopes(
    df: pd.DataFrame,
    user_col: str = 'User',
    score_col: str = 'Score'
) -> dict:
    """
    Compute linear regression slope of the `score_col` over time for each user.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing at least the columns `user_col` and `score_col`, plus a date index or sorted order.
    user_col : str
        Name of the column identifying users.
    score_col : str
        Name of the column containing numeric scores.

    Returns
    -------
    dict
        Mapping from each user to their fitted trend slope (float).
    """
    slopes = {}
    # Group by user and ensure time order
    for user, group in df.groupby(user_col):
        # Sort group by date if the first column is date-like
        group = group.sort_values(by=group.columns[0])
        y = group[score_col].values
        x = np.arange(len(y))
        if len(x) < 2:
            slopes[user] = 0.0
        else:
            slopes[user] = float(np.polyfit(x, y, 1)[0])
    return slopes


def label_trends(
    slopes: dict
) -> dict:
    """
    Label each user as 'improving' (slope >= 0) or 'declining' (slope < 0).

    Parameters
    ----------
    slopes : dict
        Mapping user -> numeric slope.

    Returns
    -------
    dict
        Mapping user -> 'improving' or 'declining'.
    """
    return {
        user: ('improving' if slope >= 0 else 'declining')
        for user, slope in slopes.items()
    }

