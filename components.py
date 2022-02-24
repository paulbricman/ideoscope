import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
import streamlit as st
from data import *


def sidebar_section():
    st.sidebar.header('settings')
    st.session_state['conceptarium_url'] = st.sidebar.text_input(
        'conceptarium URL')
    st.session_state['access_token'] = st.sidebar.text_input(
        'access token', type='password')


def header_section():
    st.title('🔬 ideoscope.')
    st.markdown(
        'An instrument for quantifying, understanding, and optimizing your thinking, split into three sections:')

    col1, col2, col3 = st.columns(3)
    col1.markdown('''#### 🌿 memetics
    - 🐣 birth rate
    - 🐇 population size
    - 🐋 variability
    - 🍃 drift
    - 🦅 fitness
    ''')
    col2.markdown('''#### 📗 linguistics
    - ⏱️ conciseness
    - 📰 readability
    - 📏 objectivity
    - 💚 sentiment
    - 🎨 interests
    ''')
    col3.markdown('''#### 🖼️ semantics
    - 🌌 projection
    - 🔭 discovery
    ''')

    hide_streamlit_style = '''
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                '''
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def birth_rate_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🐣 birth rate')
    st.caption('The rate at which new ideas get saved to your conceptarium.')

    col1, col2, col3, col4 = st.columns(4)

    value, delta = birth_rate_over_past_day()
    col1.metric(label='birth rate over past day', value=value, delta=delta)

    value, delta = birth_rate_over_past_week()
    col2.metric(label='birth rate over past week', value=value, delta=delta)

    value, delta = birth_rate_over_past_month()
    col3.metric(label='birth rate over past month', value=value, delta=delta)

    value, delta = birth_rate_over_past_year()
    col4.metric(label='birth rate over past year', value=value, delta=delta)

    col1, col2 = st.columns(2)

    data = daily_birth_rate()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='daily birth rate', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='days ago', autorange='reversed')
    fig.update_yaxes(title_text='birth rate')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = birth_rate_by_day_of_week()
    fig = px.histogram(data, x='weekday', nbins=12, color_discrete_sequence=['#228b22'], category_orders={
                       'weekday': calendar.day_abbr[0:7]}, title='birth rate by day of the week')
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(title_text='day of the week')
    fig.update_yaxes(title_text='birth rate')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)

    data = birth_rate_by_time_of_day()
    fig = px.histogram(data, nbins=12, color_discrete_sequence=[
                       '#228b22'], title='birth rate by time of day')
    fig.update_layout(bargap=0.2, showlegend=False)
    fig.update_xaxes(title_text='time of day', tickformat='%H:%M')
    fig.update_yaxes(title_text='birth rate')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = birth_rate_by_time_of_day_and_day_of_week()
    fig = px.density_heatmap(data, x='weekday', y='time', category_orders={'weekday': calendar.day_abbr[0:7]}, color_continuous_scale=[
                             '#fffffd', '#228b22'], title='birth rate by day of the week and time of day')
    fig.update_layout(bargap=0.2, xaxis={'side': 'top'})
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='time of day',
                     autorange='reversed', tickformat='%H:%M')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def population_size_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🐇 population size')
    st.caption(
        'A measure of how large the ecology of your mind is in terms of individual thoughts.')

    col1, col2 = st.columns(2)

    data = population_size_per_day()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='population size per day', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='days ago', autorange='reversed')
    fig.update_yaxes(title_text='population size')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = population_pyramid_of_fittest_quartile()
    layout = go.Layout(yaxis=go.layout.YAxis(title='age (weeks)', showline=True, linewidth=1, linecolor='#474539', mirror=True),
                       xaxis=go.layout.XAxis(range=[-1.2 * np.amax(data[0] + data[1]), 1.2 * np.amax(
                           data[0] + data[1])], title='count', showline=True, linewidth=1, linecolor='#474539', mirror=True),
                       barmode='overlay',
                       bargap=0.1,
                       title='population pyramid of fittest quartile')
    data = [go.Bar(x=np.multiply(-1, data[0]),
                   y=list(range(len(data[0]))),
                   orientation='h',
                   name='text',
                   hoverinfo='x',
                   marker=dict(color='#42D142')),
            go.Bar(x=data[1],
                   y=list(range(len(data[1]))),
                   orientation='h',
                   name='image',
                   hoverinfo='x',
                   marker=dict(color='seagreen'))]

    col2.plotly_chart(dict(data=data, layout=layout))


