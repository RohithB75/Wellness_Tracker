# src/data_generator.py

import numpy as np
import pandas as pd

def generate_dummy_data(
    users: list,
    start: str,
    periods: int,
    freq: str,
    base: float = 50.0,
    trends: dict = None,
    noise: float = 2.0,
    col_names: tuple = ('Date', 'User', 'Score')
) -> pd.DataFrame:
    """
    Generate dummy wellness‐score data for multiple users over time.

    Parameters
    ----------
    users : list of str
        List of user identifiers.
    start : str
        Start date string (e.g. '2025-01-01').
    periods : int
        Number of time points.
    freq : str
        Frequency string for pd.date_range (e.g. 'W', 'D').
    base : float, optional
        Base score at time zero, by default 50.0.
    trends : dict, optional
        Mapping user → per‐period score increment (can be negative), 
        by default zero trend for all.
    noise : float, optional
        Standard deviation of Gaussian noise to add, by default 2.0.
    col_names : tuple of str, optional
        Column names for (date, user, score), by default ('Date','User','Score').

    Returns
    -------
    pd.DataFrame
        DataFrame with shape (len(users)*periods, 3) and columns given by col_names.
    """
    # Default zero‐trend if none provided
    if trends is None:
        trends = {u: 0.0 for u in users}

    # Create the date index
    dates = pd.date_range(start=start, periods=periods, freq=freq)

    rows = []
    for user in users:
        slope = trends.get(user, 0.0)
        for idx, date in enumerate(dates):
            score = base + slope * idx + np.random.randn() * noise
            rows.append({
                col_names[0]: date,
                col_names[1]: user,
                col_names[2]: score
            })

    df = pd.DataFrame(rows)
    return df


def load_csv(
    path: str,
    date_column: str = 'Date'
) -> pd.DataFrame:
    """
    Load a CSV of wellness scores into a DataFrame, parsing the date column.

    Parameters
    ----------
    path : str
        Path to the CSV file.
    date_column : str, optional
        Name of the column to parse as datetime, by default 'Date'.

    Returns
    -------
    pd.DataFrame
    """
    df = pd.read_csv(path, parse_dates=[date_column])
    return df
