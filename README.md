# 🏎️ F1 2024 Season ETL Pipeline & Dashboard

A fully automated data engineering pipeline that extracts real Formula 1 race data from the OpenF1 API, transforms and cleans it with pandas, stores it in a SQLite database, and visualizes it in an interactive Streamlit dashboard.

Built as a portfolio project to demonstrate end-to-end data engineering skills — from raw API data to a fully interactive dashboard.


## 📸 Dashboard Preview

> Launch the dashboard with `streamlit run dashboard.py` to see:
> - Race wins and podiums by driver
> - Constructor championship wins
> - Pit stop duration analysis by circuit
> - Race-by-race finishing results


## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Core programming language |
| pandas | Data cleaning and transformation |
| requests | API calls to OpenF1 |
| SQLite | Local database storage |
| SQLAlchemy | Database connection and ORM |
| Streamlit | Interactive dashboard |
| Plotly | Charts and visualizations |
| Git + GitHub | Version control and portfolio hosting |


## 📦 Data Source

**[OpenF1 API](https://openf1.org)** — a free, open-source API providing real-time and historical Formula 1 data. No API key or sign-up required.

Endpoints used:
- `/sessions` — all 2024 race sessions
- `/drivers` — driver information and team assignments
- `/position` — lap-by-lap position data (used to derive finishing positions)
- `/pit` — pit stop timing and duration data


## 🏗️ Project Structure

```
f1-pipeline-2024/
├── src/
│   ├── __init__.py          # Makes src a Python package
│   ├── extract.py           # Fetches data from OpenF1 API
│   ├── transform.py         # Cleans and enriches data with pandas
│   └── load.py              # Saves data to SQLite database
├── data/
│   └── f1_2024.db           # SQLite database (auto-generated, not in repo)
├── dashboard.py             # Streamlit dashboard
├── main.py                  # Runs the full ETL pipeline
├── requirements.txt         # Python dependencies
├── .gitignore               # Files excluded from Git
└── README.md                # This file
```


## ⚙️ Pipeline Architecture

```
OpenF1 API
    │
    ▼
extract.py          ← Fetches sessions, drivers, positions, pit stops
    │
    ▼
transform.py        ← Cleans nulls, joins tables, adds podium/win flags
    │
    ▼
load.py             ← Writes to SQLite (4 tables: sessions, drivers,
    │                  race_results, pit_stops)
    ▼
dashboard.py        ← Reads from SQLite, renders Streamlit charts
```


## 📊 Database Schema

**sessions** — one row per race weekend
| Column | Description |
|--------|-------------|
| session_key | Unique race identifier |
| session_name | "Race" |
| race_date | Date of the race |
| location | City/circuit location |
| country_name | Country |
| circuit | Short circuit name |

**drivers** — one row per driver
| Column | Description |
|--------|-------------|
| driver_number | Car number |
| driver_name | Full name |
| abbreviation | 3-letter code (e.g. VER) |
| team | Constructor name |
| country | Nationality code |

**race_results** — one row per driver per race
| Column | Description |
|--------|-------------|
| driver_number | Car number |
| position | Final finishing position |
| session_key | Links to sessions table |
| location_x | Race location |
| driver_name | Full name |
| team | Constructor |
| podium | True if finished 1st, 2nd, or 3rd |
| win | True if finished 1st |

**pit_stops** — one row per pit stop
| Column | Description |
|--------|-------------|
| driver_number | Car number |
| lap_number | Lap the stop occurred |
| pit_duration | Total pit lane time (seconds) |
| stop_duration | Stationary time in pit box (seconds) |
| location | Race location |


## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/TCally05/f1-pipeline-2024.git
cd f1-pipeline-2024
```

### 2. Create and activate a virtual environment
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the ETL pipeline
```bash
python main.py
```

This will:
- Extract all 24 races from the 2024 F1 season via the OpenF1 API
- Clean and transform the data
- Load it into a local SQLite database at `data/f1_2024.db`

> Note: The pipeline includes a 2-second delay between API calls to respect OpenF1's rate limits. It takes approximately 2-3 minutes to complete.

### 5. Launch the dashboard
```bash
streamlit run dashboard.py
```

Open your browser to `http://localhost:8501`


## 📋 Requirements

```
pandas
requests
sqlalchemy
streamlit
plotly
```

Install all with:
```bash
pip install -r requirements.txt
```

## 🔑 Key Concepts Demonstrated

- **ETL pipeline design** — separation of extract, transform, and load into distinct modules
- **REST API integration** — fetching paginated JSON data from a public API
- **Data cleaning** — handling nulls, type conversion, column renaming, deduplication
- **Data modeling** — normalizing raw API responses into relational tables
- **SQLite database** — creating and querying a local database with SQLAlchemy
- **Rate limit handling** — adding delays between API calls to avoid 429 errors
- **Data visualization** — building interactive charts with Plotly inside Streamlit
- **Virtual environments** — isolating project dependencies with venv
- **Version control** — managing code with Git and GitHub


## 🗺️ Roadmap

- [ ] Add AI-powered season summary using the Claude API
- [ ] Add lap time analysis using OpenF1 telemetry data
- [ ] Add qualifying vs race position comparison
- [ ] Schedule pipeline to auto-run after each race weekend
- [ ] Deploy dashboard to Streamlit Community Cloud


## 📄 License

MIT License — free to use, modify, and share.
