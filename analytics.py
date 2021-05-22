# TO RUN THE APP:
# open terminal
# go to streamlit file location
# install libs, run: "pip install -r requirements.txt"
# "streamlit run analytics.py"

######################################################################
# imports
######################################################################

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from streamlit.elements import markdown


######################################################################
# Page Styles
######################################################################

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
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }}
    img{{
    	max-width:40%;
    	margin-bottom:40px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )

######################################################################
# HORIZONTAL CONTAINERS
######################################################################

header_container = st.beta_container()
leaderboard_container = st.beta_container()	
player_data_container = st.beta_container()
head_to_head_container = st.beta_container()

######################################################################
# HEADER
######################################################################

with header_container:
	st.title("TT Analytics Dashboard")
	st.write("***")
	st.header("Leaderboard")

######################################################################
# LEADERBOARD
######################################################################

with leaderboard_container:
	lbCol1, lbCol2 = st.beta_columns(2)
	
	# display leaderboard
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
		# dfLeaderBoard
		st.table(dfLeaderBoard)
	
	# display leaderboard data in bar chart
	with lbCol2:
		st.write('#')
		st.write('#')
		leaderBoard = pd.DataFrame(
			{
				'Win %': df['Win %'],
				'Rank': df["Rank"]
			}, 
		)
		chart = alt.Chart(leaderBoard).mark_bar().encode(
			x = alt.X('Rank:O'),
			y = alt.Y('Win %:Q', axis=alt.Axis(format="%", tickCount=leaderBoard.shape[0], grid=False))
		)
		st.altair_chart(chart, use_container_width=True)

######################################################################
# PLAYER DATA
######################################################################

with player_data_container:
	st.header("Player data")
	start_player_list = ['Select a player'] + df['Player'].unique().tolist()
	start_data_list = ['Select player data'] + df.columns[1:].unique().tolist()
	selectedPlayer = st.selectbox('Select a player to view player data', start_player_list)
	if (selectedPlayer != "Select a player"):
		idx, c = np.where(df == selectedPlayer)
		st.subheader('Player: %s #%d' % (selectedPlayer, df.iloc[idx].values[0][14]))
		pdChart = pd.DataFrame(
			{
				'Player Data': df.columns[1:14],
				'Values': df.iloc[idx].values[0][1:14]
			}
		)
		playerDataChart = alt.Chart(pdChart).mark_bar().encode(
			x = alt.X('Player Data:O'),
			y = alt.Y('Values:Q', axis=alt.Axis(format='%', tickCount=leaderBoard.shape[0])),
		).properties(
			height=600
		)
		st.altair_chart(playerDataChart, use_container_width=True)