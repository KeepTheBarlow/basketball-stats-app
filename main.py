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

        st.subheader("Top 10 Teams by National Championships")

        top_10_teams = basketball_df.nlargest(10, 'NCAAChampCount')[['School', 'NCAAChampCount', 'ConfChampPostCount']]

        if selected_team and selected_team not in top_10_teams['School'].values:
            selected_team_data = basketball_df[basketball_df['School'] == selected_team][['School', 'NCAAChampCount', 'ConfChampPostCount']]
            top_10_teams = pd.concat([top_10_teams, selected_team_data], ignore_index=True)
        
        top_10_teams = top_10_teams.sort_values(by='NCAAChampCount', ascending=False).reset_index(drop=True)

        x_labels = top_10_teams['School']
        bar_width = 0.35
        fig_chips, ax = plt.subplots(figsize=(10, 6))

        indices = np.arange(len(x_labels))
        ax.bar(indices - bar_width/2, top_10_teams['NCAAChampCount'], bar_width, label="National Championships", color="blue")
        ax.bar(indices + bar_width/2, top_10_teams['ConfChampPostCount'], bar_width, label="Conference Championships", color="orange")

        if selected_team and selected_team not in basketball_df.nlargest(10, 'NCAAChampCount')['School'].values:
            ax.bar(
                [len(top_10_teams) - 1 - bar_width/2],
                [top_10_teams.iloc[-1]['NCAAChampCount']],
                bar_width,
                color="green",
                label=f"{selected_team} (Selected)"
            )
            ax.bar(
                [len(top_10_teams) - 1 + bar_width/2],
                [top_10_teams.iloc[-1]['ConfChampPostCount']],
                bar_width,
                color="green"
            )
        st.pyplot(fig_chips)

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

        x_axis = st.selectbox("Select X-axis variable for scatterplot", ["Wins2023", "WinPct2023", "Points2023", "FGPct2023", 
                                                                         "3PPct2023", "FTPct2023", "TotReb2023", "Assists2023", 
                                                                         "Steals2023", "Blocks2023", "Turnovers2023"],
                               index=0)
        y_axis = st.selectbox("Select Y-axis variable for scatterplot", ["Wins2023", "WinPct2023", "Points2023", "FGPct2023", 
                                                                         "3PPct2023", "FTPct2023", "TotReb2023", "Assists2023", 
                                                                         "Steals2023", "Blocks2023", "Turnovers2023"],
                               index=1)
        if x_axis and y_axis:
        
            fig_scatter, ax = plt.subplots()

            ax.scatter(
                basketball_df[x_axis],
                basketball_df[y_axis],
                color="blue",
                label="All Teams"
            )
            
            team_data = basketball_df[basketball_df['School'] == selected_team]
            ax.scatter(
                team_data[x_axis],
                team_data[y_axis],
                color="red",
                s=100,
                label=f"{selected_team}"
            )
            st.pyplot(fig_scatter)

