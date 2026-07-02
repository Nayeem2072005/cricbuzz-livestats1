import streamlit as st

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');
    
    .main-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        color: #888;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #FF6B35;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
    }
    .tech-badge {
        background: #FF6B35;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 2px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🏏 Cricbuzz LiveStats</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Real-Time Cricket Insights & SQL-Based Analytics | GUVI × HCL Project</div>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📌 Project Overview")
    st.info("""
    **Cricbuzz LiveStats** is a comprehensive cricket analytics dashboard that integrates 
    live data from the **Cricbuzz API** with a **PostgreSQL** database to deliver real-time 
    match updates, player statistics, and SQL-driven analytics.
    """)

    st.markdown("### 🗂 Navigation Guide")
    st.markdown("""
    | Page | Description |
    |------|-------------|
    | 🔴 **Live Matches** | Real-time match scores & scorecards from Cricbuzz API |
    | 📊 **Top Player Stats** | Batting & bowling rankings fetched live |
    | 🧮 **SQL Analytics** | 25 SQL queries across Beginner → Advanced levels |
    | ✏️ **CRUD Operations** | Add / Update / Delete player records |
    """)

with col2:
    st.markdown("### 🛠 Tech Stack")
    techs = ["Python", "Streamlit", "PostgreSQL", "REST API", "psycopg2", "pandas", "requests", "JSON"]
    for t in techs:
        st.markdown(f'<span class="tech-badge">{t}</span>', unsafe_allow_html=True)

    st.markdown("### 📁 Project Structure")
    st.code("""
cricbuzz_livestats/
├── app.py              # Entry point
├── requirements.txt
├── pages/
│   ├── live_matches.py
│   ├── top_stats.py
│   ├── sql_queries.py
│   └── crud_operations.py
├── utils/
│   └── db_connection.py
└── notebooks/
    └── data_fetching.ipynb
    """, language="text")

st.markdown("---")
st.markdown("### 🎯 Business Use Cases")

uc1, uc2, uc3 = st.columns(3)
with uc1:
    st.markdown("**📺 Sports Media**")
    st.markdown("Real-time match updates, player performance analysis, historical trends")
with uc2:
    st.markdown("**🎮 Fantasy Cricket**")
    st.markdown("Player form tracking, head-to-head stats, real-time score updates")
with uc3:
    st.markdown("**📈 Analytics Firms**")
    st.markdown("Statistical modeling, performance trends, data-driven insights")

st.markdown("---")
st.caption("Created as part of GUVI × HCL Capstone Project | Domain: Sports Analytics")
