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

tab1, tab2, tab3 = st.tabs(['Single Team All Time', 'Single Team 2023', 'Interesting Graphs'])

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
        
        ax.set_xlabel("Teams")
        ax.set_ylabel("Championship Counts")
        ax.set_title("Top 10 Teams by National Championships (+ Selected Team)")
        ax.set_xticks(indices)
        ax.set_xticklabels(x_labels, rotation=45, ha="right")
        ax.legend()

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
        
        with st.expander("How to use"):
            st.write('''
                Choose your x-axis variable and y-axis variable to see the relationship between the two for the whole league. The red dot is the selected team.
            ''')
    
    with tab3:
        st.subheader("Relationship between Tournament Appearances and Win % (2023)")

        fig_apps, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(data=basketball_df, x='NCAAAppCount', y='WinPct2023', ax=ax)

        ax.set_xlabel("Number of NCAA Tournament Appearances All Time")
        ax.set_ylabel("Win Percentage (2023)")
        ax.set_title("Relationship between Tournament Appearances and Win % (2023)")

        st.pyplot(fig_apps)

        st.subheader("Relationship between Offensive Rebounds and FG% vs 3P FG% (2023)")

        fig_shooting, ax = plt.subplots(figsize=(10, 6))
        
        sns.scatterplot(
            data=basketball_df, 
            x='OffReb2023', 
            y='FGPct2023', 
            color='blue', 
            label='FG%', 
            s=50, 
            ax=ax
        )
        
        sns.scatterplot(
            data=basketball_df, 
            x='OffReb2023', 
            y='3PPct2023', 
            color='red', 
            label='3P%', 
            s=50, 
            ax=ax
        )
        
        ax.set_xlabel("Number of Offensive Rebounds")
        ax.set_ylabel("Field Goal Percentage (2023)")
        ax.set_title("Relationship between Offensive Rebounds and FG% vs 3P FG%")
        ax.legend()

        st.pyplot(fig_shooting)

        both_chips_df = basketball_df[(basketball_df['ConfChampPostCount'] > 0) & (basketball_df['NCAAChampCount'] > 0)]

        teams = both_chips_df['School']
        conference_champs = both_chips_df['RegSeasonConfChampCount']
        national_champs = both_chips_df['NCAAChampCount']

        bar_width = 0.35
        index = np.arange(len(teams))

        
        st.subheader("Conference and National Championships for Teams with Both Titles")

        fig, ax = plt.subplots(figsize=(14, 8))

        bar1 = ax.bar(index, conference_champs, bar_width, label='Conference Championships', color='blue')
        bar2 = ax.bar(index + bar_width, national_champs, bar_width, label='National Championships', color='gold')

        ax.set_xlabel('Teams')
        ax.set_ylabel('Number of Championships')
        ax.set_title('Conference and National Championships for Teams with Both Titles')
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(teams, rotation=90)
        ax.legend()

        st.pyplot(fig)

