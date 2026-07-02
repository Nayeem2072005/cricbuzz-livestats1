 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=for-the-badge&logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue?style=for-the-badge&logo=postgresql)
![RapidAPI](https://img.shields.io/badge/RapidAPI-Cricbuzz-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-green?style=for-the-badge)

**GUVI × HCL Capstone Project | Domain: Sports Analytics**

</div>

---

## 📌 Project Overview

**Cricbuzz LiveStats** is a comprehensive cricket analytics dashboard that integrates live data from the **Cricbuzz API** (via RapidAPI) with a **PostgreSQL** database to deliver:

- ⚡ Real-time match scores and scorecards
- 📊 Live batting & bowling leaderboards
- 🧮 25 SQL-driven analytics queries (Beginner → Advanced)
- ✏️ Full CRUD operations on player statistics

---

## 🗂️ Project Structure

```
cricbuzz_livestats/
├── app.py                        # 🏠 Home page — Streamlit entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
│
├── pages/
│   ├── live_matches.py           # 🔴 Live & recent match scorecards
│   ├── top_stats.py              # 📊 Batting/bowling leaderboards
│   ├── sql_queries.py            # 🧮 25 SQL analytics queries
│   └── crud_operations.py        # ✏️ Create / Read / Update / Delete
│
├── utils/
│   └── db_connection.py          # PostgreSQL connection handler
│
└── notebooks/
    └── data_fetching.ipynb       # Jupyter notebook — API extraction + all 25 queries
```

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cricbuzz-livestats.git
cd cricbuzz-livestats/cricbuzz_livestats
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. PostgreSQL Setup

Open **pgAdmin** and run:

```sql
CREATE DATABASE cricbuzz_final;
```

Then connect to `cricbuzz_final` and run the full schema:

```sql
CREATE TABLE teams (
    team_id   SERIAL PRIMARY KEY,
    team_name VARCHAR(100),
    country   VARCHAR(100)
);

CREATE TABLE players (
    player_id     SERIAL PRIMARY KEY,
    full_name     VARCHAR(150),
    team_id       INT REFERENCES teams(team_id),
    playing_role  VARCHAR(80),
    batting_style VARCHAR(80),
    bowling_style VARCHAR(80)
);

CREATE TABLE venues (
    venue_id   SERIAL PRIMARY KEY,
    venue_name VARCHAR(150),
    city       VARCHAR(100),
    country    VARCHAR(100),
    capacity   INT
);

CREATE TABLE matches (
    match_id       SERIAL PRIMARY KEY,
    match_desc     VARCHAR(200),
    team1_id       INT REFERENCES teams(team_id),
    team2_id       INT REFERENCES teams(team_id),
    venue_id       INT REFERENCES venues(venue_id),
    match_date     DATE,
    status         VARCHAR(50),
    winner_team_id INT REFERENCES teams(team_id),
    victory_margin VARCHAR(20),
    victory_type   VARCHAR(20),
    toss_winner_id INT REFERENCES teams(team_id),
    toss_decision  VARCHAR(10)
);

CREATE TABLE series (
    series_id     SERIAL PRIMARY KEY,
    series_name   VARCHAR(200),
    host_country  VARCHAR(100),
    match_type    VARCHAR(20),
    start_date    DATE,
    total_matches INT
);

CREATE TABLE batting_stats (
    player_name VARCHAR(100),
    format      VARCHAR(20),
    matches     INT,
    innings     INT,
    runs        INT,
    average     FLOAT,
    strike_rate FLOAT,
    centuries   INT,
    PRIMARY KEY (player_name, format)
);

CREATE TABLE bowling_stats (
    stat_id         SERIAL PRIMARY KEY,
    player_id       INT REFERENCES players(player_id),
    format          VARCHAR(20),
    matches         INT,
    wickets         INT,
    bowling_average FLOAT,
    economy_rate    FLOAT
);

CREATE TABLE batting_innings (
    innings_id       SERIAL PRIMARY KEY,
    match_id         INT REFERENCES matches(match_id),
    player_id        INT REFERENCES players(player_id),
    team_id          INT REFERENCES teams(team_id),
    innings_number   INT,
    batting_position INT,
    runs_scored      INT,
    balls_faced      INT,
    strike_rate      FLOAT
);

CREATE TABLE bowling_innings (
    innings_id    SERIAL PRIMARY KEY,
    match_id      INT REFERENCES matches(match_id),
    player_id     INT REFERENCES players(player_id),
    format        VARCHAR(20),
    overs         FLOAT,
    wickets       INT,
    runs_conceded INT,
    balls_bowled  INT,
    economy_rate  FLOAT
);

CREATE TABLE battingstats (
    player_name VARCHAR(100),
    format      VARCHAR(20),
    matches     INT,
    innings     INT,
    runs        INT,
    average     FLOAT,
    PRIMARY KEY (player_name, format)
);
```

### 4. Configure Credentials

Update `utils/db_connection.py`:

```python
DB_CONFIG = {
    "host":     "localhost",
    "database": "cricbuzz_final",
    "user":     "postgres",
    "password": "your_password_here",
    "port":     "5432"
}
```

Update `pages/live_matches.py` and `pages/top_stats.py`:

```python
RAPIDAPI_KEY = "your_rapidapi_key_here"
```

> Get your free API key at [rapidapi.com](https://rapidapi.com) → search **Cricbuzz Cricket** → Subscribe

### 5. Run the Notebook

Open `notebooks/data_fetching.ipynb` in VS Code → Select Python kernel → **Run All**

This populates the `battingstats` table from the API.

### 6. Launch the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🚀

---

## 📱 App Pages

| Page | Description |
|------|-------------|
| 🏠 **Home** | Project overview, tech stack, navigation guide |
| 🔴 **Live Matches** | Real-time scores and scorecards from Cricbuzz API |
| 📊 **Top Stats** | Batting & bowling leaderboards with bar charts |
| 🧮 **SQL Queries** | 25 analytics queries — run them directly in the app |
| ✏️ **CRUD Operations** | Add, view, update, delete player records |

---

## 🧮 SQL Practice Questions — 25 Queries

### 🟢 Beginner (Q1–Q8)
| # | Query |
|---|-------|
| Q1 | Find all players who represent India |
| Q2 | Recent matches with venue details |
| Q3 | Top 10 ODI run scorers |
| Q4 | Venues with capacity > 25,000 |
| Q5 | Team win count |
| Q6 | Players per playing role |
| Q7 | Highest score by format |
| Q8 | Series starting in 2024 |

### 🟡 Intermediate (Q9–Q16)
| # | Query |
|---|-------|
| Q9 | All-rounders with 1000+ runs & 50+ wickets |
| Q10 | Last 20 completed matches with results |
| Q11 | Player performance across formats |
| Q12 | Home vs Away win analysis |
| Q13 | Century batting partnerships |
| Q14 | Bowler economy at venues |
| Q15 | Players excelling in close matches |
| Q16 | Yearly batting performance since 2020 |

### 🔴 Advanced (Q17–Q25)
| # | Query |
|---|-------|
| Q17 | Toss advantage analysis |
| Q18 | Most economical bowlers (ODI + T20I) |
| Q19 | Most consistent batsmen (lowest std deviation) |
| Q20 | Format-wise match count and batting averages |
| Q21 | Comprehensive performance ranking system |
| Q22 | Head-to-head match prediction analysis |
| Q23 | Recent player form categorization |
| Q24 | Best batting partnerships |
| Q25 | Time-series career trajectory analysis |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Core programming language |
| Streamlit | Interactive web dashboard |
| PostgreSQL | Relational database |
| psycopg2 | PostgreSQL connector |
| requests | REST API calls |
| pandas | Data manipulation |
| Cricbuzz RapidAPI | Live cricket data source |

---

## 📒 Notebook Highlights

The `notebooks/data_fetching.ipynb` contains **71 cells** covering:

- ✅ Step-by-step API extraction from Cricbuzz RapidAPI
- ✅ JSON parsing — `data.keys()`, `data['values']`, row indexing
- ✅ PostgreSQL connection and table creation
- ✅ `insert_format()` function for all 3 formats (Test, ODI, T20I)
- ✅ All 25 SQL queries with sample output

---

## 💼 Business Use Cases

- 📺 **Sports Media** — Real-time commentary support and pre-match analysis
- 🎮 **Fantasy Cricket** — Player form tracking and team selection insights
- 📈 **Analytics Firms** — Statistical modeling and performance trends
- 🎓 **Education** — SQL practice with real-world cricket datasets

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit home page |
| `utils/db_connection.py` | DB connection + `run_query()` / `run_write()` helpers |
| `pages/live_matches.py` | Live API integration |
| `pages/sql_queries.py` | All 25 SQL queries with run buttons |
| `notebooks/data_fetching.ipynb` | Complete data pipeline notebook |

---

## 🙏 Acknowledgements

- **GUVI × HCL** — Capstone project framework
- **Cricbuzz API** via RapidAPI — Live cricket data
- **Streamlit** — Web app framework

---

<div align="center">

</div>
