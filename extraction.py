# Created by Mayur at 30-06-2022
import os, zipfile
import streamlit as st
import glob

extension = "zip"
flag = False

def extract_zip(path, folders):
    complete_path = []
    filenames = []
    if len(folders) != 0:
        if st.button('Extract'):
            for folder in folders:
                pf = path + '\\' + folder  # change '\\' to '/' in Linux or MacOS
                complete_path.append(pf)

            #st.write(complete_path)

            for cp in complete_path:
                filename = glob.glob(cp + '\\*' + '\\*')  # Change '\\' to '/' in Linux or MacOS
                filenames.append(filename)

            #st.write(filenames)

            for items in filenames:
                for item in items:
                    if extension in item:
                        zip_ref = zipfile.ZipFile(item)
                        zip_ref.extractall(path)
                        zip_ref.close()

            st.write('Extraction Complete')

    else:
        st.write(' ')
        return False
