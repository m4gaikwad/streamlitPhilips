import streamlit as st
import time
import base64
import pandas as pd

def structured_cdf(dataframe):
    data = dataframe.to_csv()
    b64 = base64.b64encode(data.encode()).decode()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    new_filename = "Structured_CDF_File_{}_.csv".format(timestr)
    st.markdown("#### Download  Structured CDF File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}"> ⏬ Download ⏬ </a>'
    st.markdown(href, unsafe_allow_html=True)