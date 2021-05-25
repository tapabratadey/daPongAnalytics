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
from math import sqrt
from random import seed, randrange
import csv

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
	st.markdown("<h2 style='text-align: center'>Player Earnings</h2>", unsafe_allow_html=True)
	st.markdown("<h5 style='text-align: center'>Based on match winnings</h5>", unsafe_allow_html=True)

######################################################################
# PLAYER EARNINGS
######################################################################	

######################################################################
# LINEAR REGRESSION  
# linear relationship between # of matches (x) and earnings (y)
# y = b_0 + b_1 * x
######################################################################	

# root mean squared error
# diff between prediction vs actual values
def root_mean_squared_err(real, pred):
	total_err = 0.0
	for x in range(len(real)):
		pred_err = pred[x] - real[x]
		total_err += (pred_err**2)
	err_mean = total_err / float(len(real))
	return sqrt(err_mean)

# eval algo on trained data
def training_test_sets_split(df, split_rate):
	training_set = list()
	training_set_size = split_rate * len(df)
	df_copy = list(df)
	while len(training_set) < training_set_size:
		idx = randrange(len(df_copy))
		training_set.append(df_copy.pop(idx))
	return training_set, df_copy

# eval algo on trained data
def eval_algo(df, algo, split_rate):
	training_set, testing_set = training_test_sets_split(df, split_rate)
	test_set = list()
	for row in testing_set:
		temp_row = list(row)
		temp_row[-1] = None
		test_set.append(temp_row)
	pred = algo(training_set, test_set)
	real = [row[-1] for row in testing_set]
	sqrt_mean = root_mean_squared_err(real, pred)
	return sqrt_mean

# calculate mean
def find_mean(vals):
	mean = sum(vals) / float(len(vals))
	return mean

# calculate variance (how the numbers diverge)
def find_variance(vals, mean):
	variance = sum([(x-mean)**2 for x in vals])
	return variance

# calcualte covariance (how the numbers change together)
def find_covariance(x_vals, x_mean, y_vals, y_mean):
	covariance = 0.0
	for i in range(len(x_vals)):
		covariance += (x_vals[i] - x_mean) * (y_vals[i] - y_mean)
	return covariance

# calculate coefficients
def find_coefficients(df):
	x_vals = [row[0] for row in df]
	y_vals = [row[1] for row in df]
	x_mean = find_mean(x_vals)
	y_mean = find_mean(y_vals)
	b_1 = find_covariance(x_vals, x_mean, y_vals, y_mean) / find_variance(x_vals, x_mean)
	b_0 = y_mean - b_1 * x_mean
	fig = px.scatter(
			x=x_vals,
			y=y_vals,
			title="Player Earnings from matching winnings"
	)
	fig.update_layout(
			xaxis_title="Matches Won",
			yaxis_title="Earnings (in thousands)",
	)
	st.plotly_chart(fig, use_container_width=True)
	return [b_0, b_1]

# predict using linear regression
def linear_regression(trained_data, test_data):
	pred = list()
	x_vals = list()
	b_0, b_1 = find_coefficients(trained_data)
	for row in test_data:
		# y = b_0 + b_1 * x
		y = b_0 + b_1 * row[0]
		pred.append(y)
		x_vals.append(row[0])
	fig = px.scatter(
			x=x_vals,
			y=pred,
			title="Predicted player earnings using Linear Regression"
	)
	fig.update_layout(
			xaxis_title="Matches Won",
			yaxis_title="Earnings (in thousands)",
	)
	st.plotly_chart(fig, use_container_width=True)
	return pred

seed(1)
def read_csv(f_name):
	df = list()
	with open(f_name) as earnings_csv:
		csv_reader = csv.reader(earnings_csv)
		for row in csv_reader:
			if not row:
				continue
			if (row[0] != 'Matches Won') or (row[1] != 'Earnings'):
				df.append(row)
	return df

# convert string to float
def conv_to_float(df, column):
	for row in df:
		row[column] = float(row[column].strip())

# read csv
df = read_csv('player_earnings.csv')
for i in range(len(df[0])):
	conv_to_float(df, i)

# 60% data is used to train the model
rmse = eval_algo(df, linear_regression, 0.6)
print('RMSE: %.3f' % (rmse))