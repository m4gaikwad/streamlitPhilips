# Created by Mayur at 30-06-2022
import os, zipfile
import streamlit as st
import glob

extension = '.zip'


def extract_zip(path, folders):
    complete_path = []
    filenames = []
    if len(folders) != 0:
        if st.button('Extract'):
            for folder in folders:
                pf = path + '\\' + folder
                complete_path.append(pf)

            for cp in complete_path:
                filename = glob.glob(cp + '\\*')
                filenames.append(filename)
            #st.write(filenames)

    for item in filenames:
        if extension in item[0]:
            zip_ref = zipfile.ZipFile(item[0])
            zip_ref.extractall(path)
            zip_ref.close()

    else:
        st.write(' ')
