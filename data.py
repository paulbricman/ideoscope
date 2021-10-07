import streamlit as st
import requests
import json


def fetch_conceptarium():
    # conceptarium_url = st.session_state.conceptarium_url
    # if conceptarium_url[-1] != '/':
    #    conceptarium_url += '/'
    #
    # conceptarium_url += 'find/lang/json?content=irrelevant&top_k=10&silent=True'
    # conceptarium_json = requests.get(conceptarium_url).json()
    # st.session_state.conceptarium_json = conceptarium_json
    st.session_state.conceptarium_json = json.load(open('dummy.json'))