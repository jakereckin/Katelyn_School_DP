import streamlit as st
import datetime as dt
import sys
sys.path.insert(1, 'Katelyn_HW_SL/functions')
from utils import get_students, create_db, select_students_hetrick

st.set_page_config('Hetrick Homeroom')
st.sidebar.header('Hetrick Homeroom')
conn = create_db()
hetrick_students = select_students_hetrick(conn)
hetrick_students['DATE'] = dt.datetime.today().strftime('%m/%d/%Y')
hw_cats = ['YES', 'NO', 'ABSENT']
hetrick_students['HW_DONE'] = 'YES'
hetrick_students['HW_DONE'] = hetrick_students['HW_DONE'].astype('category').cat.remove_categories(hetrick_students['HW_DONE']).cat.add_categories(hw_cats)
hetrick_students['HW_DONE'] = 'YES'
edited_df = st.data_editor(hetrick_students, column_config={'NAME': 'Name', 'DATE': 'Date', 'HW_DONE': st.column_config.SelectboxColumn(label='HW_DONE', options=['YES', 'NO', 'ABSENT'])}, disabled=['NAME', 'DATE'])
st.session_state.df = hetrick_students
if st.button('Submit'):
    st.session_state.df = edited_df
    print(st.session_state.df)