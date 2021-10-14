import streamlit as st
from components import *
from data import *

st.set_page_config(
    page_title='ideoscope',
    layout='wide',
    menu_items={
        'Get help': 'https://github.com/paulbricman/ideoscope/issues',
        'Report a Bug': 'https://github.com/paulbricman/ideoscope/issues/new',
        'About': 'https://paulbricman.com/thoughtware/ideoscope'
    })

sidebar_section()

if st.session_state.conceptarium_url == '':
    st.warning('Please introduce the URL of your conceptarium!')
else:
    fetch_conceptarium()
    header_section()

    # memetics
    birth_rate_subsection()
    population_size_subsection()
    variability_subsection()
    drift_subsection()
    fitness_subsection()

    # linguistics
    conciseness_subsection()
    readability_subsection()
    objectivity_subsection()
    sentiment_subsection()
    interests_subsection()

    # semantics
    projection_subsection()
    discovery_subsection()
    footer_section()