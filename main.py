import pandas as pd
import streamlit as st
from random import randint
import time

# Import CDF Parser and Pattern Generator
from cdf_ops.cdf_parser import CdfToDf
from cdf_ops.pattern_generator import PatternFinder

# Configuration file to populate error and keywords
import configparser

# File Download
import base64

# Global Variables for CDF Parser and Pattern Generator
parser = CdfToDf()
pattern = PatternFinder()
MAX_FILES = 5

Page_Config = {'page_title': 'C-ARM Log Analysis',
               'page_icon': '🔍'
               }

st.set_page_config(**Page_Config)


def download_dataframe(dataframe):
    data = dataframe.to_csv()
    b64 = base64.b64encode(data.encode()).decode()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    new_filename = "Structured_CDF_File_{}_.csv".format(timestr)
    st.markdown("#### Download  Structured CDF File ###")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}"> ⏬ Download ⏬ </a>'
    st.markdown(href, unsafe_allow_html=True)


def home():
    state = st.session_state  # Create a local session for Pattern Generation

    st.title('Philips C-Arm Log Analysis')

    # Specific Unique Key for Uploaded File / Files
    if 'FILE_UPLOADER_KEY' not in state:
        state.FILE_UPLOADER_KEY = str(randint(1000, 9999))

    # st.markdown('## \U0001F4C2 Upload CDF files')
    st.markdown('## \U0001F5CE Upload CDF Files')

    # Create a list for holding 5 files
    data = st.file_uploader('', accept_multiple_files=True, type='cdf', key=state.FILE_UPLOADER_KEY)

    # Check if only 5 files are uploaded
    if len(data) > MAX_FILES:
        st.error('Only Five Files Can be Uploaded At A Time. Please Wait 10 Seconds To Reupload Files.')
        time.sleep(10)  # Display Message for 5 seconds
        state.FILE_UPLOADER_KEY = str(randint(1000, 9999))  # Reinitialize Uploaded File Unique Key
        st.experimental_rerun()  # Restart Execution

    # Configuration File with Errors and Keywords
    config = configparser.ConfigParser()
    config.read('keywords.ini')

    # Select Errors One at a Time
    menu = list(config['keywords'].keys())
    error = st.sidebar.selectbox('Select Errors', menu)
    value = config.get('keywords', error)

    # print(value)

    # Submit Selection
    submit = st.button('Submit')

    if submit:
        if len(data) != 0:  # Check if data is not null
            df = parser.convert_all(data)  # Call cdf parser and return dataframe

            if df is not None:  # Check dataframe is empty or not
                try:
                    st.subheader('Structured CDF File')
                    st.dataframe(df)
                    download_dataframe(df)

                    patterns = pattern.find_patterns(df, value)  # Call pattern generator and return pattern
                    if patterns is not None:
                        st.subheader('Pattern For {}', error)
                        st.dataframe(patterns)  # Display Patterns

                    else:
                        st.warning('Selected Patterns Not Found.')

                    # if st.button("Save"):
                    # st.write(df)
                    # text_download(my_text)
                except:
                    st.write(' ')
            else:
                st.write(' ')

        else:
            st.error('Please Upload Required Files.')


if __name__ == '__main__':
    home()
