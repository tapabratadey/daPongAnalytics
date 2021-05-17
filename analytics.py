import streamlit as st
import pandas as pd
athlete_data = pd.read_csv('player_stats.csv')
df = athlete_data.copy()
dfLeaderBoard = df[['Player', 'Wins']]
dfLeaderBoard.index = [""] * len(dfLeaderBoard)
st.dataframe(dfLeaderBoard, None, height=600)