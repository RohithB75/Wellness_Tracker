#!/usr/bin/env python3
# run_trends.py

import sys
import os

# 1. Make sure `src/` is on the import path
PROJECT_ROOT = os.path.dirname(__file__)
SRC_PATH      = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# 2. Now import your modules
from data_generator import generate_dummy_data
from Analysis       import compute_slopes, label_trends
from visualization  import plot_trends

def main():
    # 3. Generate dummy data
    df = generate_dummy_data(
        users=['User A','User B','User C','User D','User E'],
        start='2025-01-01',
        periods=10,
        freq='W',
        base=50.0,
        trends={
            'User A': 0.5,
            'User B': -0.3,
            'User C': 0.1,
            'User D': -0.1,
            'User E': 0.3
        },
        noise=2.0,
        col_names=('Date','User','Score')
    )

    # 4. Compute and label trends
    slopes = compute_slopes(df, user_col='User', score_col='Score')
    trends = label_trends(slopes)

    print("Slopes:", slopes)
    print("Labels:", trends)

    # 5. Plot (and show) the results
    plot_trends(
        df,
        slopes,
        date_col='Date',
        score_col='Score',
        user_col='User',
        status=trends,
        figsize=(10,6),
        # out_path="wellness_trends.png"  # uncomment to save instead of display
    )

if __name__ == "__main__":
    main()
