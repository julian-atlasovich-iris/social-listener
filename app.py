import streamlit as st
import twint
import pandas as pd
import nest_asyncio
nest_asyncio.apply()


q = st.text_input('Search tearm')
username = st.text_input('From username (optional)')
limit = st.text_input('Count of tweets (multiple of 20)')
from_date = st.date_input('From Date')
to_date = st.date_input('To Date')
search = st.button('Search')

if search:
	c = twint.Config()	
	c.Limit = int(limit)
	c.Pandas = True
	c.Since = str(from_date) + ' 00:00:00'
	c.Until = str(to_date) + ' 00:00:00'
	c.Hide_output = True
	#c.Lang = 'en'
	#c.Custom = ['id','date', 'time', 'username', 'tweet']
	#c.Filter_retweets = True
	#c.Resume = 'history_ids.txt'
	if username is not None and username != '':
		c.Username = username
	if q is not None and q != '':
		c.Search = q		

	twint.run.Search(c)
	df = twint.storage.panda.Tweets_df

	if len(df) > 0:
		st.write(df[['id','date','tweet','username']])
		csv = df.to_csv(index=False).encode('utf-8')
		st.download_button("Download",csv,"file.csv","text/csv",key='download-csv')
		df['calendar_date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
		
		st.line_chart(df['calendar_date'].value_counts())
		st.write(df['calendar_date'].value_counts())
	else:
		st.write('No results, or error')		

