import streamlit as st
import datetime as dt
import sys
import time
from pages.functions import utils as ut
from streamlit_extras.switch_page_button import switch_page

st.set_page_config('Morgan Homeroom')
st.sidebar.header('Morgan Homeroom')
conn = ut.create_db()
morgan_students = ut.select_students_morgan(conn)
morgan_students['DATE'] = dt.datetime.today().strftime('%m/%d/%Y')
hw_cats = ['YES', 'NO', 'ABSENT']
morgan_students['HW_DONE'] = 'YES'
morgan_students['HW_DONE'] = (morgan_students['HW_DONE'].astype('category')
                                                        .cat
                                                        .remove_categories(morgan_students['HW_DONE'])
                                                        .cat
                                                        .add_categories(hw_cats)
)
morgan_students['HW_DONE'] = 'YES'
edited_df = st.data_editor(morgan_students, 
                           column_config={'NAME': 'Name', 
                                          'DATE': 'Date', 
                                          'HW_DONE': st.column_config.SelectboxColumn(label='HW_DONE', 
                                                                                      options=['YES', 'NO', 'ABSENT'])},
                           disabled=['NAME', 'DATE']
)
st.session_state.df = morgan_students
submit = st.button('Submit')
if submit:
    st.session_state.df = edited_df
    st.write('Submitted!')
    data = list(zip(st.session_state.df['NAME'], 
                    st.session_state.df['DATE'], 
                    st.session_state.df['HW_DONE'])
    )
    for row in data:
        ut.insert_hw(conn, row)
    time.sleep(3)
    switch_page('Home')