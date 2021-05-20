import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import base64
import plotly.figure_factory as ff
from streamlit.elements import markdown

# STYLES
st.set_page_config(page_title='TT Analytics', 
												page_icon = "🏓", layout = 'centered', 
												initial_sidebar_state = 'auto')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# HEADER 
hdCol1, hdCol2, hdCol3 = st.beta_columns([1, 3, 1])
with hdCol1:
	st.write("")
with hdCol2:
	st.title("TT Analytics Dashboard")
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

# LEADERBOARD - TABLE
lbCol1, lbCol2 = st.beta_columns(2)
with lbCol1:	
	# read csv
	# make a copy of the dataframe as df
	athlete_data = pd.read_csv('player_stats.csv')
	df = athlete_data.copy()
	
	# grab Player and Wins columns, rename, 
	# remove index and convert win ratio to percent
	dfLeaderBoard = df[['Rank','Player', 'Win %']]
	# dfLeaderBoard.columns = ['Rank', 'Player', 'Win %']
	dfLeaderBoard.index = [""] * len(dfLeaderBoard)
	dfLeaderBoard['Win %'] = (dfLeaderBoard['Win %'] * 100).astype(str) + "%"

	st.table(dfLeaderBoard)
# LEADERBOARD - BAR CHART
with lbCol2:
	st.write('#')
	st.write('#')
	leaderBoard = pd.DataFrame(
		{
			'Win %': df['Win %'] * 100,
			'Rank': df["Rank"]
		}, 
	)
	chart = alt.Chart(leaderBoard).mark_bar().encode(
		x = alt.X('Rank:O', axis=alt.Axis(tickCount=leaderBoard.shape[0], grid=False)),
		y = alt.Y('Win %:Q')
	)
	st.altair_chart(chart, use_container_width=True)

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

#	PLAYER DATA - SideBar options
selectedPlayer = st.sidebar.selectbox('Select a player to view player data', dfLeaderBoard['Player'])
selectedPlayer
idx, c = np.where(df == selectedPlayer)
selectedPlayerData = st.selectbox('Select type of player data', df.columns[1:])
selectedPlayerData
df["%s" %selectedPlayerData][idx]














# HEAD TO HEAD STATS
st.write("***")	
# HEADER - PLAYER DATA 
pdCol1, pdCol2, pdCol3 = st.beta_columns([1.5, 2, 1.5])
with pdCol2:
	"""
	### Player Head-to-Head Stats
	"""
pdCol4, pdCol5, pdCol6 = st.beta_columns([1, 4, 1])
with pdCol5:
	"""
	##### (Select 2 players from the sidebar on the left to a view head-to-head stats)
	"""
st.write("#")	

# PLAYER HEAD TO HEAD STATS
playerH2H = st.sidebar.multiselect('Please choose 2 players to view head-to-head stats', dfLeaderBoard['Player'])
if len(playerH2H) > 2:
	st.error('You can pick 2 players at a time')
if len(playerH2H) == 2:
	pdCol7, pdCol8, pdCol9 = st.beta_columns(3)
	with pdCol7:
		playerH2H[0]
	with pdCol8:
		playerH2H[1]

def downloadCSV():
	csv = df.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()
	href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download csv file</a>'
	return href

#Download CSV file
st.markdown(downloadCSV(), unsafe_allow_html = True)