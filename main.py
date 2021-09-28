import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import datetime
import calendar

st.header('🔬 overview')
st.caption(
    'Glimpse into your thought patterns through a curated list of high-level indicators.')

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Ideogenesis", value="54", delta="+3")
col2.metric(label="Variability", value="3.9", delta="-1.7")
col3.metric(label="Drift", value="7.2", delta="+2.3")
col4.metric(label="Load", value="1.2",
            delta="-3.9", delta_color='inverse')

col1.metric(label="Population Size", value="430", delta="+34")
col2.metric(label="Discovery Rate", value="0.23%", delta="+0.02%")
col3.metric(label="Objectivity", value="8.4", delta="-0.3")
col4.metric(label="Fitness", value="6.2", delta="-1.2")

st.markdown('---')
st.header('🌱 memetics')
st.caption(
    'Understand how the ecology of your mind is evolving, so that you can then optimally nurture it.')

col1, col2 = st.columns(2)

ideogenesis_by_hour = pd.DataFrame(
    np.random.normal(1600, 200, 24))
fig = px.histogram(ideogenesis_by_hour, nbins=12, color_discrete_sequence=[
    '#228b22'], labels={'count': '', 'Time': ''}, title='ideogenesis by hour')
fig.update_layout(bargap=0.2, showlegend=False)
col1.plotly_chart(fig)

ideogenesis_by_weekday = np.random.choice(calendar.day_abbr[0:7], 400)
df = pd.DataFrame(ideogenesis_by_weekday, columns=['Time'])
fig = px.histogram(df, x='Time', nbins=12, color_discrete_sequence=[
    '#228b22'], labels={'count': '', 'Time': ''}, title='ideogenesis by weekday', category_orders={'Time': calendar.day_abbr[0:7]})
fig.update_layout(bargap=0.2)
col2.plotly_chart(fig)

ideogenesis_by_month = np.random.choice(calendar.month_abbr[1:13], 400)
df = pd.DataFrame(ideogenesis_by_month, columns=['Time'])
fig = px.histogram(df, x='Time', nbins=12, color_discrete_sequence=[
    '#228b22'], labels={'count': '', 'Time': ''}, title='ideogenesis by month', category_orders={'Time': calendar.month_abbr[1:13]})
fig.update_layout(bargap=0.2)
col1.plotly_chart(fig)

ideogenesis_per_day = np.random.randint(100, 200, (100))
fig = px.line(ideogenesis_per_day, color_discrete_sequence=[
    '#228b22'], title='ideogenesis per day')
fig.update_layout(showlegend=False)
col2.plotly_chart(fig)

st.markdown('---')

option = st.sidebar.text_input(
    'What\'s the URL of your conceptarium?')
