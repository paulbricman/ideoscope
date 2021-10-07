import streamlit as st
from components import *

st.set_page_config(
    page_title='ideoscope',
    layout='wide',
    menu_items={
        'Get help': 'https://github.com/paulbricman/ideoscope/issues',
        'Report a Bug': 'https://github.com/paulbricman/ideoscope/issues/new',
        'About': 'https://paulbricman.com/thoughtware/ideoscope'
    })

# meta
sidebar()
header()

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
discovery_subsection()
projection_subsection()
