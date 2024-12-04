import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

basketball_df = pd.read_csv("basketball_stats.csv")

st.title('Exploring Basketball Statistics')

with st.sidebar:
    search_input = st.text_input("Choose a team:", placeholder="Start typing a team name...")
    selected_team = None

    if search_input:
        matching_teams = basketball_df[basketball_df['School'].str.contains(search_input, case=False, na=False)]

        if not matching_teams.empty:
            selected_team = st.selectbox("Select a team:", matching_teams['School'])

        else:
            st.write("No teams match your search")
    else:
        st.write("Start typing to search for a team")

tab1, tab2 = st.tabs(['Single Team All Time', 'Single Team 2023'])

if selected_team:
    team_stats = basketball_df[basketball_df['School'] == selected_team]

    with tab1:
        st.subheader(f"All-Time Statistics for {selected_team}")

        columns = [
            "AllTimeWins", "AllTimeWinPct", "ConfChampPostCount", 
            "NCAAAppCount", "NCAAFinalFourCount", "NCAAChampCount"
        ]
        table_data = team_stats[columns].rename(columns={
            "AllTimeWins": "All-Time Wins",
            "AllTimeWinPct": "All-Time Win %",
            "ConfChampPostCount": "Conference Tournament Championships",
            "NCAAAppCount": "NCAA Appearances",
            "NCAAFinalFourCount": "Final Four Appearances",
            "NCAAChampCount": "Championships"
        })
        st.table(table_data)

    with tab2:
        st.subheader(f"2023 Season Statistics for {selected_team}")

        columns_2023 = [
            "Wins2023", "WinPct2023", "FGPct2023", 
            "3PPct2023", "FTPct2023", "TotReb2023", "Assists2023"
        ]
        table_data_2023 = team_stats[columns_2023].rename(columns={
            "Wins2023": "2023 Wins",
            "WinPct2023": "2023 Win %",
            "FGPct2023": "Field Goal %",
            "3PPct2023": "Three-Point %",
            "FTPct2023": "Free Throw %",
            "TotReb2023": "Total Rebounds",
            "Assists2023": "Assists"
        })
        st.table(table_data_2023)

