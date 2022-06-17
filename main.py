# This is a sample Python script.
import streamlit as st
from random import randint
import time
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from cdf_ops.cdf_parser import CdfToDf
from cdf_ops.pattern_generator import PatternFinder

parser = CdfToDf()
pattern = PatternFinder()
MAX_FILES = 5


def home():
    state = st.session_state
    st.title('Philips Log Analysis')

    if 'FILE_UPLOADER_KEY' not in state:
        state.FILE_UPLOADER_KEY = str(randint(1000, 9999))

    #st.markdown('## \U0001F4C2 Upload CDF files')
    st.markdown('## \U0001F5CE Upload CDF Files')

    data = st.file_uploader('', accept_multiple_files=True, type='cdf', key=state.FILE_UPLOADER_KEY)

    if len(data) > 5:
        st.error('Only Five Files Can be Uploaded At A Time. Please Wait 5 Seconds To Reupload Files.')
        time.sleep(5)
        state.FILE_UPLOADER_KEY = str(randint(1000, 9999))
        st.experimental_rerun()

    error = st.sidebar.selectbox('Select Errors', ['X_ray Generator', 'Hot Tank Oil'])
    submit = st.button('Submit')
    #print(data)

    if submit:
        if len(data) != 0:
            df = parser.convert_all(data)
            patterns = pattern.find_patterns(df, error=error)
            if patterns is None:
                st.info('Selected Patterns Found.')
            else:
                st.dataframe(patterns)
        else:
            st.error('Please Upload Required Files.')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    home()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
