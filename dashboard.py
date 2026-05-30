import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="F1 2024 Season Dashboard", page_icon="🏎️", layout="wide")

DB_PATH = os.path.join("data", "f1_2024.db")

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    results = pd.read_sql("SELECT * FROM race_results", conn)
    drivers = pd.read_sql("SELECT * FROM drivers", conn)
    sessions = pd.read_sql("SELECT * FROM sessions", conn)
    pits = pd.read_sql("SELECT * FROM pit_stops", conn)
    conn.close()
    results["race_date"] = pd.to_datetime(results["race_date"])
    sessions["race_date"] = pd.to_datetime(sessions["race_date"])
    return results, drivers, sessions, pits

results, drivers, sessions, pits = load_data()

# --- Header ---
st.title("🏎️ Formula 1 — 2024 Season Dashboard")
st.caption("Data sourced from OpenF1 API · Full season analysis")

st.divider()

# --- Top metrics ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Races", sessions["session_key"].nunique())
with col2:
    st.metric("Total Drivers", drivers["driver_name"].nunique())
with col3:
    total_pits = len(pits)
    st.metric("Total Pit Stops", total_pits)
with col4:
    if "pit_duration" in pits.columns and not pits["pit_duration"].dropna().empty:
        fastest_pit = pits["pit_duration"].min()
        st.metric("Fastest Pit Stop", f"{fastest_pit:.2f}s")
    else:
        st.metric("Fastest Pit Stop", "N/A")

st.divider()

# --- Wins by driver ---
st.subheader("Race wins by driver")
wins = results[results["position"] == 1]["driver_name"].value_counts().reset_index()
wins.columns = ["Driver", "Wins"]
if not wins.empty:
    fig = px.bar(wins, x="Driver", y="Wins", text="Wins", color="Driver")
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Podiums by driver ---
st.subheader("Podium finishes by driver")
podiums = results[results["position"].isin([1, 2, 3])]["driver_name"].value_counts().reset_index()
podiums.columns = ["Driver", "Podiums"]
if not podiums.empty:
    fig2 = px.bar(podiums, x="Driver", y="Podiums", text="Podiums", color="Driver")
    fig2.update_traces(textposition="outside")
    fig2.update_layout(showlegend=False, xaxis_tickangle=-30)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Wins by constructor ---
st.subheader("Race wins by constructor")
constructor_wins = results[results["position"] == 1]["team"].value_counts().reset_index()
constructor_wins.columns = ["Team", "Wins"]
if not constructor_wins.empty:
    fig3 = px.bar(constructor_wins, x="Team", y="Wins", text="Wins", color="Team")
    fig3.update_traces(textposition="outside")
    fig3.update_layout(showlegend=False, xaxis_tickangle=-30)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Pit stop analysis ---
st.subheader("Pit stop analysis")
if "pit_duration" in pits.columns and not pits["pit_duration"].dropna().empty:
    avg_pits = pits.groupby("location")["pit_duration"].mean().reset_index()
    avg_pits.columns = ["Circuit", "Avg Pit Duration (s)"]
    avg_pits = avg_pits.sort_values("Avg Pit Duration (s)")
    fig4 = px.bar(
        avg_pits, x="Circuit", y="Avg Pit Duration (s)",
        text=avg_pits["Avg Pit Duration (s)"].round(2),
        color="Avg Pit Duration (s)", color_continuous_scale="Blues"
    )
    fig4.update_traces(textposition="outside")
    fig4.update_layout(xaxis_tickangle=-30, coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- Race by race results ---
st.subheader("Race results by circuit")
circuit_list = sorted(results["location_x"].dropna().unique())
selected = st.selectbox("Select a circuit", circuit_list)
race_df = results[results["location_x"] == selected][
    ["position", "driver_name", "team", "podium", "win"]
].sort_values("position")
st.dataframe(race_df, use_container_width=True)

st.divider()

# --- Raw data expander ---
with st.expander("View raw data"):
    st.write("**Sessions**")
    st.dataframe(sessions, use_container_width=True)
    st.write("**Drivers**")
    st.dataframe(drivers, use_container_width=True)
    st.write("**All Results**")
    st.dataframe(results, use_container_width=True)
