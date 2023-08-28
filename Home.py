import streamlit as st
import sys
from PIL import Image
import os
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from pages.functions import utils as ut

st.set_page_config('Home')

st.header("Welcome to Miss Morgan's Website!")

#image = Image.open('KMO_PIC.jpg')
#st.image(image)

#conn = ut.create_db()
#ut.drop_student(conn)
#ut.create_student(conn)