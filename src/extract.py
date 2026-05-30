import requests
import pandas as pd
import time

BASE_URL = "https://api.openf1.org/v1"

def get_sessions():
    """
    Fetches all 2024 race sessions (the actual race, not qualifying/practice).
    Returns a pandas DataFrame.
    """
    print("Extracting 2024 race sessions...")
    url = f"{BASE_URL}/sessions?year=2024&session_name=Race"
    response = requests.get(url)
    response.raise_for_status()

    df = pd.DataFrame(response.json())
    df = df[["session_key", "session_name", "date_start", "location", "country_name", "circuit_short_name"]].copy()
    df = df.rename(columns={"date_start": "race_date", "circuit_short_name": "circuit"})
    df["race_date"] = pd.to_datetime(df["race_date"]).dt.date

    print(f"  Extracted {len(df)} race sessions.")
    return df


def get_drivers():
    """
    Fetches all drivers who competed in the 2024 season.
    Returns a pandas DataFrame.
    """
    print("Extracting 2024 drivers...")
    url = f"{BASE_URL}/drivers?session_key=latest"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    rows = []
    seen = set()

    for d in data:
        driver_num = d.get("driver_number")
        if driver_num not in seen:
            seen.add(driver_num)
            rows.append({
                "driver_number": driver_num,
                "driver_name": d.get("full_name"),
                "abbreviation": d.get("name_acronym"),
                "team": d.get("team_name"),
                "country": d.get("country_code"),
            })

    df = pd.DataFrame(rows)
    print(f"  Extracted {len(df)} drivers.")
    return df


def get_race_results(session_key):
    """
    Fetches finishing positions for a single race session.
    Returns a pandas DataFrame.
    """
    url = f"{BASE_URL}/position?session_key={session_key}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # Keep only the final position for each driver (last recorded position)
    df = df.sort_values("date").groupby("driver_number").last().reset_index()
    df = df[["driver_number", "position"]].copy()
    df["session_key"] = session_key
    return df


def get_pit_stops(session_key):
    """
    Fetches pit stop data for a single race session.
    Returns a pandas DataFrame.
    """
    url = f"{BASE_URL}/pit?session_key={session_key}"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    df["session_key"] = session_key
    return df


def get_all_race_results(sessions_df):
    """
    Loops through all 2024 race sessions and fetches results + pit stops.
    Returns two DataFrames: all_results, all_pit_stops.
    """
    print("Extracting race results and pit stops for all 2024 races...")
    all_results = []
    all_pits = []

    for _, row in sessions_df.iterrows():
        session_key = row["session_key"]
        location = row["location"]

        results = get_race_results(session_key)
        if not results.empty:
            results["location"] = location
            all_results.append(results)

        pits = get_pit_stops(session_key)
        if not pits.empty:
            pits["location"] = location
            all_pits.append(pits)

        print(f"  Done: {location}")
        time.sleep(2)  # Sleep to avoid hitting API rate limits

    results_df = pd.concat(all_results, ignore_index=True) if all_results else pd.DataFrame()
    pits_df = pd.concat(all_pits, ignore_index=True) if all_pits else pd.DataFrame()

    print(f"  Total result rows: {len(results_df)}")
    print(f"  Total pit stop rows: {len(pits_df)}")
    return results_df, pits_df
