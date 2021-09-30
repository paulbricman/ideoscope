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

col1.metric(label='Ideogenesis', value='54', delta='+3')
col2.metric(label='Variability', value='3.9', delta='-1.7')
col3.metric(label='Drift', value='7.2', delta='+2.3')
col4.metric(label='Load', value='1.2',
            delta='-3.9', delta_color='inverse')

col1.metric(label='Population Size', value='430', delta='+34')
col2.metric(label='Discovery Rate', value='0.23%', delta='+0.02%')
col3.metric(label='Objectivity', value='8.4', delta='-0.3')
col4.metric(label='Fitness', value='6.2', delta='-1.2')

st.markdown('---')
st.header('🌱 ideogenesis')
st.caption('This is the rate at which you save new ideas to your conceptarium.')
col1, col2, col3, col4 = st.columns(4)

col1.metric(label='ideogenesis over past day', value='12', delta='+3')
col2.metric(label='ideogenesis over past week', value='54', delta='+7')
col3.metric(label='ideogenesis over past month', value='230', delta='-2')
col4.metric(label='population size', value='460')

col1, col2 = st.columns(2)

ideogenesis_per_day = np.random.randint(100, 200, (100))
fig = px.line(ideogenesis_per_day, color_discrete_sequence=[
    '#228b22'], title='ideogenesis per day')
fig.update_layout(showlegend=False)
fig.update_xaxes(title_text='days ago', autorange='reversed')
fig.update_yaxes(title_text='ideogenesis')
col1.plotly_chart(fig)

ideogenesis_by_day_of_the_week = np.random.choice(calendar.day_abbr[0:7], 400)
df = pd.DataFrame(ideogenesis_by_day_of_the_week, columns=['Time'])
fig = px.histogram(df, x='Time', nbins=12, color_discrete_sequence=[
    '#228b22'], labels={'count': '', 'Time': ''}, category_orders={'Time': calendar.day_abbr[0:7]}, title='ideogenesis by day of the week')
fig.update_layout(bargap=0.2)
fig.update_xaxes(title_text='day of the week')
fig.update_yaxes(title_text='ideogenesis')
col2.plotly_chart(fig)

ideogenesis_by_time_of_day = pd.DataFrame(
    np.random.normal(1600, 200, 400))
fig = px.histogram(ideogenesis_by_time_of_day, nbins=12, color_discrete_sequence=[
    '#228b22'], labels={'count': '', 'Time': ''}, title='ideogenesis by time of day')
fig.update_layout(bargap=0.2, showlegend=False)
fig.update_xaxes(title_text='time of day')
fig.update_yaxes(title_text='ideogenesis')
col1.plotly_chart(fig)

ideogenesis_by_month = np.random.choice(calendar.month_abbr[1:13], 400)
df = pd.DataFrame([e for e in zip(ideogenesis_by_day_of_the_week, np.random.normal(1600, 200, 400))],
                  columns=['weekday', 'hour'])
fig = px.density_heatmap(df, x='weekday', y='hour', category_orders={
    'weekday': calendar.day_abbr[0:7]}, color_continuous_scale=['#fffffd', '#228b22'], title='ideogenesis by day of the week and time of day')
fig.update_layout(bargap=0.2, xaxis={'side': 'top'})
fig.update_xaxes(title_text='')
fig.update_yaxes(title_text='time of day', autorange='reversed')
col2.plotly_chart(fig)

st.markdown('---')
st.header('🐋 memetic variability')
st.caption('This is a measure of how diverse your thinking is at any given time, a measure of the biodiversity of your ideas.')
col1, col2, col3, col4 = st.columns(4)

col1.metric(label='memetic variability over past week', value='54', delta='+7')
col2.metric(label='memetic variability over past month',
            value='230', delta='-2')
col3.metric(label='aggregate memetic variability', value='12')
col4.metric(label='memetic variability of fittest quartile', value='12')


col1, col2 = st.columns(2)
memetic_variability_per_week = np.random.uniform(5, 3, (20))
fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
    '#228b22'], title='memetic variability per week')
fig.update_layout(showlegend=False)
fig.update_xaxes(title_text='weeks ago', autorange='reversed')
fig.update_yaxes(title_text='memetic variability')
col1.plotly_chart(fig)

memetic_variability_per_month = np.random.uniform(5, 3, (5))
fig = px.line(memetic_variability_per_month, color_discrete_sequence=[
    '#228b22'], title='memetic variability per month')
fig.update_layout(showlegend=False)
fig.update_xaxes(title_text='months ago', autorange='reversed')
fig.update_yaxes(title_text='memetic variability')
col2.plotly_chart(fig)

st.markdown('---')
st.header('⚓ memetic drift')
st.caption(
    'This is a measure of how much you\'re shifting your focus from one period to the next.')
col1, col2, col3, col4 = st.columns(4)

col1.metric(label='memetic drift over past week', value='54', delta='+7')
col2.metric(label='memetic drift over past week (% of max)',
            value='12%', delta='3%')
col3.metric(label='memetic drift over past month',
            value='230', delta='-2')
col4.metric(label='memetic drift over past month (% of max)',
            value='12', delta='3%')


col1, col2 = st.columns(2)
memetic_variability_per_week = np.random.uniform(5, 3, (20))
fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
    '#228b22'], title='memetic drift per week')
fig.update_layout(showlegend=False)
fig.update_xaxes(title_text='weeks ago', autorange='reversed')
fig.update_yaxes(title_text='memetic drift')
col1.plotly_chart(fig)

memetic_variability_per_month = np.random.uniform(5, 3, (5))
fig = px.line(memetic_variability_per_month, color_discrete_sequence=[
    '#228b22'], title='memetic drift per month')
fig.update_layout(showlegend=False)
fig.update_xaxes(title_text='months ago', autorange='reversed')
fig.update_yaxes(title_text='memetic drift')
col2.plotly_chart(fig)

st.markdown('---')
st.header('🏅 memetic fitness')
st.caption(
    'The fitness of a thought is equated with how active it is in your mind. Powerful, catchy, gripping ideas are the ones on which you reflect most.')
col1, col2, col3, col4 = st.columns(4)

col1.metric(label='mean memetic fitness', value='54', delta='+7')
col2.metric(label='median memetic fitness',
            value='12%', delta='3%')
col3.metric(label='mean age of fittest quartile',
            value='230', delta='-2')
col4.metric(label='memetic load',
            value='12', delta='3%')


col1, col2 = st.columns(2)
memetic_fitness = pd.DataFrame(
    np.random.normal(20, 10, 400))
fig = px.histogram(memetic_fitness, nbins=50, color_discrete_sequence=[
    '#228b22'], labels={'count': '', 'Time': ''}, title='memetic fitness distribution')
fig.update_layout(bargap=0.2, showlegend=False)
fig.update_xaxes(title_text='memetic fitness')
fig.update_yaxes(title_text='thought count')
col1.plotly_chart(fig)

memetic_fitness = pd.DataFrame(
    np.random.randint(0, 100, 100))
fig = px.histogram(memetic_fitness, nbins=20, color_discrete_sequence=[
    '#228b22'], labels={'count': '', 'Time': ''}, title='genesis of fittest quartile (days)')
fig.update_layout(bargap=0.2, showlegend=False)
fig.update_xaxes(title_text='days ago', autorange='reversed')
fig.update_yaxes(title_text='thought count')
col2.plotly_chart(fig)

st.markdown('---')

option = st.sidebar.text_input(
    'What\'s the URL of your conceptarium?')

option = st.sidebar.number_input(
    'What timezone are you in? (UTC+...)', step=1)
