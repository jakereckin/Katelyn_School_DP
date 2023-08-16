import streamlit as st
import sys
from PIL import Image

st.set_page_config('Home')

st.header("Welcome to Miss Morgan's Website!")

image = Image.open('KMO_PIC.jpg')
st.image(image)