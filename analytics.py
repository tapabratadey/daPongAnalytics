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
import plotly.express as px

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
		
</style>
""",
        unsafe_allow_html=True,
    )

######################################################################
# HORIZONTAL CONTAINERS
######################################################################

header_container = st.beta_container()
leaderboard_container = st.beta_container()
player_data_header_container = st.beta_container()	
player_data_container = st.beta_container()
head_to_head_header_container = st.beta_container()
head_to_head_container = st.beta_container()
player_earnings_header = st.beta_container()
player_earnings = st.beta_container()

######################################################################
# HEADER
######################################################################

with header_container:
	st.markdown("<h1 style='text-align: center'>TT Analytics Dashboard</h1>", unsafe_allow_html=True)
	st.write("***")
	st.markdown("<h2 style='text-align: center'>Leaderboard</h2>", unsafe_allow_html=True)

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
			y = alt.Y('Win %:Q', axis=alt.Axis(format="%", tickCount=leaderBoard.shape[0], grid=False)),
			tooltip=['Rank', 'Win %']
		).interactive()
		st.altair_chart(chart, use_container_width=True)

######################################################################
# PLAYER DATA HEADER
######################################################################

with player_data_header_container:
	st.markdown("<h2 style='text-align: center'>Player Data</h2>", unsafe_allow_html=True)
	st.markdown("<h5 style='text-align: center'>Select a player to view player data</h5>", unsafe_allow_html=True)

######################################################################
# PLAYER DATA
######################################################################

with player_data_container:	
	start_player_list = ['Select a player'] + df['Player'].unique().tolist()
	st.text("\n")
	selectedPlayer = st.selectbox('', start_player_list)
	if (selectedPlayer != "Select a player"):
		idx, c = np.where(df == selectedPlayer)
		st.markdown("<h3 style='text-align: center'>{} #{}</h3>".format(selectedPlayer, 
		df.iloc[idx].values[0][14]), unsafe_allow_html=True)
		pdChart = pd.DataFrame(
			{
				'Player Data': df.columns[1:14],
				'Values': df.iloc[idx].values[0][1:14]
			}
		)
		playerDataChart = alt.Chart(pdChart).mark_bar().encode(
			x = alt.X('Player Data:O'),
			y = alt.Y('Values:Q', axis=alt.Axis(format='%', tickCount=leaderBoard.shape[0])),
			tooltip=['Player Data', 'Values']
		).properties(
			height=600
		).interactive()
		st.altair_chart(playerDataChart, use_container_width=True)

######################################################################
# PLAYER HEAD-TO-HEAD HEADER
######################################################################

with head_to_head_header_container:
	st.markdown("<h2 style='text-align: center'>Player Head-To-Head Data</h2>", unsafe_allow_html=True)
	st.markdown("<h5 style='text-align: center'>Select 2 players for a head-to-head comparison</h5>", unsafe_allow_html=True)

######################################################################
# PLAYER HEAD-TO-HEAD DATA
######################################################################	

with head_to_head_container:
	p1Score = 0
	p2Score = 0
	selectPlayers = st.multiselect('', df['Player'])
	if len(selectPlayers) > 2:
		st.error('You can only choose 2 players')
	if len(selectPlayers) == 2:
		idx, c = np.where(df == selectPlayers[0])
		idx1, c1 = np.where(df == selectPlayers[1])
		st.markdown("<h3 style='text-align: center'>{} #{} v. {} #{}</h3>".format(selectPlayers[0], 
		df.iloc[idx].values[0][14], selectPlayers[1], df.iloc[idx1].values[0][14]), unsafe_allow_html=True)
		stats = df.columns[1:14]
		compareDF = pd.DataFrame(
    [df.iloc[idx].values[0][:14], df.iloc[idx1].values[0][:14]],
    columns=df.columns[:14]
		)

		fig = px.bar(compareDF, x="Player", y=df.columns[:14], barmode='group', height=600)
		fig.update_layout(
			yaxis = dict(
				tickformat = ',.0%',
				range = [0,1]
		))
		st.plotly_chart(fig, use_container_width=True)
		st.markdown("<h3 style='text-align: center'>Who would win?</h3>", unsafe_allow_html=True)
		toLoop = len(df.iloc[idx].values[0][1:15])
		p1Score = 0
		p2Score = 0
		for i in range(1, toLoop):
			p1Score += df.iloc[idx].values[0][i]
			p2Score += df.iloc[idx1].values[0][i]
		st.markdown("<h4 style='text-align: center'>Based on the cumulative data, the predicted winner is....</h4>", unsafe_allow_html=True)
		if p1Score < p2Score:
			st.markdown("<h4 style='text-align: center'>{} with a score of {}, comparing to {}'s score of {}</h4>".format(selectPlayers[1], p2Score,selectPlayers[0], round(p1Score, 2)), unsafe_allow_html=True)
		elif p2Score < p1Score:
			st.markdown("<h4 style='text-align: center'>{} with a score of {}, comparing to {}'s score of {}</h4>".format(selectPlayers[0], round(p1Score, 2), selectPlayers[1], p2Score), unsafe_allow_html=True)					

######################################################################
# PLAYER EARNINGS HEADER
######################################################################

with player_earnings_header:
	st.markdown("<h2 style='text-align: center'>Player Earning</h2>", unsafe_allow_html=True)
	st.markdown("<h5 style='text-align: center'>Select 2 players for a head-to-head comparison</h5>", unsafe_allow_html=True)

######################################################################
# PLAYER HEAD-TO-HEAD DATA
######################################################################	

# with player_earnings:
