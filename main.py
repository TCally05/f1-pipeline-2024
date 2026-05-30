from src.extract import get_sessions, get_drivers, get_all_race_results
from src.transform import transform_sessions, transform_drivers, transform_results, transform_pit_stops
from src.load import load_table

def run_pipeline():
    print("=" * 50)
    print("  F1 2024 Season ETL Pipeline (OpenF1)")
    print("=" * 50)

    # Extract
    sessions_df = get_sessions()
    drivers_df = get_drivers()
    results_df, pits_df = get_all_race_results(sessions_df)

    # Transform
    sessions_clean = transform_sessions(sessions_df)
    drivers_clean = transform_drivers(drivers_df)
    results_clean = transform_results(results_df, sessions_clean, drivers_clean)
    pits_clean = transform_pit_stops(pits_df)

    # Load
    load_table(sessions_clean, "sessions")
    load_table(drivers_clean, "drivers")
    load_table(results_clean, "race_results")
    load_table(pits_clean, "pit_stops")

    print("=" * 50)
    print("Pipeline complete! Run: streamlit run dashboard.py")
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()
