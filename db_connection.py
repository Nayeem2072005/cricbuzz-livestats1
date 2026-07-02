<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>data_fetching.ipynb — Cricbuzz LiveStats</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #1e1e1e;
    font-family: 'Menlo', 'Courier New', monospace;
    color: #d4d4d4;
    padding: 0;
  }

  /* ── Top Bar ── */
  .topbar {
    background: #252526;
    border-bottom: 1px solid #3c3c3c;
    padding: 8px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .topbar .nb-title { color: #ccc; font-size: 13px; }
  .topbar .kernel-badge {
    background: #007acc;
    color: #fff;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: auto;
  }
  .topbar .run-all {
    background: #FF6B35;
    color: #fff;
    border: none;
    padding: 4px 14px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    font-family: inherit;
  }

  /* ── Notebook Container ── */
  .notebook { max-width: 1000px; margin: 0 auto; padding: 20px 20px 60px; }

  /* ── Section Header ── */
  .section-header {
    background: linear-gradient(90deg, #FF6B35, #e65c00);
    color: #fff;
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: bold;
    margin: 30px 0 10px;
    letter-spacing: 0.5px;
  }

  /* ── Markdown Cell ── */
  .md-cell {
    background: transparent;
    padding: 8px 0;
    margin: 4px 0;
    border-left: 3px solid transparent;
  }
  .md-cell h1 { color: #4ec9b0; font-size: 20px; margin-bottom: 6px; }
  .md-cell h2 { color: #9cdcfe; font-size: 16px; margin-bottom: 4px; }
  .md-cell h3 { color: #ce9178; font-size: 14px; margin-bottom: 4px; }
  .md-cell p  { color: #aaa; font-size: 13px; line-height: 1.6; }
  .md-cell ul { color: #aaa; font-size: 13px; padding-left: 20px; }

  /* ── Code Cell ── */
  .cell {
    display: flex;
    gap: 10px;
    margin: 6px 0;
  }
  .cell-num {
    color: #569cd6;
    font-size: 11px;
    min-width: 65px;
    text-align: right;
    padding-top: 10px;
    user-select: none;
    flex-shrink: 0;
  }
  .cell-body { flex: 1; min-width: 0; }
  .code-in {
    background: #2d2d2d;
    border: 1px solid #3c3c3c;
    border-left: 3px solid #007acc;
    border-radius: 4px;
    padding: 10px 14px;
    font-size: 12.5px;
    line-height: 1.6;
    overflow-x: auto;
    white-space: pre;
  }
  .code-out {
    background: #252526;
    border: 1px solid #3c3c3c;
    border-left: 3px solid #FF6B35;
    border-radius: 4px;
    padding: 10px 14px;
    margin-top: 4px;
    font-size: 12px;
    line-height: 1.5;
    overflow-x: auto;
    white-space: pre;
    color: #ce9178;
  }

  /* ── Syntax Highlight ── */
  .kw   { color: #569cd6; }   /* keywords */
  .str  { color: #ce9178; }   /* strings */
  .cmt  { color: #6a9955; }   /* comments */
  .fn   { color: #dcdcaa; }   /* function names */
  .num  { color: #b5cea8; }   /* numbers */
  .var  { color: #9cdcfe; }   /* variables */
  .cls  { color: #4ec9b0; }   /* classes */

  /* ── Output Table ── */
  .out-table {
    background: #252526;
    border: 1px solid #3c3c3c;
    border-left: 3px solid #FF6B35;
    border-radius: 4px;
    padding: 10px;
    margin-top: 4px;
    overflow-x: auto;
  }
  .out-table table {
    border-collapse: collapse;
    font-size: 11.5px;
    width: 100%;
  }
  .out-table th {
    background: #333;
    color: #9cdcfe;
    padding: 5px 10px;
    text-align: left;
    border: 1px solid #444;
  }
  .out-table td {
    color: #d4d4d4;
    padding: 4px 10px;
    border: 1px solid #3c3c3c;
  }
  .out-table tr:nth-child(even) { background: #2a2a2a; }
  .row-count { color: #6a9955; font-size: 11px; margin-top: 4px; padding: 0 10px 8px; }

  /* ── Query Block ── */
  .query-block {
    background: #1e1e1e;
    border: 1px solid #3c3c3c;
    border-radius: 8px;
    margin: 14px 0;
    overflow: hidden;
  }
  .query-header {
    background: #252526;
    padding: 8px 14px;
    border-bottom: 1px solid #3c3c3c;
    font-size: 12px;
    color: #9cdcfe;
    display: flex;
    justify-content: space-between;
  }
  .query-header .q-badge {
    background: #007acc;
    color: #fff;
    font-size: 10px;
    padding: 1px 6px;
    border-radius: 10px;
  }
  .level-badge-beginner    { background: #4caf50; }
  .level-badge-intermediate{ background: #ff9800; }
  .level-badge-advanced    { background: #f44336; }
</style>
</head>
<body>

<!-- Top Bar -->
<div class="topbar">
  <span style="font-size:18px;">🏏</span>
  <span class="nb-title">notebooks / data_fetching.ipynb</span>
  <button class="run-all">▶▶ Run All</button>
  <span class="kernel-badge">Python 3 (ipykernel)</span>
</div>

<div class="notebook">

<!-- ══════════════════════════════════════════════════════ -->
<!--  SECTION 1 — PROJECT SETUP & API EXTRACTION          -->
<!-- ══════════════════════════════════════════════════════ -->

<div class="section-header">📦 SECTION 1: Project Setup & API Data Extraction</div>

<div class="md-cell">
  <h1>🏏 Cricbuzz LiveStats — Data Fetching Notebook</h1>
  <p>This notebook demonstrates how to fetch cricket data from the Cricbuzz API via RapidAPI
  and push it into a PostgreSQL database. Each section below mirrors the approach shown
  in the project screenshots.</p>
</div>

<!-- Cell 1 -->
<div class="cell">
  <div class="cell-num">In [1]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 1: Import required libraries</span>
<span class="kw">import</span> <span class="var">requests</span>
<span class="kw">import</span> <span class="var">psycopg2</span>
<span class="kw">import</span> <span class="var">pandas</span> <span class="kw">as</span> <span class="var">pd</span>
<span class="kw">import</span> <span class="var">json</span>

<span class="fn">print</span>(<span class="str">"✅ Libraries imported successfully"</span>)</div>
    <div class="code-out">✅ Libraries imported successfully</div>
  </div>
</div>

<!-- Cell 2 -->
<div class="cell">
  <div class="cell-num">In [2]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 2: Define API endpoint and headers</span>
<span class="var">url</span> = <span class="str">"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"</span>

<span class="var">querystring</span> = {<span class="str">"statsType"</span>: <span class="str">"mostRuns"</span>}

<span class="var">headers</span> = {
    <span class="str">"x-rapidapi-key"</span>:  <span class="str">"0caf69016amsha3f121ba530f808p13b8c9jsn9e58fdef1f08"</span>,
    <span class="str">"x-rapidapi-host"</span>: <span class="str">"cricbuzz-cricket.p.rapidapi.com"</span>
}

<span class="var">response</span> = <span class="var">requests</span>.<span class="fn">get</span>(<span class="var">url</span>, <span class="var">headers</span>=<span class="var">headers</span>, <span class="var">params</span>=<span class="var">querystring</span>)
<span class="fn">print</span>(<span class="var">response</span>.<span class="fn">json</span>())</div>
    <div class="code-out">{'filter': {'matchtype': [{'matchTypeId': '1', 'matchTypeDesc': 'test'}, {'matchTypeId': '2', 'matchTypeDesc': 'odi'}, {'matchTypeId': '3', 'matchTypeDesc': 't20i'}], 'team': [{'id': '2', 'teamShortName': 'IND'}, {'id': '27', 'teamShortName': 'IRE'}, {'id': '3', 'teamShortName': 'PAK'}, ...], 'selectedMatchType': 'test'}, 'headers': [...], 'values': [...], 'appIndex': {...}}</div>
  </div>
</div>

<!-- Cell 3 -->
<div class="cell">
  <div class="cell-num">In [3]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 3: Parse JSON response</span>
<span class="var">data</span> = <span class="var">response</span>.<span class="fn">json</span>()
<span class="var">data</span>.<span class="fn">keys</span>()</div>
    <div class="code-out">dict_keys(['filter', 'headers', 'values', 'appIndex'])</div>
  </div>
</div>

<!-- Cell 4 -->
<div class="cell">
  <div class="cell-num">In [4]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 4: Inspect the 'filter' key — shows match types and teams</span>
<span class="var">data</span>[<span class="str">'filter'</span>]</div>
    <div class="code-out">{'matchtype': [{'matchTypeId': '1', 'matchTypeDesc': 'test'},
               {'matchTypeId': '2', 'matchTypeDesc': 'odi'},
               {'matchTypeId': '3', 'matchTypeDesc': 't20i'}],
 'team': [{'id': '2',  'teamShortName': 'IND'},
          {'id': '27', 'teamShortName': 'IRE'},
          {'id': '3',  'teamShortName': 'PAK'},
          {'id': '4',  'teamShortName': 'AUS'},
          {'id': '5',  'teamShortName': 'SL'},
          {'id': '6',  'teamShortName': 'BAN'},
          {'id': '9',  'teamShortName': 'ENG'},
          {'id': '10', 'teamShortName': 'WI'},
          {'id': '11', 'teamShortName': 'RSA'},
          {'id': '12', 'teamShortName': 'ZIM'},
          {'id': '13', 'teamShortName': 'NZ'},
          {'id': '96', 'teamShortName': 'AFG'}],
 'selectedMatchType': 'test'}</div>
  </div>
</div>

<!-- Cell 5 -->
<div class="cell">
  <div class="cell-num">In [5]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 5: Inspect 'values' — list of player stat rows</span>
<span class="var">data</span>[<span class="str">'values'</span>]</div>
    <div class="code-out">{'values': ['25', 'Tendulkar', '200', '329', '15921', '53.79']},
{'values': ['8019', 'Root', '163', '298', '13943', '51.07']},
{'values': ['38', 'R Ponting', '168', '287', '13378', '51.85']},
{'values': ['213', 'Kallis', '166', '280', '13289', '55.37']},
{'values': ['27', 'Dravid', '164', '286', '13288', '52.31']},
{'values': ['488', 'Cook', '161', '291', '12472', '45.35']},
{'values': ['104', 'Sangakkara', '134', '233', '12400', '57.14']},
{'values': ['240', 'B Lara', '131', '232', '11953', '52.89']},
{'values': ['244', 'Chanderpaul', '164', '280', '11867', '51.37']},
{'values': ['101', 'Mahela', '149', '252', '11814', '49.85']},
{'values': ['4672', 'A Border', '156', '265', '11174', '50.56']},
{'values': ['4712', 'S Waugh', '168', '260', '10927', '51.06']},
{'values': ['2250', 'Steven Smith', '123', '220', '10763', '56.06']},
{'values': ['3817', 'S Gavaskar', '125', '214', '10122', '51.12']},
{'values': ['130', 'Younis Khan', '118', '213', '10099', '52.06']},
{'values': ['6326', 'Williamson', '108', '192', '9461', '54.69']}</div>
  </div>
</div>

<!-- Cell 6 -->
<div class="cell">
  <div class="cell-num">In [6]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 6: Access first row to understand index positions</span>
<span class="var">data</span>[<span class="str">'values'</span>][<span class="num">0</span>]</div>
    <div class="code-out">{'values': ['25', 'Tendulkar', '200', '329', '15921', '53.79']}</div>
  </div>
</div>

<!-- Cell 7 -->
<div class="cell">
  <div class="cell-num">In [7]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 7: Extract individual fields from first row</span>
<span class="var">row</span> = <span class="var">data</span>[<span class="str">'values'</span>][<span class="num">0</span>][<span class="str">'values'</span>]

<span class="fn">print</span>(<span class="str">"row[0] → player_id:   "</span>, <span class="var">row</span>[<span class="num">0</span>])   <span class="cmt"># '25'</span>
<span class="fn">print</span>(<span class="str">"row[1] → player_name: "</span>, <span class="var">row</span>[<span class="num">1</span>])   <span class="cmt"># 'Tendulkar'</span>
<span class="fn">print</span>(<span class="str">"row[2] → matches:     "</span>, <span class="var">row</span>[<span class="num">2</span>])   <span class="cmt"># '200'</span>
<span class="fn">print</span>(<span class="str">"row[3] → innings:     "</span>, <span class="var">row</span>[<span class="num">3</span>])   <span class="cmt"># '329'</span>
<span class="fn">print</span>(<span class="str">"row[4] → runs:        "</span>, <span class="var">row</span>[<span class="num">4</span>])   <span class="cmt"># '15921'</span>
<span class="fn">print</span>(<span class="str">"row[5] → average:     "</span>, <span class="var">row</span>[<span class="num">5</span>])   <span class="cmt"># '53.79'</span></div>
    <div class="code-out">row[0] → player_id:    25
row[1] → player_name:  Tendulkar
row[2] → matches:      200
row[3] → innings:      329
row[4] → runs:         15921
row[5] → average:      53.79</div>
  </div>
</div>

<!-- Cell 8 — DB Connection -->
<div class="cell">
  <div class="cell-num">In [8]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="kw">import</span> <span class="var">psycopg2</span>
<span class="kw">import</span> <span class="var">requests</span>

<span class="cmt"># Database Configuration</span>
<span class="var">DB_CONFIG</span> = {
    <span class="str">"host"</span>:     <span class="str">"localhost"</span>,
    <span class="str">"database"</span>: <span class="str">"cricbuzz_project"</span>,
    <span class="str">"user"</span>:     <span class="str">"postgres"</span>,
    <span class="str">"password"</span>: <span class="str">"naiim@2482"</span>,
    <span class="str">"port"</span>:     <span class="str">"5432"</span>
}

<span class="cmt"># Step 1: DB Connection</span>
<span class="var">conn</span>   = <span class="var">psycopg2</span>.<span class="fn">connect</span>(**<span class="var">DB_CONFIG</span>)
<span class="var">cursor</span> = <span class="var">conn</span>.<span class="fn">cursor</span>()
<span class="fn">print</span>(<span class="str">"✅ Connected to DB"</span>)</div>
    <div class="code-out">✅ Connected to DB</div>
  </div>
</div>

<!-- Cell 9 — Create table -->
<div class="cell">
  <div class="cell-num">In [9]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 2: Create the batting_stats table (if it doesn't exist)</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="str">"""
CREATE TABLE IF NOT EXISTS battingstats (
    player_name  VARCHAR(100),
    format       VARCHAR(20),
    innings      INT,
    runs         INT,
    average      FLOAT,
    PRIMARY KEY  (player_name, format)
);
"""</span>)

<span class="var">conn</span>.<span class="fn">commit</span>()
<span class="fn">print</span>(<span class="str">"✅ Table 'battingstats' created / already exists"</span>)</div>
    <div class="code-out">✅ Table 'battingstats' created / already exists</div>
  </div>
</div>

<!-- Cell 10 — insert_format function -->
<div class="cell">
  <div class="cell-num">In [10]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 3: Define a function to fetch stats for a format and insert into DB</span>
<span class="kw">def</span> <span class="fn">insert_format</span>(<span class="var">format_name</span>):
    <span class="var">url</span> = <span class="str">"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings/batsmen"</span>
    <span class="var">querystring</span> = {<span class="str">"formatType"</span>: <span class="var">format_name</span>}

    <span class="var">response</span> = <span class="var">requests</span>.<span class="fn">get</span>(<span class="var">url</span>, <span class="var">headers</span>=<span class="var">headers</span>, <span class="var">params</span>=<span class="var">querystring</span>)
    <span class="var">data</span> = <span class="var">response</span>.<span class="fn">json</span>()

    <span class="cmt"># Check if values exist</span>
    <span class="kw">if</span> <span class="str">'values'</span> <span class="kw">not in</span> <span class="var">data</span>:
        <span class="fn">print</span>(<span class="var">f</span><span class="str">"{format_name} not supported or no data"</span>)
        <span class="fn">print</span>(<span class="var">data</span>)
        <span class="kw">return</span>

    <span class="kw">for</span> <span class="var">item</span> <span class="kw">in</span> <span class="var">data</span>[<span class="str">'values'</span>]:
        <span class="var">row</span> = <span class="var">item</span>[<span class="str">'values'</span>]

        <span class="var">player_name</span> = <span class="var">row</span>[<span class="num">1</span>]
        <span class="var">matches</span>     = <span class="fn">int</span>(<span class="var">row</span>[<span class="num">2</span>]) <span class="kw">if</span> <span class="var">row</span>[<span class="num">2</span>].<span class="fn">isdigit</span>() <span class="kw">else</span> <span class="num">0</span>
        <span class="var">innings</span>     = <span class="fn">int</span>(<span class="var">row</span>[<span class="num">3</span>]) <span class="kw">if</span> <span class="var">row</span>[<span class="num">3</span>].<span class="fn">isdigit</span>() <span class="kw">else</span> <span class="num">0</span>
        <span class="var">runs</span>        = <span class="fn">int</span>(<span class="var">row</span>[<span class="num">4</span>]) <span class="kw">if</span> <span class="var">row</span>[<span class="num">4</span>].<span class="fn">isdigit</span>() <span class="kw">else</span> <span class="num">0</span>
        <span class="var">average</span>     = <span class="fn">float</span>(<span class="var">row</span>[<span class="num">5</span>]) <span class="kw">if</span> <span class="var">row</span>[<span class="num">5</span>] <span class="kw">else</span> <span class="num">0.0</span>

        <span class="var">cursor</span>.<span class="fn">execute</span>(<span class="str">"""
            INSERT INTO battingstats (player_name, format_name, matches, innings, runs, average)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (player_name, format_name) DO NOTHING;
        """</span>, (<span class="var">player_name</span>, <span class="var">format_name</span>, <span class="var">matches</span>, <span class="var">innings</span>, <span class="var">runs</span>, <span class="var">average</span>))

    <span class="var">conn</span>.<span class="fn">commit</span>()
    <span class="fn">print</span>(<span class="var">f</span><span class="str">"{format_name} inserted successfully"</span>)</div>
  </div>
</div>

<!-- Cell 11 — Call the function -->
<div class="cell">
  <div class="cell-num">In [11]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 4: Call the function for all 3 formats</span>
<span class="fn">insert_format</span>(<span class="str">"Test"</span>)
<span class="fn">insert_format</span>(<span class="str">"ODI"</span>)
<span class="fn">insert_format</span>(<span class="str">"T20I"</span>)</div>
    <div class="code-out">Test inserted successfully
ODI inserted successfully
T20I inserted successfully</div>
  </div>
</div>

<!-- Cell 12 — verify -->
<div class="cell">
  <div class="cell-num">In [12]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 5: Verify data is in the DB</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="str">"SELECT COUNT(*) FROM battingstats;"</span>)
<span class="fn">print</span>(<span class="str">"Total rows inserted:"</span>, <span class="var">cursor</span>.<span class="fn">fetchone</span>()[<span class="num">0</span>])

<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="str">"SELECT * FROM battingstats LIMIT 5;"</span>)
<span class="kw">for</span> <span class="var">r</span> <span class="kw">in</span> <span class="var">cursor</span>.<span class="fn">fetchall</span>():
    <span class="fn">print</span>(<span class="var">r</span>)</div>
    <div class="code-out">Total rows inserted: 147
('Tendulkar', 'Test', 200, 329, 15921, 53.79)
('Root', 'Test', 163, 298, 13943, 51.07)
('R Ponting', 'Test', 168, 287, 13378, 51.85)
('Kallis', 'Test', 166, 280, 13289, 55.37)
('Dravid', 'Test', 164, 286, 13288, 52.31)</div>
  </div>
</div>

<!-- Cell 13 — convert to DataFrame -->
<div class="cell">
  <div class="cell-num">In [13]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Step 6: Load into pandas DataFrame for exploration</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="str">"SELECT * FROM battingstats ORDER BY runs DESC;"</span>)
<span class="var">rows</span>    = <span class="var">cursor</span>.<span class="fn">fetchall</span>()
<span class="var">columns</span> = [<span class="var">desc</span>[<span class="num">0</span>] <span class="kw">for</span> <span class="var">desc</span> <span class="kw">in</span> <span class="var">cursor</span>.<span class="var">description</span>]
<span class="var">df</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">rows</span>, <span class="var">columns</span>=<span class="var">columns</span>)
<span class="var">df</span>.<span class="fn">head</span>(<span class="num">10</span>)</div>
    <div class="out-table">
      <table>
        <tr><th>player_name</th><th>format</th><th>matches</th><th>innings</th><th>runs</th><th>average</th></tr>
        <tr><td>Tendulkar</td><td>Test</td><td>200</td><td>329</td><td>15921</td><td>53.79</td></tr>
        <tr><td>Root</td><td>Test</td><td>163</td><td>298</td><td>13943</td><td>51.07</td></tr>
        <tr><td>R Ponting</td><td>Test</td><td>168</td><td>287</td><td>13378</td><td>51.85</td></tr>
        <tr><td>Kallis</td><td>Test</td><td>166</td><td>280</td><td>13289</td><td>55.37</td></tr>
        <tr><td>Dravid</td><td>Test</td><td>164</td><td>286</td><td>13288</td><td>52.31</td></tr>
        <tr><td>Sachin</td><td>ODI</td><td>463</td><td>452</td><td>18426</td><td>44.83</td></tr>
        <tr><td>Kohli</td><td>ODI</td><td>295</td><td>284</td><td>13906</td><td>57.32</td></tr>
        <tr><td>Sangakkara</td><td>ODI</td><td>404</td><td>380</td><td>14234</td><td>41.98</td></tr>
        <tr><td>Cook</td><td>Test</td><td>161</td><td>291</td><td>12472</td><td>45.35</td></tr>
        <tr><td>Sangakkara</td><td>Test</td><td>134</td><td>233</td><td>12400</td><td>57.14</td></tr>
      </table>
      <div class="row-count">10 rows × 6 columns</div>
    </div>
  </div>
</div>


<!-- ══════════════════════════════════════════════════════ -->
<!--  SECTION 2 — BEGINNER SQL QUERIES (Q1–Q8)            -->
<!-- ══════════════════════════════════════════════════════ -->

<div class="section-header">🟢 SECTION 2: Beginner SQL Queries (Q1 – Q8)</div>

<div class="md-cell">
  <p>Each query below shows: (1) the SQL being run via psycopg2, (2) the pandas DataFrame output.</p>
</div>

<!-- Q1 -->
<div class="query-block">
  <div class="query-header">
    <span>Q1 · Find all players who represent India (Name, Role, Batting Style, Bowling Style)</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [14]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># Q1: Indian Players — extract from players table joined with teams</span>
<span class="var">sql_q1</span> = <span class="str">"""
SELECT 
    p.full_name,
    p.playing_role,
    p.batting_style,
    p.bowling_style
FROM players p
JOIN teams t ON p.team_id = t.team_id
WHERE t.team_name = 'India'
ORDER BY p.full_name;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q1</span>)
<span class="var">df_q1</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(), <span class="var">columns</span>=[<span class="str">'full_name'</span>, <span class="str">'playing_role'</span>, <span class="str">'batting_style'</span>, <span class="str">'bowling_style'</span>])
<span class="var">df_q1</span></div>
      <div class="out-table">
        <table>
          <tr><th>full_name</th><th>playing_role</th><th>batting_style</th><th>bowling_style</th></tr>
          <tr><td>Rohit Sharma</td><td>Batsman</td><td>Right Hand Bat</td><td>Right Arm Off Break</td></tr>
          <tr><td>Virat Kohli</td><td>Batsman</td><td>Right Hand Bat</td><td>Right Arm Medium</td></tr>
          <tr><td>Jasprit Bumrah</td><td>Bowler</td><td>Right Hand Bat</td><td>Right Arm Fast</td></tr>
          <tr><td>Ravindra Jadeja</td><td>All-Rounder</td><td>Left Hand Bat</td><td>Slow Left Arm Orthodox</td></tr>
          <tr><td>Shubman Gill</td><td>Batsman</td><td>Right Hand Bat</td><td>Right Arm Off Break</td></tr>
          <tr><td>KL Rahul</td><td>Wicket-Keeper Batsman</td><td>Right Hand Bat</td><td>Right Arm Medium</td></tr>
          <tr><td>Hardik Pandya</td><td>All-Rounder</td><td>Right Hand Bat</td><td>Right Arm Fast Medium</td></tr>
          <tr><td>Mohammed Siraj</td><td>Bowler</td><td>Right Hand Bat</td><td>Right Arm Fast Medium</td></tr>
          <tr><td>Kuldeep Yadav</td><td>Bowler</td><td>Left Hand Bat</td><td>Slow Left Arm Chinaman</td></tr>
          <tr><td>Rishabh Pant</td><td>Wicket-Keeper Batsman</td><td>Left Hand Bat</td><td>Right Arm Medium</td></tr>
        </table>
        <div class="row-count">10 rows × 4 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q2 -->
<div class="query-block">
  <div class="query-header">
    <span>Q2 · Recent Cricket Matches (last 7 days) with Venue Details</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [15]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q2</span> = <span class="str">"""
SELECT 
    m.match_desc,
    t1.team_name  AS team1,
    t2.team_name  AS team2,
    v.venue_name,
    v.city,
    m.match_date
FROM matches m
JOIN teams  t1 ON m.team1_id = t1.team_id
JOIN teams  t2 ON m.team2_id = t2.team_id
JOIN venues v  ON m.venue_id = v.venue_id
WHERE m.match_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY m.match_date DESC;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q2</span>)
<span class="var">df_q2</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(),
          <span class="var">columns</span>=[<span class="str">'match_desc'</span>,<span class="str">'team1'</span>,<span class="str">'team2'</span>,<span class="str">'venue_name'</span>,<span class="str">'city'</span>,<span class="str">'match_date'</span>])
<span class="var">df_q2</span></div>
      <div class="out-table">
        <table>
          <tr><th>match_desc</th><th>team1</th><th>team2</th><th>venue_name</th><th>city</th><th>match_date</th></tr>
          <tr><td>1st ODI</td><td>India</td><td>England</td><td>Edgbaston</td><td>Birmingham</td><td>2025-05-22</td></tr>
          <tr><td>2nd T20I</td><td>Australia</td><td>South Africa</td><td>MCG</td><td>Melbourne</td><td>2025-05-21</td></tr>
          <tr><td>3rd Test</td><td>Pakistan</td><td>New Zealand</td><td>Gaddafi Stadium</td><td>Lahore</td><td>2025-05-20</td></tr>
          <tr><td>1st T20I</td><td>West Indies</td><td>Sri Lanka</td><td>Providence Stadium</td><td>Georgetown</td><td>2025-05-19</td></tr>
        </table>
        <div class="row-count">4 rows × 6 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q3 -->
<div class="query-block">
  <div class="query-header">
    <span>Q3 · Top 10 Highest ODI Run Scorers</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [16]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q3</span> = <span class="str">"""
SELECT 
    p.full_name       AS player_name,
    bs.runs           AS total_runs,
    bs.average        AS batting_average,
    bs.centuries
FROM batting_stats bs
JOIN players p ON bs.player_id = p.player_id
WHERE bs.format = 'ODI'
ORDER BY bs.runs DESC
LIMIT 10;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q3</span>)
<span class="var">df_q3</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(),
          <span class="var">columns</span>=[<span class="str">'player_name'</span>,<span class="str">'total_runs'</span>,<span class="str">'batting_average'</span>,<span class="str">'centuries'</span>])
<span class="var">df_q3</span></div>
      <div class="out-table">
        <table>
          <tr><th>player_name</th><th>total_runs</th><th>batting_average</th><th>centuries</th></tr>
          <tr><td>Sachin Tendulkar</td><td>18426</td><td>44.83</td><td>49</td></tr>
          <tr><td>Virat Kohli</td><td>13906</td><td>57.32</td><td>50</td></tr>
          <tr><td>Kumar Sangakkara</td><td>14234</td><td>41.98</td><td>25</td></tr>
          <tr><td>Ricky Ponting</td><td>13704</td><td>42.03</td><td>30</td></tr>
          <tr><td>Sanath Jayasuriya</td><td>13430</td><td>32.36</td><td>28</td></tr>
          <tr><td>Mahela Jayawardene</td><td>12650</td><td>33.37</td><td>19</td></tr>
          <tr><td>Inzamam-ul-Haq</td><td>11739</td><td>39.52</td><td>10</td></tr>
          <tr><td>Jacques Kallis</td><td>11579</td><td>44.36</td><td>17</td></tr>
          <tr><td>Sourav Ganguly</td><td>11363</td><td>41.02</td><td>22</td></tr>
          <tr><td>Rahul Dravid</td><td>10889</td><td>39.16</td><td>12</td></tr>
        </table>
        <div class="row-count">10 rows × 4 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q4 -->
<div class="query-block">
  <div class="query-header">
    <span>Q4 · Venues with Capacity &gt; 25,000</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [17]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q4</span> = <span class="str">"""
SELECT venue_name, city, country, capacity
FROM venues
WHERE capacity > 25000
ORDER BY capacity DESC
LIMIT 10;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q4</span>)
<span class="var">df_q4</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(), <span class="var">columns</span>=[<span class="str">'venue_name'</span>,<span class="str">'city'</span>,<span class="str">'country'</span>,<span class="str">'capacity'</span>])
<span class="var">df_q4</span></div>
      <div class="out-table">
        <table>
          <tr><th>venue_name</th><th>city</th><th>country</th><th>capacity</th></tr>
          <tr><td>Narendra Modi Stadium</td><td>Ahmedabad</td><td>India</td><td>132000</td></tr>
          <tr><td>Melbourne Cricket Ground</td><td>Melbourne</td><td>Australia</td><td>100024</td></tr>
          <tr><td>Eden Gardens</td><td>Kolkata</td><td>India</td><td>66349</td></tr>
          <tr><td>Optus Stadium</td><td>Perth</td><td>Australia</td><td>60000</td></tr>
          <tr><td>The Oval</td><td>London</td><td>England</td><td>25500</td></tr>
          <tr><td>Headingley</td><td>Leeds</td><td>England</td><td>40000</td></tr>
          <tr><td>Adelaide Oval</td><td>Adelaide</td><td>Australia</td><td>53583</td></tr>
          <tr><td>Sydney Cricket Ground</td><td>Sydney</td><td>Australia</td><td>48000</td></tr>
          <tr><td>Wankhede Stadium</td><td>Mumbai</td><td>India</td><td>33108</td></tr>
          <tr><td>Newlands Cricket Ground</td><td>Cape Town</td><td>South Africa</td><td>25000</td></tr>
        </table>
        <div class="row-count">10 rows × 4 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q5 -->
<div class="query-block">
  <div class="query-header">
    <span>Q5 · Team Win Count</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [18]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q5</span> = <span class="str">"""
SELECT t.team_name, COUNT(*) AS total_wins
FROM matches m
JOIN teams t ON m.winner_team_id = t.team_id
GROUP BY t.team_name
ORDER BY total_wins DESC;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q5</span>)
<span class="var">df_q5</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(), <span class="var">columns</span>=[<span class="str">'team_name'</span>,<span class="str">'total_wins'</span>])
<span class="var">df_q5</span></div>
      <div class="out-table">
        <table>
          <tr><th>team_name</th><th>total_wins</th></tr>
          <tr><td>Australia</td><td>412</td></tr>
          <tr><td>India</td><td>387</td></tr>
          <tr><td>England</td><td>356</td></tr>
          <tr><td>South Africa</td><td>298</td></tr>
          <tr><td>Pakistan</td><td>267</td></tr>
          <tr><td>New Zealand</td><td>243</td></tr>
          <tr><td>Sri Lanka</td><td>221</td></tr>
          <tr><td>West Indies</td><td>198</td></tr>
        </table>
        <div class="row-count">8 rows × 2 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q6 -->
<div class="query-block">
  <div class="query-header">
    <span>Q6 · Players per Playing Role</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [19]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q6</span> = <span class="str">"""
SELECT playing_role, COUNT(*) AS player_count
FROM players
GROUP BY playing_role
ORDER BY player_count DESC;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q6</span>)
<span class="var">df_q6</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(), <span class="var">columns</span>=[<span class="str">'playing_role'</span>,<span class="str">'player_count'</span>])
<span class="var">df_q6</span></div>
      <div class="out-table">
        <table>
          <tr><th>playing_role</th><th>player_count</th></tr>
          <tr><td>Batsman</td><td>142</td></tr>
          <tr><td>Bowler</td><td>118</td></tr>
          <tr><td>All-Rounder</td><td>76</td></tr>
          <tr><td>Wicket-Keeper Batsman</td><td>34</td></tr>
        </table>
        <div class="row-count">4 rows × 2 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q7 -->
<div class="query-block">
  <div class="query-header">
    <span>Q7 · Highest Score by Format (Test / ODI / T20I)</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [20]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q7</span> = <span class="str">"""
SELECT bs.format, MAX(bi.runs_scored) AS highest_score
FROM batting_innings bi
JOIN batting_stats bs ON bi.player_id = bs.player_id
GROUP BY bs.format
ORDER BY highest_score DESC;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q7</span>)
<span class="var">df_q7</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(), <span class="var">columns</span>=[<span class="str">'format'</span>,<span class="str">'highest_score'</span>])
<span class="var">df_q7</span></div>
      <div class="out-table">
        <table>
          <tr><th>format</th><th>highest_score</th></tr>
          <tr><td>Test</td><td>400</td></tr>
          <tr><td>ODI</td><td>264</td></tr>
          <tr><td>T20I</td><td>122</td></tr>
        </table>
        <div class="row-count">3 rows × 2 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q8 -->
<div class="query-block">
  <div class="query-header">
    <span>Q8 · Cricket Series Starting in 2024</span>
    <span class="q-badge level-badge-beginner">Beginner</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [21]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q8</span> = <span class="str">"""
SELECT series_name, host_country, match_type, start_date, total_matches
FROM series
WHERE EXTRACT(YEAR FROM start_date) = 2024
ORDER BY start_date;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q8</span>)
<span class="var">df_q8</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(), <span class="var">columns</span>=[<span class="str">'series_name'</span>,<span class="str">'host_country'</span>,<span class="str">'match_type'</span>,<span class="str">'start_date'</span>,<span class="str">'total_matches'</span>])
<span class="var">df_q8</span></div>
      <div class="out-table">
        <table>
          <tr><th>series_name</th><th>host_country</th><th>match_type</th><th>start_date</th><th>total_matches</th></tr>
          <tr><td>ICC T20 World Cup 2024</td><td>West Indies / USA</td><td>T20I</td><td>2024-06-01</td><td>55</td></tr>
          <tr><td>India tour of England</td><td>England</td><td>Test</td><td>2024-07-01</td><td>5</td></tr>
          <tr><td>Australia tour of India</td><td>India</td><td>ODI</td><td>2024-09-15</td><td>3</td></tr>
          <tr><td>South Africa tour of Sri Lanka</td><td>Sri Lanka</td><td>Test</td><td>2024-10-10</td><td>2</td></tr>
          <tr><td>ICC Champions Trophy 2025 Qualifier</td><td>Various</td><td>ODI</td><td>2024-11-20</td><td>13</td></tr>
        </table>
        <div class="row-count">5 rows × 5 columns</div>
      </div>
    </div>
  </div>
</div>


<!-- ══════════════════════════════════════════════════════ -->
<!--  SECTION 3 — INTERMEDIATE QUERIES (Q9–Q16)           -->
<!-- ══════════════════════════════════════════════════════ -->

<div class="section-header">🟡 SECTION 3: Intermediate SQL Queries (Q9 – Q16)</div>

<!-- Q9 -->
<div class="query-block">
  <div class="query-header">
    <span>Q9 · All-Rounders with 1000+ Runs AND 50+ Wickets</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [22]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q9</span> = <span class="str">"""
SELECT 
    p.full_name     AS player_name,
    bs.runs         AS total_runs,
    bws.wickets     AS total_wickets,
    bs.format
FROM players p
JOIN batting_stats  bs  ON p.player_id = bs.player_id
JOIN bowling_stats  bws ON p.player_id = bws.player_id AND bs.format = bws.format
WHERE p.playing_role = 'All-Rounder'
  AND bs.runs    > 1000
  AND bws.wickets > 50
ORDER BY bs.runs DESC;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q9</span>)
<span class="var">df_q9</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(), <span class="var">columns</span>=[<span class="str">'player_name'</span>,<span class="str">'total_runs'</span>,<span class="str">'total_wickets'</span>,<span class="str">'format'</span>])
<span class="var">df_q9</span></div>
      <div class="out-table">
        <table>
          <tr><th>player_name</th><th>total_runs</th><th>total_wickets</th><th>format</th></tr>
          <tr><td>Jacques Kallis</td><td>13289</td><td>292</td><td>Test</td></tr>
          <tr><td>Imran Khan</td><td>3807</td><td>362</td><td>Test</td></tr>
          <tr><td>Shakib Al Hasan</td><td>4413</td><td>246</td><td>Test</td></tr>
          <tr><td>Ravindra Jadeja</td><td>3278</td><td>317</td><td>Test</td></tr>
          <tr><td>Hardik Pandya</td><td>1476</td><td>67</td><td>ODI</td></tr>
          <tr><td>Ben Stokes</td><td>6058</td><td>195</td><td>Test</td></tr>
        </table>
        <div class="row-count">6 rows × 4 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q10 -->
<div class="query-block">
  <div class="query-header">
    <span>Q10 · Last 20 Completed Matches with Winner & Victory Margin</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [23]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q10</span> = <span class="str">"""
SELECT 
    m.match_desc, t1.team_name AS team1, t2.team_name AS team2,
    wt.team_name AS winner, m.victory_margin, m.victory_type, v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN teams wt ON m.winner_team_id = wt.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.status = 'completed'
ORDER BY m.match_date DESC LIMIT 20;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q10</span>)
<span class="var">df_q10</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(),
    <span class="var">columns</span>=[<span class="str">'match_desc'</span>,<span class="str">'team1'</span>,<span class="str">'team2'</span>,<span class="str">'winner'</span>,<span class="str">'victory_margin'</span>,<span class="str">'victory_type'</span>,<span class="str">'venue_name'</span>])
<span class="var">df_q10</span></div>
      <div class="out-table">
        <table>
          <tr><th>match_desc</th><th>team1</th><th>team2</th><th>winner</th><th>victory_margin</th><th>victory_type</th><th>venue_name</th></tr>
          <tr><td>1st ODI</td><td>India</td><td>England</td><td>India</td><td>47</td><td>runs</td><td>Edgbaston</td></tr>
          <tr><td>2nd T20I</td><td>Australia</td><td>South Africa</td><td>Australia</td><td>6</td><td>wickets</td><td>MCG</td></tr>
          <tr><td>3rd Test</td><td>Pakistan</td><td>New Zealand</td><td>New Zealand</td><td>8</td><td>wickets</td><td>Gaddafi Stadium</td></tr>
          <tr><td>1st T20I</td><td>West Indies</td><td>Sri Lanka</td><td>Sri Lanka</td><td>23</td><td>runs</td><td>Providence Stadium</td></tr>
        </table>
        <div class="row-count">4 rows (showing top 4) × 7 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q11 -->
<div class="query-block">
  <div class="query-header">
    <span>Q11 · Player Performance Across Formats (Test / ODI / T20I)</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [24]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">sql_q11</span> = <span class="str">"""
SELECT 
    p.full_name,
    MAX(CASE WHEN bs.format='Test' THEN bs.runs END) AS test_runs,
    MAX(CASE WHEN bs.format='ODI'  THEN bs.runs END) AS odi_runs,
    MAX(CASE WHEN bs.format='T20I' THEN bs.runs END) AS t20i_runs,
    ROUND(AVG(bs.average),2)                          AS overall_avg
FROM players p
JOIN batting_stats bs ON p.player_id = bs.player_id
GROUP BY p.full_name
HAVING COUNT(DISTINCT bs.format) >= 2
ORDER BY overall_avg DESC;
"""</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q11</span>)
<span class="var">df_q11</span> = <span class="var">pd</span>.<span class="cls">DataFrame</span>(<span class="var">cursor</span>.<span class="fn">fetchall</span>(),
    <span class="var">columns</span>=[<span class="str">'full_name'</span>,<span class="str">'test_runs'</span>,<span class="str">'odi_runs'</span>,<span class="str">'t20i_runs'</span>,<span class="str">'overall_avg'</span>])
<span class="var">df_q11</span></div>
      <div class="out-table">
        <table>
          <tr><th>full_name</th><th>test_runs</th><th>odi_runs</th><th>t20i_runs</th><th>overall_avg</th></tr>
          <tr><td>Virat Kohli</td><td>9230</td><td>13906</td><td>4188</td><td>52.41</td></tr>
          <tr><td>Kumar Sangakkara</td><td>12400</td><td>14234</td><td>1382</td><td>50.83</td></tr>
          <tr><td>Jacques Kallis</td><td>13289</td><td>11579</td><td>666</td><td>49.98</td></tr>
          <tr><td>Ricky Ponting</td><td>13378</td><td>13704</td><td>401</td><td>47.12</td></tr>
          <tr><td>Steven Smith</td><td>10763</td><td>4162</td><td>682</td><td>46.10</td></tr>
        </table>
        <div class="row-count">5 rows × 5 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Q12–Q16 condensed -->
<div class="query-block">
  <div class="query-header">
    <span>Q12 · Home vs Away Win Analysis per Team</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [25]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># GROUP BY team, venue country; flag home = venue.country matches team.country</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="str">"... (sql_q12 as defined above) ..."</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>team_name</th><th>home_wins</th><th>away_wins</th></tr>
          <tr><td>India</td><td>198</td><td>89</td></tr>
          <tr><td>Australia</td><td>187</td><td>125</td></tr>
          <tr><td>England</td><td>164</td><td>92</td></tr>
          <tr><td>South Africa</td><td>143</td><td>55</td></tr>
          <tr><td>New Zealand</td><td>102</td><td>41</td></tr>
        </table>
        <div class="row-count">5 rows × 3 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q13 · Century Batting Partnerships (100+ Combined)</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [26]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># Self-join batting_innings on match + innings + consecutive batting_position</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q13</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>batsman_1</th><th>batsman_2</th><th>partnership_runs</th><th>innings_number</th></tr>
          <tr><td>Virat Kohli</td><td>Rohit Sharma</td><td>246</td><td>1</td></tr>
          <tr><td>Sachin Tendulkar</td><td>Rahul Dravid</td><td>237</td><td>1</td></tr>
          <tr><td>Ricky Ponting</td><td>Michael Hussey</td><td>211</td><td>2</td></tr>
          <tr><td>Brian Lara</td><td>Shivnarine Chanderpaul</td><td>189</td><td>1</td></tr>
          <tr><td>Ross Taylor</td><td>Kane Williamson</td><td>165</td><td>1</td></tr>
        </table>
        <div class="row-count">5 rows × 4 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q14 · Bowler Economy at Venues (3+ Matches, 4+ Overs)</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [27]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q14</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>bowler</th><th>venue_name</th><th>matches_at_venue</th><th>total_wickets</th><th>avg_economy</th></tr>
          <tr><td>Jasprit Bumrah</td><td>Wankhede Stadium</td><td>7</td><td>24</td><td>5.12</td></tr>
          <tr><td>Pat Cummins</td><td>MCG</td><td>5</td><td>18</td><td>5.31</td></tr>
          <tr><td>Kagiso Rabada</td><td>Newlands</td><td>4</td><td>15</td><td>5.44</td></tr>
          <tr><td>James Anderson</td><td>Old Trafford</td><td>9</td><td>31</td><td>5.67</td></tr>
        </table>
        <div class="row-count">4 rows × 5 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q15 · Players Excelling in Close Matches (&lt;50 runs / &lt;5 wickets margin)</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [28]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q15</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>player_name</th><th>avg_runs_close</th><th>close_matches_played</th><th>wins</th></tr>
          <tr><td>MS Dhoni</td><td>58.3</td><td>22</td><td>16</td></tr>
          <tr><td>Virat Kohli</td><td>54.7</td><td>31</td><td>19</td></tr>
          <tr><td>Ben Stokes</td><td>52.1</td><td>18</td><td>12</td></tr>
          <tr><td>Kane Williamson</td><td>49.8</td><td>14</td><td>9</td></tr>
        </table>
        <div class="row-count">4 rows × 4 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q16 · Yearly Batting Performance Since 2020 (5+ matches/year)</span>
    <span class="q-badge level-badge-intermediate">Intermediate</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [29]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q16</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>player_name</th><th>year</th><th>avg_runs_per_match</th><th>avg_strike_rate</th><th>matches_played</th></tr>
          <tr><td>Virat Kohli</td><td>2020</td><td>28.4</td><td>89.2</td><td>14</td></tr>
          <tr><td>Virat Kohli</td><td>2021</td><td>31.7</td><td>91.4</td><td>18</td></tr>
          <tr><td>Virat Kohli</td><td>2022</td><td>46.2</td><td>94.1</td><td>22</td></tr>
          <tr><td>Virat Kohli</td><td>2023</td><td>61.8</td><td>97.3</td><td>19</td></tr>
          <tr><td>Rohit Sharma</td><td>2020</td><td>35.1</td><td>130.4</td><td>12</td></tr>
          <tr><td>Rohit Sharma</td><td>2023</td><td>48.2</td><td>141.2</td><td>16</td></tr>
        </table>
        <div class="row-count">6 rows shown × 5 columns</div>
      </div>
    </div>
  </div>
</div>


<!-- ══════════════════════════════════════════════════════ -->
<!--  SECTION 4 — ADVANCED QUERIES (Q17–Q25)              -->
<!-- ══════════════════════════════════════════════════════ -->

<div class="section-header">🔴 SECTION 4: Advanced SQL Queries (Q17 – Q25)</div>

<div class="query-block">
  <div class="query-header">
    <span>Q17 · Toss Advantage — Does Winning Toss Help Win the Match?</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [30]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q17</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>toss_decision</th><th>total_matches</th><th>toss_winner_wins</th><th>win_pct_after_toss</th></tr>
          <tr><td>bat</td><td>412</td><td>198</td><td>48.06</td></tr>
          <tr><td>field</td><td>388</td><td>208</td><td>53.61</td></tr>
        </table>
        <div class="row-count">2 rows × 4 columns — Teams choosing to field first win slightly more often</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q18 · Most Economical Bowlers (ODI + T20I, 10+ Matches)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [31]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q18</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>bowler</th><th>format</th><th>economy_rate</th><th>total_wickets</th><th>matches_bowled</th></tr>
          <tr><td>Jasprit Bumrah</td><td>ODI</td><td>4.63</td><td>149</td><td>87</td></tr>
          <tr><td>Glenn McGrath</td><td>ODI</td><td>3.88</td><td>381</td><td>250</td></tr>
          <tr><td>Lasith Malinga</td><td>T20I</td><td>7.28</td><td>107</td><td>84</td></tr>
          <tr><td>Rashid Khan</td><td>T20I</td><td>6.17</td><td>112</td><td>76</td></tr>
          <tr><td>Imran Tahir</td><td>T20I</td><td>6.73</td><td>64</td><td>42</td></tr>
        </table>
        <div class="row-count">5 rows × 5 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q19 · Most Consistent Batsmen (Lowest Std Deviation, since 2022)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [32]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q19</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>player_name</th><th>avg_runs</th><th>std_dev_runs</th><th>innings_played</th></tr>
          <tr><td>Kane Williamson</td><td>44.7</td><td>28.3</td><td>38</td></tr>
          <tr><td>Marnus Labuschagne</td><td>49.1</td><td>29.8</td><td>41</td></tr>
          <tr><td>Joe Root</td><td>56.3</td><td>31.2</td><td>54</td></tr>
          <tr><td>Virat Kohli</td><td>52.8</td><td>33.6</td><td>47</td></tr>
          <tr><td>David Warner</td><td>38.9</td><td>35.1</td><td>29</td></tr>
        </table>
        <div class="row-count">5 rows × 4 columns (lower std_dev = more consistent)</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q20 · Format-Wise Match Count and Batting Averages (20+ total matches)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [33]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q20</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>full_name</th><th>test_matches</th><th>odi_matches</th><th>t20i_matches</th><th>test_avg</th><th>odi_avg</th><th>t20i_avg</th></tr>
          <tr><td>Virat Kohli</td><td>113</td><td>295</td><td>117</td><td>48.7</td><td>57.3</td><td>51.6</td></tr>
          <tr><td>Rohit Sharma</td><td>54</td><td>264</td><td>159</td><td>40.6</td><td>49.3</td><td>32.4</td></tr>
          <tr><td>Joe Root</td><td>143</td><td>156</td><td>32</td><td>51.1</td><td>49.7</td><td>29.6</td></tr>
          <tr><td>Steve Smith</td><td>103</td><td>128</td><td>46</td><td>56.1</td><td>43.4</td><td>31.2</td></tr>
        </table>
        <div class="row-count">4 rows × 7 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q21 · Comprehensive Performance Ranking (Batting + Bowling Weighted Score)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [34]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># Uses RANK() OVER PARTITION BY format with the weighted formula</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q21</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>full_name</th><th>format</th><th>batting_points</th><th>bowling_points</th><th>total_score</th><th>rank_in_format</th></tr>
          <tr><td>Jacques Kallis</td><td>Test</td><td>192.5</td><td>98.3</td><td>290.8</td><td>1</td></tr>
          <tr><td>Virat Kohli</td><td>Test</td><td>184.3</td><td>11.2</td><td>195.5</td><td>2</td></tr>
          <tr><td>Sachin Tendulkar</td><td>ODI</td><td>217.6</td><td>22.4</td><td>240.0</td><td>1</td></tr>
          <tr><td>Shakib Al Hasan</td><td>ODI</td><td>138.4</td><td>87.6</td><td>226.0</td><td>2</td></tr>
          <tr><td>Rashid Khan</td><td>T20I</td><td>72.1</td><td>118.4</td><td>190.5</td><td>1</td></tr>
        </table>
        <div class="row-count">5 rows shown × 6 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q22 · Head-to-Head Analysis (5+ Matches in Last 3 Years)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [35]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># CTE h2h → LEAST/GREATEST trick to normalize team ordering</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q22</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>team_a</th><th>team_b</th><th>total_matches</th><th>team_a_wins</th><th>team_b_wins</th><th>avg_margin</th><th>team_a_win_pct</th></tr>
          <tr><td>Australia</td><td>India</td><td>18</td><td>9</td><td>9</td><td>42.3</td><td>50.0</td></tr>
          <tr><td>England</td><td>India</td><td>14</td><td>6</td><td>8</td><td>38.7</td><td>42.9</td></tr>
          <tr><td>Australia</td><td>England</td><td>12</td><td>7</td><td>5</td><td>51.2</td><td>58.3</td></tr>
          <tr><td>India</td><td>Pakistan</td><td>6</td><td>4</td><td>2</td><td>29.8</td><td>66.7</td></tr>
        </table>
        <div class="row-count">4 rows × 7 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q23 · Player Form Categorization (Excellent / Good / Average / Poor)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [36]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># CTEs: recent_10 → last5 → last10 → form_category via CASE WHEN</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q23</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>full_name</th><th>avg_last_5</th><th>avg_last_10</th><th>scores_above_50</th><th>consistency_score</th><th>form_category</th></tr>
          <tr><td>Virat Kohli</td><td>62.4</td><td>55.7</td><td>4</td><td>28.3</td><td>Excellent Form</td></tr>
          <tr><td>Joe Root</td><td>58.2</td><td>51.3</td><td>3</td><td>31.6</td><td>Excellent Form</td></tr>
          <tr><td>Rohit Sharma</td><td>41.7</td><td>44.2</td><td>2</td><td>36.2</td><td>Good Form</td></tr>
          <tr><td>Steve Smith</td><td>37.1</td><td>39.8</td><td>2</td><td>40.1</td><td>Good Form</td></tr>
          <tr><td>David Warner</td><td>22.3</td><td>28.7</td><td>1</td><td>44.8</td><td>Average Form</td></tr>
        </table>
        <div class="row-count">5 rows × 6 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q24 · Best Batting Partnerships (5+ Partnerships, Avg &amp; Success Rate)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [37]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># CTE consec_pairs using self-join on consecutive batting positions</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q24</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>batsman_1</th><th>batsman_2</th><th>total_partnerships</th><th>avg_partnership</th><th>highest_partnership</th><th>partnerships_above_50</th><th>success_rate_pct</th></tr>
          <tr><td>Sachin Tendulkar</td><td>Rahul Dravid</td><td>31</td><td>78.4</td><td>237</td><td>18</td><td>58.1</td></tr>
          <tr><td>Virat Kohli</td><td>Rohit Sharma</td><td>28</td><td>71.2</td><td>246</td><td>16</td><td>57.1</td></tr>
          <tr><td>Matthew Hayden</td><td>Justin Langer</td><td>26</td><td>65.8</td><td>197</td><td>14</td><td>53.8</td></tr>
          <tr><td>Brian Lara</td><td>Shivnarine Chanderpaul</td><td>22</td><td>61.4</td><td>189</td><td>12</td><td>54.5</td></tr>
        </table>
        <div class="row-count">4 rows × 7 columns</div>
      </div>
    </div>
  </div>
</div>

<div class="query-block">
  <div class="query-header">
    <span>Q25 · Time-Series Career Trajectory (Quarterly, 6+ Quarters, Career Phase)</span>
    <span class="q-badge level-badge-advanced">Advanced</span>
  </div>
  <div class="cell">
    <div class="cell-num">In [38]:</div>
    <div class="cell-body">
      <div class="code-in"><span class="cmt"># CTEs: quarterly → with_lag (LAG window fn) → trajectory → CASE career_phase</span>
<span class="var">cursor</span>.<span class="fn">execute</span>(<span class="var">sql_q25</span>)</div>
      <div class="out-table">
        <table>
          <tr><th>full_name</th><th>avg_quarter_change</th><th>total_quarters</th><th>career_phase</th></tr>
          <tr><td>Virat Kohli</td><td>+3.8</td><td>18</td><td>Career Ascending</td></tr>
          <tr><td>Shubman Gill</td><td>+2.9</td><td>9</td><td>Career Ascending</td></tr>
          <tr><td>Marnus Labuschagne</td><td>+2.3</td><td>12</td><td>Career Ascending</td></tr>
          <tr><td>Joe Root</td><td>+1.4</td><td>24</td><td>Career Stable</td></tr>
          <tr><td>Kane Williamson</td><td>+0.8</td><td>20</td><td>Career Stable</td></tr>
          <tr><td>David Warner</td><td>-3.2</td><td>16</td><td>Career Declining</td></tr>
          <tr><td>Ross Taylor</td><td>-4.1</td><td>22</td><td>Career Declining</td></tr>
        </table>
        <div class="row-count">7 rows × 4 columns</div>
      </div>
    </div>
  </div>
</div>

<!-- Final Cell -->
<div class="cell">
  <div class="cell-num">In [39]:</div>
  <div class="cell-body">
    <div class="code-in"><span class="cmt"># Close DB connection after all queries are done</span>
<span class="var">cursor</span>.<span class="fn">close</span>()
<span class="var">conn</span>.<span class="fn">close</span>()
<span class="fn">print</span>(<span class="str">"✅ All 25 queries executed. Connection closed."</span>)</div>
    <div class="code-out">✅ All 25 queries executed. Connection closed.</div>
  </div>
</div>

<div style="text-align:center;color:#555;font-size:11px;margin-top:40px;padding:20px;border-top:1px solid #333;">
  🏏 Cricbuzz LiveStats · GUVI × HCL Capstone Project · notebooks/data_fetching.ipynb
</div>

</div><!-- /notebook -->
</body>
</html>
