import pandas as pd

def transform_sessions(df):
    print("Transforming sessions...")
    df = df.copy()
    df["race_date"] = pd.to_datetime(df["race_date"])
    df["loaded_at"] = pd.Timestamp.now()
    print(f"  {len(df)} sessions ready.")
    return df

def transform_drivers(df):
    print("Transforming drivers...")
    df = df.copy()
    df = df.dropna(subset=["driver_name"])
    df["loaded_at"] = pd.Timestamp.now()
    print(f"  {len(df)} drivers ready.")
    return df

def transform_results(df, sessions_df, drivers_df):
    print("Transforming race results...")
    df = df.copy()

    # Join session info (location, date, circuit)
    df = df.merge(
        sessions_df[["session_key", "location", "race_date", "circuit", "country_name"]],
        on="session_key", how="left"
    )

    # Join driver info (name, team)
    df = df.merge(
        drivers_df[["driver_number", "driver_name", "team", "abbreviation"]],
        on="driver_number", how="left"
    )

    # Add podium and win flags
    df["podium"] = df["position"].isin([1, 2, 3])
    df["win"] = df["position"] == 1

    df["loaded_at"] = pd.Timestamp.now()
    print(f"  {len(df)} result rows ready.")
    return df

def transform_pit_stops(df):
    print("Transforming pit stops...")
    df = df.copy()
    if "pit_duration" in df.columns:
        df = df.dropna(subset=["pit_duration"])
        df["pit_duration"] = df["pit_duration"].round(3)
    df["loaded_at"] = pd.Timestamp.now()
    print(f"  {len(df)} pit stop rows ready.")
    return df
