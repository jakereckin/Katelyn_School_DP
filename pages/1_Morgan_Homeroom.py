import streamlit as st
import datetime as dt
import sys
sys.path.insert(1, 'Katelyn_HW_SL/functions')
from utils import get_students, create_db, select_students_morgan

st.set_page_config('Morgan Homeroom')
st.sidebar.header('Morgan Homeroom')
conn = create_db()
morgan_students = select_students_morgan(conn)
morgan_students['DATE'] = dt.datetime.today().strftime('%m/%d/%Y')
hw_cats = ['YES', 'NO', 'ABSENT']
morgan_students['HW_DONE'] = 'YES'
morgan_students['HW_DONE'] = morgan_students['HW_DONE'].astype('category').cat.remove_categories(morgan_students['HW_DONE']).cat.add_categories(hw_cats)
morgan_students['HW_DONE'] = 'YES'
edited_df = st.data_editor(morgan_students, 
                           column_config={'NAME': 'Name', 'DATE': 'Date', 'HW_DONE': st.column_config.SelectboxColumn(label='HW_DONE', options=['YES', 'NO', 'ABSENT'])},
                           disabled=['NAME', 'DATE'])
st.session_state.df = morgan_students
if st.button('Submit'):
    st.session_state.df = edited_df
    print(st.session_state.df)

