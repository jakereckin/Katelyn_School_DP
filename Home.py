import streamlit as st
import sys
from PIL import Image
import os
import pandas as pd
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from pages.functions import utils as ut


st.set_page_config('Home')

st.header("Welcome to Miss Morgan's Website!")

image = Image.open('KMO_PIC.jpg')
st.image(image)

conn = ut.create_db()
password = st.text_input(label='Miss Morgan Only')
if password=='KesmNov15':
    with open("NDA_BB.db", "rb") as fp:
        btn = st.download_button(
                label="Download DB File",
                data=fp,
                file_name="km013.db",
                mime="application/octet-stream"
            )

def run_insert():
    conn = ut.create_db()
    ut.drop_hw(conn)
    ut.create_hw(conn)
    data = pd.read_csv(r'C:\Users\Jake\Downloads\All_Data.csv')
    this = list(zip(data['NAME'], 
                     data['HW_DATE'], 
                     data['HW_DONE'])
                )
    for row in this:
        ut.insert_hw(conn, row)
