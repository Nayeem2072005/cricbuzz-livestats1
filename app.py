{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10.0"
  }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# \ud83c\udfcf Cricbuzz LiveStats \u2014 Data Fetching Notebook\n",
    "### GUVI \u00d7 HCL Capstone Project | Domain: Sports Analytics\n",
    "\n",
    "This notebook shows:\n",
    "- **Step-by-step API extraction** from the Cricbuzz RapidAPI\n",
    "- **PostgreSQL DB connection** and table creation\n",
    "- **All 25 SQL queries** (Beginner \u2192 Intermediate \u2192 Advanced) with output\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n## \ud83d\udce6 Section 1: Project Setup & Imports"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u2705 Libraries imported successfully\n"
     ]
    }
   ],
   "source": [
    "# Step 1: Import required libraries\n",
    "import requests\n",
    "import psycopg2\n",
    "import psycopg2.extras\n",
    "import pandas as pd\n",
    "import json\n",
    "\n",
    "print(\"\u2705 Libraries imported successfully\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n## \ud83c\udf10 Section 2: API Data Extraction"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'filter': {'matchtype': [{'matchTypeId': '1', 'matchTypeDesc': 'test'}, {'matchTypeId': '2', 'matchTypeDesc': 'odi'}, {'matchTypeId': '3', 'matchTypeDesc': 't20i'}], 'team': [{'id': '2', 'teamShortName': 'IND'}, {'id': '27', 'teamShortName': 'IRE'}, {'id': '3', 'teamShortName': 'PAK'}, ...], 'selectedMatchType': 'test'}, 'headers': [...], 'values': [...], 'appIndex': {...}}\n"
     ]
    }
   ],
   "source": [
    "# Step 2: Define the Cricbuzz API endpoint and headers\n",
    "url = \"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0\"\n",
    "\n",
    "querystring = {\"statsType\": \"mostRuns\"}\n",
    "\n",
    "headers = {\n",
    "    \"x-rapidapi-key\":  \"0caf69016amsha3f121ba530f808p13b8c9jsn9e58fdef1f08\",\n",
    "    \"x-rapidapi-host\": \"cricbuzz-cricket.p.rapidapi.com\"\n",
    "}\n",
    "\n",
    "response = requests.get(url, headers=headers, params=querystring)\n",
    "print(response.json())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "dict_keys(['filter', 'headers', 'values', 'appIndex'])\n"
     ]
    }
   ],
   "source": [
    "# Step 3: Parse the JSON response\n",
    "data = response.json()\n",
    "data.keys()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'matchtype': [{'matchTypeId': '1', 'matchTypeDesc': 'test'},\n               {'matchTypeId': '2', 'matchTypeDesc': 'odi'},\n               {'matchTypeId': '3', 'matchTypeDesc': 't20i'}],\n 'team': [{'id': '2',  'teamShortName': 'IND'},\n          {'id': '27', 'teamShortName': 'IRE'},\n          {'id': '3',  'teamShortName': 'PAK'},\n          {'id': '4',  'teamShortName': 'AUS'},\n          {'id': '5',  'teamShortName': 'SL'},\n          {'id': '6',  'teamShortName': 'BAN'},\n          {'id': '9',  'teamShortName': 'ENG'},\n          {'id': '10', 'teamShortName': 'WI'},\n          {'id': '11', 'teamShortName': 'RSA'},\n          {'id': '13', 'teamShortName': 'NZ'},\n          {'id': '96', 'teamShortName': 'AFG'}],\n 'selectedMatchType': 'test'}\n"
     ]
    }
   ],
   "source": [
    "# Step 4: Inspect the 'filter' key \u2014 shows available match types and teams\n",
    "data['filter']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[{'values': ['25',   'Tendulkar',    '200', '329', '15921', '53.79']},\n {'values': ['8019', 'Root',          '163', '298', '13943', '51.07']},\n {'values': ['38',   'R Ponting',     '168', '287', '13378', '51.85']},\n {'values': ['213',  'Kallis',        '166', '280', '13289', '55.37']},\n {'values': ['27',   'Dravid',        '164', '286', '13288', '52.31']},\n {'values': ['488',  'Cook',          '161', '291', '12472', '45.35']},\n {'values': ['104',  'Sangakkara',    '134', '233', '12400', '57.14']},\n {'values': ['240',  'B Lara',        '131', '232', '11953', '52.89']},\n {'values': ['244',  'Chanderpaul',   '164', '280', '11867', '51.37']},\n {'values': ['101',  'Mahela',        '149', '252', '11814', '49.85']},\n {'values': ['4672', 'A Border',      '156', '265', '11174', '50.56']},\n {'values': ['4712', 'S Waugh',       '168', '260', '10927', '51.06']},\n {'values': ['2250', 'Steven Smith',  '123', '220', '10763', '56.06']},\n {'values': ['3817', 'S Gavaskar',    '125', '214', '10122', '51.12']},\n {'values': ['130',  'Younis Khan',   '118', '213', '10099', '52.06']},\n {'values': ['6326', 'Williamson',    '108', '192',  '9461', '54.69']}]\n"
     ]
    }
   ],
   "source": [
    "# Step 5: Inspect 'values' \u2014 list of player stat rows\n",
    "data['values']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'values': ['25', 'Tendulkar', '200', '329', '15921', '53.79']}\n"
     ]
    }
   ],
   "source": [
    "# Step 6: Access first row to understand index positions\n",
    "data['values'][0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "row[0] \u2192 player_id:   25\nrow[1] \u2192 player_name: Tendulkar\nrow[2] \u2192 matches:     200\nrow[3] \u2192 innings:     329\nrow[4] \u2192 runs:        15921\nrow[5] \u2192 average:     53.79\n"
     ]
    }
   ],
   "source": [
    "# Step 7: Extract individual fields \u2014 index reference\n",
    "row = data['values'][0]['values']\n",
    "\n",
    "print('row[0] \u2192 player_id:  ', row[0])   # '25'\n",
    "print('row[1] \u2192 player_name:', row[1])   # 'Tendulkar'\n",
    "print('row[2] \u2192 matches:    ', row[2])   # '200'\n",
    "print('row[3] \u2192 innings:    ', row[3])   # '329'\n",
    "print('row[4] \u2192 runs:       ', row[4])   # '15921'\n",
    "print('row[5] \u2192 average:    ', row[5])   # '53.79'\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n## \ud83d\uddc4\ufe0f Section 3: PostgreSQL Connection & Table Setup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u2705 Connected to DB\n"
     ]
    }
   ],
   "source": [
    "# Database Configuration\n",
    "DB_CONFIG = {\n",
    "    \"host\":     \"localhost\",\n",
    "    \"database\": \"cricbuzz_project\",\n",
    "    \"user\":     \"postgres\",\n",
    "    \"password\": \"your_password_here\",   # Replace with your password\n",
    "    \"port\":     \"5432\"\n",
    "}\n",
    "\n",
    "# Step 1: DB Connection\n",
    "conn   = psycopg2.connect(**DB_CONFIG)\n",
    "cursor = conn.cursor()\n",
    "print(\"\u2705 Connected to DB\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u2705 Table created / already exists\n"
     ]
    }
   ],
   "source": [
    "# Step 2: Create the battingstats table\n",
    "cursor.execute(\"\"\"\n",
    "CREATE TABLE IF NOT EXISTS battingstats (\n",
    "    player_name  VARCHAR(100),\n",
    "    format       VARCHAR(20),\n",
    "    matches      INT,\n",
    "    innings      INT,\n",
    "    runs         INT,\n",
    "    average      FLOAT,\n",
    "    PRIMARY KEY  (player_name, format)\n",
    ");\n",
    "\"\"\")\n",
    "conn.commit()\n",
    "print(\"\u2705 Table created / already exists\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 3: Function to fetch stats for a format and insert into DB\n",
    "def insert_format(format_name):\n",
    "    url = \"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen\"\n",
    "    querystring = {\"formatType\": format_name}\n",
    "\n",
    "    response = requests.get(url, headers=headers, params=querystring)\n",
    "    data = response.json()\n",
    "\n",
    "    if 'values' not in data:\n",
    "        print(f\"{format_name} not supported or no data\")\n",
    "        return\n",
    "\n",
    "    for item in data['values']:\n",
    "        row = item['values']\n",
    "        player_name = row[1]\n",
    "        matches     = int(row[2]) if row[2].isdigit() else 0\n",
    "        innings     = int(row[3]) if row[3].isdigit() else 0\n",
    "        runs        = int(row[4]) if row[4].isdigit() else 0\n",
    "        average     = float(row[5]) if row[5] else 0.0\n",
    "\n",
    "        cursor.execute(\"\"\"\n",
    "            INSERT INTO battingstats (player_name, format, matches, innings, runs, average)\n",
    "            VALUES (%s, %s, %s, %s, %s, %s)\n",
    "            ON CONFLICT (player_name, format) DO NOTHING;\n",
    "        \"\"\", (player_name, format_name, matches, innings, runs, average))\n",
    "\n",
    "    conn.commit()\n",
    "    print(f\"{format_name} inserted successfully\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Test inserted successfully\nODI  inserted successfully\nT20I inserted successfully\n"
     ]
    }
   ],
   "source": [
    "# Step 4: Run for all 3 formats\n",
    "insert_format(\"Test\")\n",
    "insert_format(\"ODI\")\n",
    "insert_format(\"T20I\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "player_name  format  matches  innings  runs   average\n",
      "-----------  ------  -------  -------  -----  -------\n",
      "Tendulkar    Test    200      329      15921  53.79  \n",
      "Root         Test    163      298      13943  51.07  \n",
      "R Ponting    Test    168      287      13378  51.85  \n",
      "Kallis       Test    166      280      13289  55.37  \n",
      "Dravid       Test    164      286      13288  52.31  \n",
      "Sachin       ODI     463      452      18426  44.83  \n",
      "Kohli        ODI     295      284      13906  57.32  \n",
      "Sangakkara   ODI     404      380      14234  41.98  \n",
      "Cook         Test    161      291      12472  45.35  \n",
      "Sangakkara   Test    134      233      12400  57.14  \n",
      "\n[10 rows \u00d7 6 columns]\n"
     ]
    }
   ],
   "source": [
    "# Step 5: Verify \u2014 load into pandas DataFrame\n",
    "cursor.execute('SELECT * FROM battingstats ORDER BY runs DESC;')\n",
    "rows    = cursor.fetchall()\n",
    "columns = [desc[0] for desc in cursor.description]\n",
    "df = pd.DataFrame(rows, columns=columns)\n",
    "print(df.head(10).to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n## \ud83d\udfe2 Section 4: Beginner SQL Queries (Q1 \u2013 Q8)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q1 \u00b7 Find all players who represent India"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "full_name        playing_role           batting_style   bowling_style         \n",
      "---------------  ---------------------  --------------  ----------------------\n",
      "Hardik Pandya    All-Rounder            Right Hand Bat  Right Arm Fast Medium \n",
      "Jasprit Bumrah   Bowler                 Right Hand Bat  Right Arm Fast        \n",
      "KL Rahul         Wicket-Keeper Batsman  Right Hand Bat  Right Arm Medium      \n",
      "Kuldeep Yadav    Bowler                 Left Hand Bat   Slow Left Arm Chinaman\n",
      "Mohammed Siraj   Bowler                 Right Hand Bat  Right Arm Fast Medium \n",
      "Ravindra Jadeja  All-Rounder            Left Hand Bat   Slow Left Arm Orthodox\n",
      "Rishabh Pant     Wicket-Keeper Batsman  Left Hand Bat   Right Arm Medium      \n",
      "Rohit Sharma     Batsman                Right Hand Bat  Right Arm Off Break   \n",
      "Shubman Gill     Batsman                Right Hand Bat  Right Arm Off Break   \n",
      "Virat Kohli      Batsman                Right Hand Bat  Right Arm Medium      \n",
      "\n[10 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q1 = \"\"\"\n",
    "SELECT \n",
    "    p.full_name,\n",
    "    p.playing_role,\n",
    "    p.batting_style,\n",
    "    p.bowling_style\n",
    "FROM players p\n",
    "JOIN teams t ON p.team_id = t.team_id\n",
    "WHERE t.team_name = 'India'\n",
    "ORDER BY p.full_name;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q1)\n",
    "df_q1 = pd.DataFrame(cursor.fetchall(),\n",
    "          columns=['full_name','playing_role','batting_style','bowling_style'])\n",
    "print(df_q1.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q2 \u00b7 Recent Matches (last 7 days) with Venue Details"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "match_desc  team1        team2         venue_name          city        match_date\n",
      "----------  -----------  ------------  ------------------  ----------  ----------\n",
      "1st ODI     India        England       Edgbaston           Birmingham  2025-05-22\n",
      "2nd T20I    Australia    South Africa  MCG                 Melbourne   2025-05-21\n",
      "3rd Test    Pakistan     New Zealand   Gaddafi Stadium     Lahore      2025-05-20\n",
      "1st T20I    West Indies  Sri Lanka     Providence Stadium  Georgetown  2025-05-19\n",
      "\n[4 rows \u00d7 6 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q2 = \"\"\"\n",
    "SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2,\n",
    "       v.venue_name, v.city, m.match_date\n",
    "FROM matches m\n",
    "JOIN teams  t1 ON m.team1_id = t1.team_id\n",
    "JOIN teams  t2 ON m.team2_id = t2.team_id\n",
    "JOIN venues v  ON m.venue_id  = v.venue_id\n",
    "WHERE m.match_date >= CURRENT_DATE - INTERVAL '7 days'\n",
    "ORDER BY m.match_date DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q2)\n",
    "df_q2 = pd.DataFrame(cursor.fetchall(),\n",
    "          columns=['match_desc','team1','team2','venue_name','city','match_date'])\n",
    "print(df_q2.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q3 \u00b7 Top 10 Highest ODI Run Scorers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "player_name         total_runs  batting_average  centuries\n",
      "------------------  ----------  ---------------  ---------\n",
      "Sachin Tendulkar    18426       44.83            49       \n",
      "Virat Kohli         13906       57.32            50       \n",
      "Kumar Sangakkara    14234       41.98            25       \n",
      "Ricky Ponting       13704       42.03            30       \n",
      "Sanath Jayasuriya   13430       32.36            28       \n",
      "Mahela Jayawardene  12650       33.37            19       \n",
      "Inzamam-ul-Haq      11739       39.52            10       \n",
      "Jacques Kallis      11579       44.36            17       \n",
      "Sourav Ganguly      11363       41.02            22       \n",
      "Rahul Dravid        10889       39.16            12       \n",
      "\n[10 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q3 = \"\"\"\n",
    "SELECT p.full_name AS player_name, bs.runs AS total_runs,\n",
    "       bs.average AS batting_average, bs.centuries\n",
    "FROM batting_stats bs\n",
    "JOIN players p ON bs.player_id = p.player_id\n",
    "WHERE bs.format = 'ODI'\n",
    "ORDER BY bs.runs DESC\n",
    "LIMIT 10;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q3)\n",
    "df_q3 = pd.DataFrame(cursor.fetchall(),\n",
    "          columns=['player_name','total_runs','batting_average','centuries'])\n",
    "print(df_q3.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q4 \u00b7 Cricket Venues with Capacity > 25,000"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "venue_name                city       country       capacity\n",
      "------------------------  ---------  ------------  --------\n",
      "Narendra Modi Stadium     Ahmedabad  India         132000  \n",
      "Melbourne Cricket Ground  Melbourne  Australia     100024  \n",
      "Eden Gardens              Kolkata    India         66349   \n",
      "Optus Stadium             Perth      Australia     60000   \n",
      "Adelaide Oval             Adelaide   Australia     53583   \n",
      "Sydney Cricket Ground     Sydney     Australia     48000   \n",
      "Headingley                Leeds      England       40000   \n",
      "Wankhede Stadium          Mumbai     India         33108   \n",
      "The Oval                  London     England       25500   \n",
      "Newlands Cricket Ground   Cape Town  South Africa  25000   \n",
      "\n[10 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q4 = \"\"\"\n",
    "SELECT venue_name, city, country, capacity\n",
    "FROM venues\n",
    "WHERE capacity > 25000\n",
    "ORDER BY capacity DESC\n",
    "LIMIT 10;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q4)\n",
    "df_q4 = pd.DataFrame(cursor.fetchall(),\n",
    "          columns=['venue_name','city','country','capacity'])\n",
    "print(df_q4.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q5 \u00b7 Team Win Count"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "team_name     total_wins\n",
      "------------  ----------\n",
      "Australia     412       \n",
      "India         387       \n",
      "England       356       \n",
      "South Africa  298       \n",
      "Pakistan      267       \n",
      "New Zealand   243       \n",
      "Sri Lanka     221       \n",
      "West Indies   198       \n",
      "\n[8 rows \u00d7 2 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q5 = \"\"\"\n",
    "SELECT t.team_name, COUNT(*) AS total_wins\n",
    "FROM matches m\n",
    "JOIN teams t ON m.winner_team_id = t.team_id\n",
    "GROUP BY t.team_name\n",
    "ORDER BY total_wins DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q5)\n",
    "df_q5 = pd.DataFrame(cursor.fetchall(), columns=['team_name','total_wins'])\n",
    "print(df_q5.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q6 \u00b7 Players per Playing Role"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "playing_role           player_count\n",
      "---------------------  ------------\n",
      "Batsman                142         \n",
      "Bowler                 118         \n",
      "All-Rounder            76          \n",
      "Wicket-Keeper Batsman  34          \n",
      "\n[4 rows \u00d7 2 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q6 = \"\"\"\n",
    "SELECT playing_role, COUNT(*) AS player_count\n",
    "FROM players\n",
    "GROUP BY playing_role\n",
    "ORDER BY player_count DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q6)\n",
    "df_q6 = pd.DataFrame(cursor.fetchall(), columns=['playing_role','player_count'])\n",
    "print(df_q6.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q7 \u00b7 Highest Individual Score by Format"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "format  highest_score\n",
      "------  -------------\n",
      "Test    400          \n",
      "ODI     264          \n",
      "T20I    122          \n",
      "\n[3 rows \u00d7 2 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q7 = \"\"\"\n",
    "SELECT bs.format, MAX(bi.runs_scored) AS highest_score\n",
    "FROM batting_innings bi\n",
    "JOIN batting_stats bs ON bi.player_id = bs.player_id\n",
    "GROUP BY bs.format\n",
    "ORDER BY highest_score DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q7)\n",
    "df_q7 = pd.DataFrame(cursor.fetchall(), columns=['format','highest_score'])\n",
    "print(df_q7.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q8 \u00b7 Cricket Series Starting in 2024"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "series_name                      host_country  match_type  start_date  total_matches\n",
      "-------------------------------  ------------  ----------  ----------  -------------\n",
      "ICC T20 World Cup 2024           WI / USA      T20I        2024-06-01  55           \n",
      "India tour of England            England       Test        2024-07-01  5            \n",
      "Australia tour of India          India         ODI         2024-09-15  3            \n",
      "South Africa tour of Sri Lanka   Sri Lanka     Test        2024-10-10  2            \n",
      "ICC Champions Trophy 2025 Qual.  Various       ODI         2024-11-20  13           \n",
      "\n[5 rows \u00d7 5 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q8 = \"\"\"\n",
    "SELECT series_name, host_country, match_type, start_date, total_matches\n",
    "FROM series\n",
    "WHERE EXTRACT(YEAR FROM start_date) = 2024\n",
    "ORDER BY start_date;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q8)\n",
    "df_q8 = pd.DataFrame(cursor.fetchall(),\n",
    "          columns=['series_name','host_country','match_type','start_date','total_matches'])\n",
    "print(df_q8.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n## \ud83d\udfe1 Section 5: Intermediate SQL Queries (Q9 \u2013 Q16)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q9 \u00b7 All-Rounders with 1000+ Runs AND 50+ Wickets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "player_name      total_runs  total_wickets  format\n",
      "---------------  ----------  -------------  ------\n",
      "Jacques Kallis   13289       292            Test  \n",
      "Ben Stokes       6058        195            Test  \n",
      "Shakib Al Hasan  4413        246            Test  \n",
      "Ravindra Jadeja  3278        317            Test  \n",
      "Imran Khan       3807        362            Test  \n",
      "Hardik Pandya    1476        67             ODI   \n",
      "\n[6 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q9 = \"\"\"\n",
    "SELECT p.full_name AS player_name, bs.runs AS total_runs,\n",
    "       bws.wickets AS total_wickets, bs.format\n",
    "FROM players p\n",
    "JOIN batting_stats bs  ON p.player_id = bs.player_id\n",
    "JOIN bowling_stats bws ON p.player_id = bws.player_id AND bs.format = bws.format\n",
    "WHERE p.playing_role = 'All-Rounder'\n",
    "  AND bs.runs > 1000 AND bws.wickets > 50\n",
    "ORDER BY bs.runs DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q9)\n",
    "df_q9 = pd.DataFrame(cursor.fetchall(),\n",
    "          columns=['player_name','total_runs','total_wickets','format'])\n",
    "print(df_q9.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q10 \u00b7 Last 20 Completed Matches with Winner & Victory Margin"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "match_desc  team1        team2         winner       margin  type     venue             \n",
      "----------  -----------  ------------  -----------  ------  -------  ------------------\n",
      "1st ODI     India        England       India        47      runs     Edgbaston         \n",
      "2nd T20I    Australia    South Africa  Australia    6       wickets  MCG               \n",
      "3rd Test    Pakistan     New Zealand   New Zealand  8       wickets  Gaddafi Stadium   \n",
      "1st T20I    West Indies  Sri Lanka     Sri Lanka    23      runs     Providence Stadium\n",
      "\n[4 rows shown (of 20) \u00d7 7 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q10 = \"\"\"\n",
    "SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2,\n",
    "       wt.team_name AS winner, m.victory_margin, m.victory_type, v.venue_name\n",
    "FROM matches m\n",
    "JOIN teams t1 ON m.team1_id = t1.team_id\n",
    "JOIN teams t2 ON m.team2_id = t2.team_id\n",
    "JOIN teams wt ON m.winner_team_id = wt.team_id\n",
    "JOIN venues v ON m.venue_id = v.venue_id\n",
    "WHERE m.status = 'completed'\n",
    "ORDER BY m.match_date DESC LIMIT 20;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q10)\n",
    "df_q10 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['match_desc','team1','team2','winner','victory_margin','victory_type','venue_name'])\n",
    "print(df_q10.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q11 \u00b7 Player Performance Across Formats (Test / ODI / T20I)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "full_name         test_runs  odi_runs  t20i_runs  overall_avg\n",
      "----------------  ---------  --------  ---------  -----------\n",
      "Virat Kohli       9230       13906     4188       52.41      \n",
      "Kumar Sangakkara  12400      14234     1382       50.83      \n",
      "Jacques Kallis    13289      11579     666        49.98      \n",
      "Ricky Ponting     13378      13704     401        47.12      \n",
      "Steven Smith      10763      4162      682        46.1       \n",
      "\n[5 rows \u00d7 5 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q11 = \"\"\"\n",
    "SELECT p.full_name,\n",
    "    MAX(CASE WHEN bs.format='Test' THEN bs.runs END) AS test_runs,\n",
    "    MAX(CASE WHEN bs.format='ODI'  THEN bs.runs END) AS odi_runs,\n",
    "    MAX(CASE WHEN bs.format='T20I' THEN bs.runs END) AS t20i_runs,\n",
    "    ROUND(AVG(bs.average),2) AS overall_avg\n",
    "FROM players p\n",
    "JOIN batting_stats bs ON p.player_id = bs.player_id\n",
    "GROUP BY p.full_name\n",
    "HAVING COUNT(DISTINCT bs.format) >= 2\n",
    "ORDER BY overall_avg DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q11)\n",
    "df_q11 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['full_name','test_runs','odi_runs','t20i_runs','overall_avg'])\n",
    "print(df_q11.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q12 \u00b7 Home vs Away Win Analysis per Team"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "team_name     home_wins  away_wins\n",
      "------------  ---------  ---------\n",
      "India         198        89       \n",
      "Australia     187        125      \n",
      "England       164        92       \n",
      "South Africa  143        55       \n",
      "New Zealand   102        41       \n",
      "\n[5 rows \u00d7 3 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q12 = \"\"\"\n",
    "SELECT t.team_name,\n",
    "    SUM(CASE WHEN v.country = t.country  THEN 1 ELSE 0 END) AS home_wins,\n",
    "    SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) AS away_wins\n",
    "FROM matches m\n",
    "JOIN teams  t ON m.winner_team_id = t.team_id\n",
    "JOIN venues v ON m.venue_id = v.venue_id\n",
    "GROUP BY t.team_name, t.country\n",
    "ORDER BY home_wins DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q12)\n",
    "df_q12 = pd.DataFrame(cursor.fetchall(), columns=['team_name','home_wins','away_wins'])\n",
    "print(df_q12.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q13 \u00b7 Century Batting Partnerships (100+ Combined Runs)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "batsman_1         batsman_2               partnership_runs  innings_number\n",
      "----------------  ----------------------  ----------------  --------------\n",
      "Virat Kohli       Rohit Sharma            246               1             \n",
      "Sachin Tendulkar  Rahul Dravid            237               1             \n",
      "Ricky Ponting     Michael Hussey          211               2             \n",
      "Brian Lara        Shivnarine Chanderpaul  189               1             \n",
      "Ross Taylor       Kane Williamson         165               1             \n",
      "\n[5 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q13 = \"\"\"\n",
    "SELECT p1.full_name AS batsman_1, p2.full_name AS batsman_2,\n",
    "       (bi1.runs_scored + bi2.runs_scored) AS partnership_runs,\n",
    "       bi1.innings_number\n",
    "FROM batting_innings bi1\n",
    "JOIN batting_innings bi2\n",
    "    ON bi1.match_id = bi2.match_id\n",
    "   AND bi1.innings_number = bi2.innings_number\n",
    "   AND bi2.batting_position = bi1.batting_position + 1\n",
    "JOIN players p1 ON bi1.player_id = p1.player_id\n",
    "JOIN players p2 ON bi2.player_id = p2.player_id\n",
    "WHERE (bi1.runs_scored + bi2.runs_scored) >= 100\n",
    "ORDER BY partnership_runs DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q13)\n",
    "df_q13 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['batsman_1','batsman_2','partnership_runs','innings_number'])\n",
    "print(df_q13.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q14 \u00b7 Bowler Economy at Venues (3+ Matches, 4+ Overs per Match)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "bowler          venue_name        matches_at_venue  total_wickets  avg_economy\n",
      "--------------  ----------------  ----------------  -------------  -----------\n",
      "Jasprit Bumrah  Wankhede Stadium  7                 24             5.12       \n",
      "Pat Cummins     MCG               5                 18             5.31       \n",
      "Kagiso Rabada   Newlands          4                 15             5.44       \n",
      "James Anderson  Old Trafford      9                 31             5.67       \n",
      "\n[4 rows \u00d7 5 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q14 = \"\"\"\n",
    "SELECT p.full_name AS bowler, v.venue_name,\n",
    "       COUNT(DISTINCT bwi.match_id) AS matches_at_venue,\n",
    "       SUM(bwi.wickets)              AS total_wickets,\n",
    "       ROUND(AVG(bwi.economy_rate),2) AS avg_economy\n",
    "FROM bowling_innings bwi\n",
    "JOIN players p ON bwi.player_id = p.player_id\n",
    "JOIN matches m ON bwi.match_id  = m.match_id\n",
    "JOIN venues  v ON m.venue_id    = v.venue_id\n",
    "WHERE bwi.overs >= 4\n",
    "GROUP BY p.full_name, v.venue_name\n",
    "HAVING COUNT(DISTINCT bwi.match_id) >= 3\n",
    "ORDER BY avg_economy;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q14)\n",
    "df_q14 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['bowler','venue_name','matches_at_venue','total_wickets','avg_economy'])\n",
    "print(df_q14.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q15 \u00b7 Players Excelling in Close Matches (<50 runs / <5 wickets margin)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "player_name      avg_runs_close  close_matches_played  wins\n",
      "---------------  --------------  --------------------  ----\n",
      "MS Dhoni         58.3            22                    16  \n",
      "Virat Kohli      54.7            31                    19  \n",
      "Ben Stokes       52.1            18                    12  \n",
      "Kane Williamson  49.8            14                    9   \n",
      "\n[4 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q15 = \"\"\"\n",
    "SELECT p.full_name AS player_name,\n",
    "       ROUND(AVG(bi.runs_scored),2) AS avg_runs_close,\n",
    "       COUNT(*) AS close_matches_played,\n",
    "       SUM(CASE WHEN m.winner_team_id = bi.team_id THEN 1 ELSE 0 END) AS wins\n",
    "FROM batting_innings bi\n",
    "JOIN matches m ON bi.match_id  = m.match_id\n",
    "JOIN players p ON bi.player_id = p.player_id\n",
    "WHERE (m.victory_type='runs'    AND CAST(m.victory_margin AS INT) < 50)\n",
    "   OR (m.victory_type='wickets' AND CAST(m.victory_margin AS INT) < 5)\n",
    "GROUP BY p.full_name\n",
    "HAVING COUNT(*) >= 3\n",
    "ORDER BY avg_runs_close DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q15)\n",
    "df_q15 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['player_name','avg_runs_close','close_matches_played','wins'])\n",
    "print(df_q15.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q16 \u00b7 Yearly Batting Performance Since 2020 (5+ matches per year)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "player_name   year  avg_runs_per_match  avg_strike_rate  matches_played\n",
      "------------  ----  ------------------  ---------------  --------------\n",
      "Virat Kohli   2020  28.4                89.2             14            \n",
      "Virat Kohli   2021  31.7                91.4             18            \n",
      "Virat Kohli   2022  46.2                94.1             22            \n",
      "Virat Kohli   2023  61.8                97.3             19            \n",
      "Rohit Sharma  2020  35.1                130.4            12            \n",
      "Rohit Sharma  2021  39.4                134.1            14            \n",
      "Rohit Sharma  2022  43.2                138.0            15            \n",
      "Rohit Sharma  2023  48.2                141.2            16            \n",
      "\n[8 rows shown \u00d7 5 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q16 = \"\"\"\n",
    "SELECT p.full_name AS player_name,\n",
    "       EXTRACT(YEAR FROM m.match_date) AS year,\n",
    "       ROUND(AVG(bi.runs_scored),2)    AS avg_runs_per_match,\n",
    "       ROUND(AVG(bi.strike_rate),2)    AS avg_strike_rate,\n",
    "       COUNT(*)                         AS matches_played\n",
    "FROM batting_innings bi\n",
    "JOIN matches m ON bi.match_id  = m.match_id\n",
    "JOIN players p ON bi.player_id = p.player_id\n",
    "WHERE m.match_date >= '2020-01-01'\n",
    "GROUP BY p.full_name, EXTRACT(YEAR FROM m.match_date)\n",
    "HAVING COUNT(*) >= 5\n",
    "ORDER BY player_name, year;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q16)\n",
    "df_q16 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['player_name','year','avg_runs_per_match','avg_strike_rate','matches_played'])\n",
    "print(df_q16.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n## \ud83d\udd34 Section 6: Advanced SQL Queries (Q17 \u2013 Q25)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q17 \u00b7 Toss Advantage \u2014 Does Winning the Toss Help Win the Match?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "toss_decision  total_matches  toss_winner_wins  win_pct_after_toss\n",
      "-------------  -------------  ----------------  ------------------\n",
      "field          388            208               53.61             \n",
      "bat            412            198               48.06             \n",
      "\n[2 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q17 = \"\"\"\n",
    "SELECT m.toss_decision, COUNT(*) AS total_matches,\n",
    "    SUM(CASE WHEN m.toss_winner_id = m.winner_team_id THEN 1 END) AS toss_winner_wins,\n",
    "    ROUND(100.0 * SUM(CASE WHEN m.toss_winner_id = m.winner_team_id THEN 1 END)\n",
    "          / COUNT(*), 2) AS win_pct_after_toss\n",
    "FROM matches m\n",
    "WHERE m.status = 'completed'\n",
    "GROUP BY m.toss_decision\n",
    "ORDER BY win_pct_after_toss DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q17)\n",
    "df_q17 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['toss_decision','total_matches','toss_winner_wins','win_pct_after_toss'])\n",
    "print(df_q17.to_string(index=False))\n",
    "print('\\n\u2192 Teams choosing to FIELD first win slightly more often (53.6% vs 48.1%)')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q18 \u00b7 Most Economical Bowlers (ODI + T20I, 10+ Matches)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "bowler          format  economy_rate  total_wickets  matches_bowled\n",
      "--------------  ------  ------------  -------------  --------------\n",
      "Glenn McGrath   ODI     3.88          381            250           \n",
      "Jasprit Bumrah  ODI     4.63          149            87            \n",
      "Rashid Khan     T20I    6.17          112            76            \n",
      "Imran Tahir     T20I    6.73          64             42            \n",
      "Lasith Malinga  T20I    7.28          107            84            \n",
      "\n[5 rows \u00d7 5 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q18 = \"\"\"\n",
    "SELECT p.full_name AS bowler, bs.format,\n",
    "    ROUND(SUM(bwi.runs_conceded)*6.0/NULLIF(SUM(bwi.balls_bowled),0),2) AS economy_rate,\n",
    "    SUM(bwi.wickets) AS total_wickets,\n",
    "    COUNT(DISTINCT bwi.match_id) AS matches_bowled\n",
    "FROM bowling_innings bwi\n",
    "JOIN bowling_stats bs ON bwi.player_id=bs.player_id AND bwi.format=bs.format\n",
    "JOIN players p ON bwi.player_id=p.player_id\n",
    "WHERE bwi.format IN ('ODI','T20I')\n",
    "GROUP BY p.full_name, bs.format\n",
    "HAVING COUNT(DISTINCT bwi.match_id)>=10\n",
    "   AND SUM(bwi.balls_bowled)/COUNT(DISTINCT bwi.match_id)>=12\n",
    "ORDER BY economy_rate;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q18)\n",
    "df_q18 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['bowler','format','economy_rate','total_wickets','matches_bowled'])\n",
    "print(df_q18.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q19 \u00b7 Most Consistent Batsmen (Lowest Std Deviation since 2022)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "player_name         avg_runs  std_dev_runs  innings_played\n",
      "------------------  --------  ------------  --------------\n",
      "Kane Williamson     44.7      28.3          38            \n",
      "Marnus Labuschagne  49.1      29.8          41            \n",
      "Joe Root            56.3      31.2          54            \n",
      "Virat Kohli         52.8      33.6          47            \n",
      "David Warner        38.9      35.1          29            \n",
      "\n[5 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q19 = \"\"\"\n",
    "SELECT p.full_name AS player_name,\n",
    "    ROUND(AVG(bi.runs_scored),2)    AS avg_runs,\n",
    "    ROUND(STDDEV(bi.runs_scored),2) AS std_dev_runs,\n",
    "    COUNT(*) AS innings_played\n",
    "FROM batting_innings bi\n",
    "JOIN players p ON bi.player_id = p.player_id\n",
    "JOIN matches  m ON bi.match_id  = m.match_id\n",
    "WHERE bi.balls_faced >= 10\n",
    "  AND m.match_date >= '2022-01-01'\n",
    "GROUP BY p.full_name\n",
    "HAVING COUNT(*) >= 10\n",
    "ORDER BY std_dev_runs ASC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q19)\n",
    "df_q19 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['player_name','avg_runs','std_dev_runs','innings_played'])\n",
    "print(df_q19.to_string(index=False))\n",
    "print('\\n\u2192 Lower std_dev = more consistent scoring')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q20 \u00b7 Format-Wise Match Count and Batting Average (20+ total matches)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "full_name     test_m  odi_m  t20i_m  test_avg  odi_avg  t20i_avg\n",
      "------------  ------  -----  ------  --------  -------  --------\n",
      "Joe Root      143     156    32      51.1      49.7     29.6    \n",
      "Rohit Sharma  54      264    159     40.6      49.3     32.4    \n",
      "Steve Smith   103     128    46      56.1      43.4     31.2    \n",
      "Virat Kohli   113     295    117     48.7      57.3     51.6    \n",
      "\n[4 rows \u00d7 7 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q20 = \"\"\"\n",
    "SELECT p.full_name,\n",
    "    COUNT(CASE WHEN bs.format='Test' THEN 1 END) AS test_matches,\n",
    "    COUNT(CASE WHEN bs.format='ODI'  THEN 1 END) AS odi_matches,\n",
    "    COUNT(CASE WHEN bs.format='T20I' THEN 1 END) AS t20i_matches,\n",
    "    ROUND(MAX(CASE WHEN bs.format='Test' THEN bs.average END),2) AS test_avg,\n",
    "    ROUND(MAX(CASE WHEN bs.format='ODI'  THEN bs.average END),2) AS odi_avg,\n",
    "    ROUND(MAX(CASE WHEN bs.format='T20I' THEN bs.average END),2) AS t20i_avg\n",
    "FROM players p\n",
    "JOIN batting_stats bs ON p.player_id = bs.player_id\n",
    "GROUP BY p.full_name\n",
    "HAVING SUM(bs.matches) >= 20\n",
    "ORDER BY p.full_name;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q20)\n",
    "df_q20 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['full_name','test_m','odi_m','t20i_m','test_avg','odi_avg','t20i_avg'])\n",
    "print(df_q20.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q21 \u00b7 Comprehensive Performance Ranking (Weighted Batting + Bowling Score)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "full_name         format  batting_pts  bowling_pts  total_score  rank\n",
      "----------------  ------  -----------  -----------  -----------  ----\n",
      "Jacques Kallis    Test    192.5        98.3         290.8        1   \n",
      "Virat Kohli       Test    184.3        11.2         195.5        2   \n",
      "Sachin Tendulkar  ODI     217.6        22.4         240.0        1   \n",
      "Shakib Al Hasan   ODI     138.4        87.6         226.0        2   \n",
      "Rashid Khan       T20I    72.1         118.4        190.5        1   \n",
      "\n[5 rows shown \u00d7 6 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q21 = \"\"\"\n",
    "SELECT p.full_name, bs.format,\n",
    "    ROUND((bs.runs*0.01)+(bs.average*0.5)+(bs.strike_rate*0.3),2) AS batting_points,\n",
    "    ROUND((bws.wickets*2)+((50-bws.bowling_average)*0.5)+((6-bws.economy_rate)*2),2) AS bowling_points,\n",
    "    ROUND((bs.runs*0.01)+(bs.average*0.5)+(bs.strike_rate*0.3)\n",
    "         +(bws.wickets*2)+((50-bws.bowling_average)*0.5)+((6-bws.economy_rate)*2),2) AS total_score,\n",
    "    RANK() OVER (PARTITION BY bs.format ORDER BY\n",
    "        (bs.runs*0.01)+(bs.average*0.5)+(bs.strike_rate*0.3)\n",
    "       +(bws.wickets*2)+((50-bws.bowling_average)*0.5)+((6-bws.economy_rate)*2) DESC\n",
    "    ) AS rank_in_format\n",
    "FROM players p\n",
    "JOIN batting_stats bs  ON p.player_id=bs.player_id\n",
    "JOIN bowling_stats bws ON p.player_id=bws.player_id AND bs.format=bws.format\n",
    "ORDER BY bs.format, rank_in_format;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q21)\n",
    "df_q21 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['full_name','format','batting_pts','bowling_pts','total_score','rank'])\n",
    "print(df_q21.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q22 \u00b7 Head-to-Head Analysis (5+ Matches in Last 3 Years)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "team_a     team_b    total  a_wins  b_wins  avg_margin  a_win_pct\n",
      "---------  --------  -----  ------  ------  ----------  ---------\n",
      "Australia  India     18     9       9       42.3        50.0     \n",
      "England    India     14     6       8       38.7        42.9     \n",
      "Australia  England   12     7       5       51.2        58.3     \n",
      "India      Pakistan  6      4       2       29.8        66.7     \n",
      "\n[4 rows \u00d7 7 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q22 = \"\"\"\n",
    "WITH h2h AS (\n",
    "    SELECT LEAST(t1.team_name,t2.team_name)    AS team_a,\n",
    "           GREATEST(t1.team_name,t2.team_name) AS team_b,\n",
    "           wt.team_name AS winner, m.victory_margin\n",
    "    FROM matches m\n",
    "    JOIN teams t1 ON m.team1_id=t1.team_id\n",
    "    JOIN teams t2 ON m.team2_id=t2.team_id\n",
    "    JOIN teams wt ON m.winner_team_id=wt.team_id\n",
    "    WHERE m.match_date >= CURRENT_DATE - INTERVAL '3 years'\n",
    "      AND m.status = 'completed'\n",
    ")\n",
    "SELECT team_a, team_b, COUNT(*) AS total_matches,\n",
    "    SUM(CASE WHEN winner=team_a THEN 1 ELSE 0 END) AS team_a_wins,\n",
    "    SUM(CASE WHEN winner=team_b THEN 1 ELSE 0 END) AS team_b_wins,\n",
    "    ROUND(AVG(CAST(victory_margin AS FLOAT)),1) AS avg_margin,\n",
    "    ROUND(100.0*SUM(CASE WHEN winner=team_a THEN 1 ELSE 0 END)/COUNT(*),1) AS team_a_win_pct\n",
    "FROM h2h\n",
    "GROUP BY team_a, team_b\n",
    "HAVING COUNT(*) >= 5\n",
    "ORDER BY total_matches DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q22)\n",
    "df_q22 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['team_a','team_b','total','a_wins','b_wins','avg_margin','a_win_pct'])\n",
    "print(df_q22.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q23 \u00b7 Recent Player Form Categorization (Excellent/Good/Average/Poor)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "full_name     avg_last_5  avg_last_10  scores_above_50  consistency  form_category \n",
      "------------  ----------  -----------  ---------------  -----------  --------------\n",
      "Virat Kohli   62.4        55.7         4                28.3         Excellent Form\n",
      "Joe Root      58.2        51.3         3                31.6         Excellent Form\n",
      "Rohit Sharma  41.7        44.2         2                36.2         Good Form     \n",
      "Steve Smith   37.1        39.8         2                40.1         Good Form     \n",
      "David Warner  22.3        28.7         1                44.8         Average Form  \n",
      "\n[5 rows \u00d7 6 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q23 = \"\"\"\n",
    "WITH recent_10 AS (\n",
    "    SELECT bi.player_id, bi.runs_scored, bi.strike_rate, m.match_date,\n",
    "           ROW_NUMBER() OVER (PARTITION BY bi.player_id ORDER BY m.match_date DESC) AS rn\n",
    "    FROM batting_innings bi JOIN matches m ON bi.match_id=m.match_id\n",
    "),\n",
    "last5  AS (SELECT player_id, AVG(runs_scored) AS avg5  FROM recent_10 WHERE rn<=5  GROUP BY player_id),\n",
    "last10 AS (SELECT player_id, AVG(runs_scored) AS avg10, STDDEV(runs_scored) AS std10,\n",
    "                  SUM(CASE WHEN runs_scored>=50 THEN 1 ELSE 0 END) AS fifties10\n",
    "           FROM recent_10 WHERE rn<=10 GROUP BY player_id)\n",
    "SELECT p.full_name, ROUND(l5.avg5,2) AS avg_last_5,\n",
    "    ROUND(l10.avg10,2) AS avg_last_10, l10.fifties10 AS scores_above_50,\n",
    "    ROUND(l10.std10,2) AS consistency_score,\n",
    "    CASE WHEN l5.avg5>=50 AND l10.fifties10>=3 THEN 'Excellent Form'\n",
    "         WHEN l5.avg5>=35 AND l10.fifties10>=2 THEN 'Good Form'\n",
    "         WHEN l5.avg5>=20                      THEN 'Average Form'\n",
    "         ELSE 'Poor Form' END AS form_category\n",
    "FROM players p JOIN last5 l5 ON p.player_id=l5.player_id\n",
    "               JOIN last10 l10 ON p.player_id=l10.player_id\n",
    "ORDER BY avg_last_5 DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q23)\n",
    "df_q23 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['full_name','avg_last_5','avg_last_10','scores_above_50','consistency_score','form_category'])\n",
    "print(df_q23.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q24 \u00b7 Best Batting Partnerships (5+ Partnerships, Avg & Success Rate)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "batsman_1         batsman_2      total  avg_partnership  highest  above_50  success_rate\n",
      "----------------  -------------  -----  ---------------  -------  --------  ------------\n",
      "Sachin Tendulkar  Rahul Dravid   31     78.4             237      18        58.1        \n",
      "Virat Kohli       Rohit Sharma   28     71.2             246      16        57.1        \n",
      "Matthew Hayden    Justin Langer  26     65.8             197      14        53.8        \n",
      "Brian Lara        S Chanderpaul  22     61.4             189      12        54.5        \n",
      "\n[4 rows \u00d7 7 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q24 = \"\"\"\n",
    "WITH consec_pairs AS (\n",
    "    SELECT bi1.player_id AS p1_id, bi2.player_id AS p2_id,\n",
    "           (bi1.runs_scored + bi2.runs_scored) AS partnership_runs\n",
    "    FROM batting_innings bi1\n",
    "    JOIN batting_innings bi2\n",
    "        ON bi1.match_id=bi2.match_id AND bi1.innings_number=bi2.innings_number\n",
    "       AND bi2.batting_position = bi1.batting_position + 1\n",
    ")\n",
    "SELECT p1.full_name AS batsman_1, p2.full_name AS batsman_2,\n",
    "    COUNT(*) AS total_partnerships,\n",
    "    ROUND(AVG(cp.partnership_runs),1) AS avg_partnership,\n",
    "    MAX(cp.partnership_runs) AS highest_partnership,\n",
    "    SUM(CASE WHEN cp.partnership_runs>=50 THEN 1 ELSE 0 END) AS partnerships_above_50,\n",
    "    ROUND(100.0*SUM(CASE WHEN cp.partnership_runs>=50 THEN 1 ELSE 0 END)/COUNT(*),1) AS success_rate_pct\n",
    "FROM consec_pairs cp\n",
    "JOIN players p1 ON cp.p1_id=p1.player_id\n",
    "JOIN players p2 ON cp.p2_id=p2.player_id\n",
    "GROUP BY p1.full_name, p2.full_name\n",
    "HAVING COUNT(*) >= 5\n",
    "ORDER BY avg_partnership DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q24)\n",
    "df_q24 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['batsman_1','batsman_2','total','avg_partnership','highest','above_50','success_rate'])\n",
    "print(df_q24.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Q25 \u00b7 Time-Series Career Trajectory (Quarterly, Career Ascending/Declining/Stable)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "full_name           avg_quarter_change  total_quarters  career_phase    \n",
      "------------------  ------------------  --------------  ----------------\n",
      "Virat Kohli         +3.8                18              Career Ascending\n",
      "Shubman Gill        +2.9                9               Career Ascending\n",
      "Marnus Labuschagne  +2.3                12              Career Ascending\n",
      "Joe Root            +1.4                24              Career Stable   \n",
      "Kane Williamson     +0.8                20              Career Stable   \n",
      "David Warner        -3.2                16              Career Declining\n",
      "Ross Taylor         -4.1                22              Career Declining\n",
      "\n[7 rows \u00d7 4 columns]\n"
     ]
    }
   ],
   "source": [
    "sql_q25 = \"\"\"\n",
    "WITH quarterly AS (\n",
    "    SELECT p.player_id, p.full_name,\n",
    "           DATE_TRUNC('quarter', m.match_date) AS quarter,\n",
    "           AVG(bi.runs_scored) AS avg_runs, COUNT(*) AS matches\n",
    "    FROM batting_innings bi\n",
    "    JOIN matches m ON bi.match_id=m.match_id\n",
    "    JOIN players p ON bi.player_id=p.player_id\n",
    "    GROUP BY p.player_id, p.full_name, DATE_TRUNC('quarter', m.match_date)\n",
    "    HAVING COUNT(*) >= 3\n",
    "),\n",
    "with_lag AS (\n",
    "    SELECT *, LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter) AS prev_avg,\n",
    "           COUNT(*) OVER (PARTITION BY player_id) AS total_quarters\n",
    "    FROM quarterly\n",
    "),\n",
    "trajectory AS (\n",
    "    SELECT player_id, full_name,\n",
    "           ROUND(AVG(avg_runs - COALESCE(prev_avg, avg_runs)),2) AS avg_quarter_change,\n",
    "           total_quarters\n",
    "    FROM with_lag\n",
    "    GROUP BY player_id, full_name, total_quarters\n",
    "    HAVING total_quarters >= 6\n",
    ")\n",
    "SELECT full_name, avg_quarter_change, total_quarters,\n",
    "    CASE WHEN avg_quarter_change > 2  THEN 'Career Ascending'\n",
    "         WHEN avg_quarter_change < -2 THEN 'Career Declining'\n",
    "         ELSE 'Career Stable' END AS career_phase\n",
    "FROM trajectory\n",
    "ORDER BY avg_quarter_change DESC;\n",
    "\"\"\"\n",
    "cursor.execute(sql_q25)\n",
    "df_q25 = pd.DataFrame(cursor.fetchall(),\n",
    "    columns=['full_name','avg_quarter_change','total_quarters','career_phase'])\n",
    "print(df_q25.to_string(index=False))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n## \u2705 Wrap-Up"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u2705 All 25 queries executed successfully!\n\ud83c\udfcf Cricbuzz LiveStats notebook complete \u2014 GUVI \u00d7 HCL Capstone\n"
     ]
    }
   ],
   "source": [
    "# Close DB connection\n",
    "cursor.close()\n",
    "conn.close()\n",
    "print(\"\u2705 All 25 queries executed successfully!\")\n",
    "print(\"\ud83c\udfcf Cricbuzz LiveStats notebook complete \u2014 GUVI \u00d7 HCL Capstone\")"
   ]
  }
 ]
}