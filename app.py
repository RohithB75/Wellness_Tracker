# app.py

import streamlit as st
import pandas as pd
import json
import ast
from src.data_generator import generate_dummy_data, load_csv
from src.Analysis  import compute_slopes, label_trends

st.set_page_config(page_title="Wellness Trends Dashboard", layout="wide")
st.title("🏃 Wellness Trends Dashboard")

mode = st.sidebar.radio("Data source", ["Dummy Data", "Upload CSV"])

if mode == "Dummy Data":
    # --- Sidebar inputs for dummy data ---
    users_txt   = st.sidebar.text_input("Users (comma-sep)", "User A,User B,User C")
    start_date  = st.sidebar.date_input("Start Date", pd.to_datetime("2025-01-01"))
    periods     = st.sidebar.slider("Number of periods", 5, 52, 10)
    freq        = st.sidebar.selectbox("Frequency", ["D","W","M"])
    noise       = st.sidebar.slider("Noise level", 0.0, 10.0, 2.0)
    trends_txt  = st.sidebar.text_area(
        "Trends JSON",
        '{"User A": 0.5, "User B": -0.3}'
    )

    # —— JSON load block ——    
    try:
        # strict JSON
        trends = json.loads(trends_txt)
    except json.JSONDecodeError:
        # fallback to Python dict syntax
        try:
            trends = ast.literal_eval(trends_txt)
        except Exception:
            st.error("Invalid JSON or Python dict for trends")
            st.stop()
    # — end JSON load block —

    users = [u.strip() for u in users_txt.split(",") if u.strip()]
    df = generate_dummy_data(
        users=users,
        start=start_date.strftime("%Y-%m-%d"),
        periods=periods,
        freq=freq,
        base=50.0,
        trends=trends,
        noise=noise,
        col_names=("Date","User","Score")
    )

else:
    upload = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if not upload:
        st.info("Upload a CSV with columns Date,User,Score")
        st.stop()
    df = load_csv(upload)

# Show data
st.subheader("Data Preview")
st.dataframe(df)

# Compute & label trends
slopes = compute_slopes(df, user_col="User", score_col="Score")
labels = label_trends(slopes)

# Summary table
summary = pd.DataFrame({
    "User": list(slopes.keys()),
    "Slope": list(slopes.values()),
    "Trend": [labels[u] for u in slopes],
})
st.subheader("Trend Summary")
st.table(summary)

# Plot inline
st.subheader("Trend Plot")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10,5))
for user, grp in df.sort_values("Date").groupby("User"):
    style = "-" if slopes[user] >= 0 else "--"
    ax.plot(grp["Date"], grp["Score"], style, label=f"{user} ({labels[user]})")
ax.set_xlabel("Date")
ax.set_ylabel("Wellness Score")
ax.set_title("Comparative Wellness Score Trends")
ax.legend()
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)
