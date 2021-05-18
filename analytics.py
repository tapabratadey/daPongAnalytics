import streamlit as st
import pandas as pd
import altair as alt
import numpy as np


# HEADER 
hdCol1, hdCol2, hdCol3 = st.beta_columns(3)
with hdCol1:
	st.write("")
with hdCol2:
	st.title("Dashboard")
with hdCol3:
	st.write("")

"""
***
"""

# HEADER - LEADERBOARD
hdCol4, hdCol5, hdCol6 = st.beta_columns([2, 1, 2])
with hdCol5:
	"""
	### Leaderboard
	"""

# LEADERBOARD
lbCol1, lbCol2 = st.beta_columns(2)
with lbCol1:	
	# read csv
	# make a copy of the dataframe as df
	athlete_data = pd.read_csv('player_stats.csv')
	df = athlete_data.copy()
	
	# grab Player and Wins columns, rename, 
	# remove index and convert win ratio to percent
	dfLeaderBoard = df[['Rank','Player', 'Wins']]
	dfLeaderBoard.columns = ['Rank', 'Player', 'Win %']
	dfLeaderBoard.index = [""] * len(dfLeaderBoard)
	dfLeaderBoard['Win %'] = (dfLeaderBoard['Win %'] * 100).astype(str) + "%"

	st.table(dfLeaderBoard)

with lbCol2:
	
	st.bar_chart(df[['Player', 'Wins']])
	

st.write("***")	
# HEADER - PLAYER DATA 
pdCol1, pdCol2, pdCol3 = st.beta_columns([2, 1, 2])
with pdCol2:
	"""
	### Player Data
	"""
pdCol4, pdCol5, pdCol6 = st.beta_columns([1, 3, 1])
with pdCol5:
	"""
	##### (Select a player from the sidebar on the left to a view player data)
	"""

st.write("#")	

#	PLAYER DATA
option = st.sidebar.selectbox('Select a player to view player data', dfLeaderBoard['Player'])
			
option

