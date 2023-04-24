'''

import streamlit as st
from PIL import Image



bg_image = Image.open("B_Image1.jpg")
st.markdown("""
            <style>
            .css-9s5bis.edgvbvh3
            {
                visibility:hidden;
                }
            .css-h5rgaw.egzxvld1
            {
                visibility:hidden;
                }
            body {
                background-image: url('C:\\Users\Shiva\Documents\Data Science\Projects\Currency Exchange Prediction\B_Image1.jpg');
                background-size: cover;
                }
            
            </style>
            """,unsafe_allow_html=True)

t1,t2,t3=st.columns(3)
t2.title("Currency_Exchange")
st.write("---")
ind,tit,usa=st.columns(3)
ind.image("India_flag.jpg")
tit.header("$USD - ₹INR")
usa.image("flag.jpg")
'''

import streamlit as st
from PIL import Image
import base64

# Load background image
try:
    bg_image = Image.open("C:\\Users\Shiva\Documents\Data Science\Projects\Currency Exchange Prediction\B_Image.jpg")
except IOError:
    st.error("Error: Image not found or could not be opened. Please check the file path and format.")
    st.stop()

# Set page configuration to display background image
st.set_page_config(page_title="My Streamlit App", page_icon=":smiley:", layout="wide", initial_sidebar_state="expanded")
try:
    page_bg = '''
    <style>
    body {
    background-image: url("C:\\Users\Shiva\Documents\Data Science\Projects\Currency Exchange Prediction\B_Image.jpg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % base64.b64encode(bg_image.tobytes()).decode()
except AttributeError:
    st.error("Error: Image could not be encoded in base64. Please check the file format.")
    st.stop()
st.markdown(page_bg, unsafe_allow_html=True)

# Write your Streamlit app
st.title("My Streamlit App")
st.write("Welcome to my app!")
