import streamlit as st
import datetime as dt
import sys
import time
import pandas as pd
import os
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from functions import utils as ut
from streamlit_extras.switch_page_button import switch_page
import plotly.express as px

st.set_page_config('Results')
st.sidebar.header('Results')


conn = ut.create_db()
all = ut.select_full_results(conn)
counts, count_all = ut.select_counts(conn)


names = list(counts['NAME'].unique())

name_box = st.selectbox('Choose student', names)
names = list(counts['NAME'].unique())
_counts= counts[counts['NAME']==name_box]
_all = all[all['NAME']==name_box]
st.dataframe(_all, hide_index=True, use_container_width=True)
fig = px.bar(count_all, 
             x='WEEK_START', 
             y='HW_NOT_DONE_COUNT',
             title=f'Homework Assignmnets Not Done for {name_box}')
fig.update_layout(xaxis_title='Week',
                  yaxis_title='Homework Not Done',)
fig2 = px.bar(counts, 
             x='WEEK_START', 
             y='HW_NOT_DONE_COUNT',
             title='Homework Assignmnets Not Done for All Students')
fig2.update_layout(xaxis_title='Week',
                  yaxis_title='Homework Not Done')
st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)