def variability_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🐋 variability')
    st.caption(
        'A measure of how diverse your thinking is at any given time, the biodiversity of your ideas.')

    col1, col2, col3, col4 = st.columns(4)

    value, delta = variability_over_past_week()
    col1.metric(label='variability over past week', value=value, delta=delta)

    value, delta = variability_over_past_month()
    col2.metric(label='variability over past month', value=value, delta=delta)

    value = aggregate_variability()
    col3.metric(label='aggregate variability', value=value)

    value = variability_of_fittest_quartile()
    col4.metric(label='variability of fittest quartile', value=value)

    col1, col2 = st.columns(2)

    data = variability_per_week()
    fig = px.line(data, x='age', y='variability', color_discrete_sequence=[
                  '#228b22'], title='variability per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='variability')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = variability_per_month()
    fig = px.line(data, x='age', y='variability', color_discrete_sequence=[
                  '#228b22'], title='variability per month', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='months ago', autorange='reversed')
    fig.update_yaxes(title_text='variability')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def drift_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🍃 drift')
    st.caption(
        'A measure of how much you\'re shifting your focus from one period to the next.')

    col1, col2, col3, col4 = st.columns(4)

    value, delta = drift_over_past_week()
    col1.metric(label='drift over past week', value=value, delta=delta)

    value, delta = drift_over_past_week_percent_of_max()
    col2.metric(label='drift over past week (% of max)',
                value=value, delta=delta)

    value, delta = drift_over_past_month()
    col3.metric(label='drift over past month', value=value, delta=delta)

    value, delta = drift_over_past_month_percent_of_max()
    col4.metric(label='drift over past month (% of max)',
                value=value, delta=delta)

    col1, col2 = st.columns(2)

    data = drift_per_week()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='drift per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='drift')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = drift_per_month()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='drift per month', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='months ago', autorange='reversed')
    fig.update_yaxes(title_text='drift')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def fitness_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🦅 fitness')
    st.caption('The fitness of a thought is equated with how active it is in your mind. Powerful, catchy, gripping ideas are the ones on which you reflect most.')

    col1, col2, col3, col4 = st.columns(4)

    value = mean_fitness()
    col1.metric(label='mean fitness', value=value)

    value = fitness_interquartile_mean()
    col2.metric(label='fitness interquartile mean', value=value)

    value = fitness_interquartile_range()
    col3.metric(label='fitness interquartile range', value=value)

    value = memetic_load()
    col4.metric(label='memetic load', value=value)

    col1, col2 = st.columns(2)

    data = fitness_distribution()
    fig = px.histogram(data, nbins=50, color_discrete_sequence=[
                       '#228b22'], title='fitness distribution')
    fig.update_layout(bargap=0.2, showlegend=False)
    fig.update_xaxes(title_text='fitness')
    fig.update_yaxes(title_text='thought count')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = fitness_distribution()
    fig = px.box(data, color_discrete_sequence=[
                 '#228b22'], title='fitness distribution')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='fitness')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def conciseness_subsection():
    st.markdown('---')
    st.header('📗 linguistics / ⏱️ conciseness')
    st.caption('The average reading time of text thoughts in seconds based on average reading speed (lower is more concise).')

    col1, col2 = st.columns(2)

    data = conciseness_per_week()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='conciseness per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='average reading time (seconds)')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = conciseness_distribution_over_past_month()
    fig = px.box(data, color_discrete_sequence=[
                 '#228b22'], title='conciseness distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='reading time (seconds)')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def readability_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 📰 readability')
    st.caption('The Flesch-Kincaid grade level is an estimate for how many years of formal education one needs to understand a text.')

    col1, col2 = st.columns(2)

    data = readability_per_week()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='readability per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='Flesch-Kincaid grade level')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = readability_distribution_over_past_month()
    fig = px.box(data, color_discrete_sequence=[
                 '#228b22'], title='readability distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='Flesch-Kincaid grade level')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def objectivity_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 📏 objectivity')
    st.caption(
        'A measure of how much your text thoughts appear to describe facts, rather than opinions.')

    col1, col2 = st.columns(2)

    data = objectivity_per_week()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='objectivity per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='objectivity')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = objectivity_distribution_over_past_month()
    fig = px.box(data, color_discrete_sequence=[
                 '#228b22'], title='objectivity distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='objectivity')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def sentiment_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 💚 sentiment')
    st.caption('A measure of how positive your text thoughts are.')

    col1, col2 = st.columns(2)

    data = sentiment_per_week()
    fig = px.line(data, color_discrete_sequence=[
                  '#228b22'], title='sentiment per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='sentiment')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = sentiment_distribution_over_past_month()
    fig = px.box(data, color_discrete_sequence=[
                 '#228b22'], title='sentiment distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='sentiment')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def interests_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 🎨 interests')
    st.caption('Keywords derived from your text thoughts.')

    col1, col2 = st.columns(2)

    data = interests()
    fig = px.timeline(data, x_start='start', x_end='end', y='keyword', color_discrete_sequence=[
                      '#228b22'], text='keyword', title='timeline of interests')
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='', showticklabels=False)
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)

    col1.plotly_chart(fig)

    fig = px.bar(data, x='keyword', y='count', color_discrete_sequence=[
                 '#228b22'], title='thoughts by interest')
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='count')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def projection_subsection():
    st.markdown('---')
    st.header('🖼️ semantics / 🌌 projection')
    st.caption(
        'Low-dimensional visualizations of the high-dimensional semantics of your thoughts.')

    col1, col2 = st.columns(2)

    data = projection_2d()
    fig = px.scatter(data, x='x', y='y', hover_data=[
                     'modality', 'content'], color_discrete_sequence=['#228b22'], title='2D projection')
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0))
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = projection_3d()
    fig = px.scatter_3d(data, x='x', y='y', z='z', hover_data=[
                        'modality', 'content'], size='size', size_max=5, color_discrete_sequence=['#228b22'], title='3D projection')
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0))
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def discovery_subsection():
    st.markdown('---')
    st.header('🖼️ semantics / 🔭 discovery')
    st.caption(
        'A measure of how much of the semantic space you\'ve explored through your ideas.')

    col1, col2, col3, col4 = st.columns(4)

    data = [explored_portion_of_semantic_space()]
    data += [discovery_per_thought(data[0]['value'][0])]
    data += [(1 - data[0]['value'][0]) / data[1]]
    data += [(1 - data[0]['value'][0]) / data[0]
             ['value'][0] * conceptarium_age()]

    col1.metric(label='explored proportion of semantic volume',
                value='{:.3f}'.format(data[0]['value'][0] * 100) + '%')
    col2.metric(label='mean dicovery rate per thought',
                value='{:.5f}'.format(data[1] * 100) + '%')
    col3.metric(label='estimated thoughts left for full coverage',
                value=int(data[2]))
    col4.metric(label='ETA full coverage', value=f'{data[3]:.2f}' + ' YRS')

    col1, col2 = st.columns(2)

    fig = px.pie(data[0], names='name', values='value', color_discrete_sequence=[
                 '#228b22'], title='explored portion of semantic space')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='weekly discovery rates')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = energy_spectrum()
    fig = px.bar(data, color_discrete_sequence=[
                 '#228b22'], title='PCA energy spectrum')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='principal component')
    fig.update_yaxes(title_text='explained variance ratio')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def footer_section():
    footer = '''
    ---
    <style>
    button {
        border: 4px solid;
        border-color: #228b22;
        border-radius: 4px;
        background-color: #228b22;
        color: #fffffd;
        font-weight: bold;
        padding-left: 5px;
        padding-right: 5px;
    }
    </style>
    <center>
        <div>
            <a href="https://paulbricman.com/contact"><button>send feedback</button></a>
            <a href="https://github.com/paulbricman/ideoscope"><button>learn more</button></a>
            <a href="https://github.com/sponsors/paulbricman"><button>support me 🤍</button></a>
        </div>
    </center>
    '''

    st.markdown(footer, unsafe_allow_html=True)
