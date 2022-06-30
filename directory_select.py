# Created by Mayur at 30-06-2022
import streamlit as st
import os

folders = []
folders_path = []
files = []


def directory(path):
    complete_path = []
    selected_folders = []

    if st.button('Submit Path'):
        for dp, dirname, filename in os.walk(path):
            folders_path.append(dp)
            folders.append(dirname)
            files.append(filename)

    if len(selected_folders) is 0:
        try:
            selected_folders = st.multiselect('Select Folders', folders[0])
            return selected_folders
        except:
            st.write(' ')
            return None

        # for fp in selected_folders:
        #     complete_path_sf = path + '\\' + fp
        #     complete_path.append(complete_path_sf)
