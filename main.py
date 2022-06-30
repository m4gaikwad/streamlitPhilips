import pandas as pd
import streamlit as st
from random import randint
import time

# Import CDF Parser, Pattern Generator and Download
from cdf_ops.cdf_parser import CdfToDf
from cdf_ops.pattern_generator import PatternFinder

# Import file with method to download structured cdf files
from cdf_ops.download import structured_cdf

import directory_select as ds
import extraction as ext
# Configuration file to populate error and keywords
import configparser

# Global Variables for CDF Parser and Pattern Generator
parser = CdfToDf()
pattern = PatternFinder()
MAX_FILES = 5

Page_Config = {'page_title': 'C-ARM Log Analysis',
               'page_icon': '🔍'
               }

st.set_page_config(**Page_Config)


def home():
    selected_folders = []
    state = st.session_state  # Create a local session for Pattern Generation

    st.title('Philips C-Arm Log Pattern Generator')  # Project Title

    #Select Process
    process = ['Directory','CSV']
    select_menu = st.sidebar.selectbox('Select Step',process)

    # Configuration File with Errors and Keywords
    config = configparser.ConfigParser()
    config.read('keywords.ini')

    # Select Errors One at a Time
    menu = list(config['keywords'].keys())
    error = st.sidebar.selectbox('Select Errors', menu)
    value = config.get('keywords', error)

    if select_menu == 'CSV':
        # Specific Unique Key for Uploaded File / Files
        if 'FILE_UPLOADER_KEY' not in state:
            state.FILE_UPLOADER_KEY = str(randint(1000, 9999))



        # st.markdown('## \U0001F4C2 Upload CDF files')
        st.markdown('## \U0001F5CE Upload CDF Files')

        # Create a list for holding 5 files
        data = st.file_uploader('', accept_multiple_files=True, type='cdf', key=state.FILE_UPLOADER_KEY)

        # Check if only 5 files are uploaded
        # if len(data) > MAX_FILES:
        #     st.error('Only Five Files Can be Uploaded At A Time. Please Wait 10 Seconds To Reupload Files.')
        #     time.sleep(10)  # Display Message for 5 seconds
        #     state.FILE_UPLOADER_KEY = str(randint(1000, 9999))  # Reinitialize Uploaded File Unique Key
        #     st.experimental_rerun()  # Restart Execution


        # print(value)

        # Submit Selection
        submit = st.button('Submit')

        if submit:
            if len(data) != 0:  # Check if data is not null
                df = parser.convert_all(data)  # Call cdf parser and return dataframe

                if df is not None:  # Check dataframe is empty or not
                    try:
                        # st.subheader('Structured CDF File')
                        # st.dataframe(df)
                        structured_cdf(df)

                        patterns = pattern.find_patterns(df, value)  # Call pattern generator and return pattern

                        if patterns is not None:
                            st.subheader('Pattern For {}', error)
                            st.dataframe(patterns)  # Display Patterns
                            # structured_cdf(pd.DataFrame.from_dict(patterns))

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
    elif select_menu == 'Directory':
        # Select Directory Code

        path = st.text_input('Type Complete Path till Test1 Directory')

        selected_folders = ds.directory(path)

        try:
            ext.extract_zip(path, selected_folders)
        except:
            st.write(' ')
    else:
        st.write(' ')

if __name__ == '__main__':
    home()
