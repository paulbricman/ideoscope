import calendar
from numpy import empty
import streamlit as st
import requests
import json
import pandas as pd
from time import time as now
from datetime import datetime, date, tzinfo, time
from pytz import timezone
import math


def fetch_conceptarium():
    # conceptarium_url = st.session_state.conceptarium_url
    # if conceptarium_url[-1] != '/':
    #    conceptarium_url += '/'
    #
    # conceptarium_url += 'find/lang/json?content=irrelevant&top_k=10&silent=True'
    # conceptarium_json = requests.get(conceptarium_url).json()
    # st.session_state.conceptarium_json = conceptarium_json
    st.session_state.conceptarium_json = json.load(open('dummy.json'))


def birth_rate_over_past_day():
    data = daily_birth_rate()
    return data[0], data[0] - data[1]


def birth_rate_over_past_week():
    data = daily_birth_rate()
    return sum(data[:7]), sum(data[:7]) - sum(data[7:14])


def birth_rate_over_past_month():
    data = daily_birth_rate()
    return sum(data[:30]), sum(data[:30]) - sum(data[30:60])


def birth_rate_over_past_year():
    data = daily_birth_rate()
    return sum(data[:365]), sum(data[:365]) - sum(data[365:2 * 365])


def daily_birth_rate():
    conceptarium_json = st.session_state.conceptarium_json
    timestamps = pd.DataFrame(conceptarium_json)['timestamp'].values
    midnight = datetime.combine(datetime.today(), time.min).timestamp()
    
    timestamps = [midnight - e for e in timestamps]
    timestamps = [int(1 + e / (60 * 60 * 24)) for e in timestamps]
    timestamps = sorted(timestamps)
    data = [timestamps.count(e) for e in range(max(timestamps) + 1)]
    return data

    
def birth_rate_by_day_of_week():
    conceptarium_json = st.session_state.conceptarium_json
    timestamps = pd.DataFrame(conceptarium_json)['timestamp'].values

    data = [date.fromtimestamp(e).strftime('%a') for e in timestamps]
    return pd.DataFrame(data, columns=['weekday'])


def birth_rate_by_time_of_day():
    conceptarium_json = st.session_state.conceptarium_json
    timestamps = pd.DataFrame(conceptarium_json)['timestamp'].values

    data = [datetime.fromtimestamp(e, tz=timezone(st.session_state.timezone)).strftime('%H:%M') for e in timestamps]
    data = pd.to_datetime(data, format='%H:%M')
    return pd.DataFrame(data, columns=['time'])


def birth_rate_by_time_of_day_and_day_of_week():
    time = birth_rate_by_time_of_day()
    weekday = birth_rate_by_day_of_week()

    data = pd.DataFrame()
    data['time'] = time['time'].values
    data['weekday'] = weekday['weekday'].values
    return data


def population_size_per_day():
    data = daily_birth_rate()
    data = [sum(data[e:]) for e in range(len(data))]
    return data


def population_pyramid_of_fittest_quartile():
    conceptarium_json = st.session_state.conceptarium_json
    conceptarium_json = sorted(conceptarium_json, key=lambda x: x['activation'])
    fittest = conceptarium_json[:math.ceil(len(conceptarium_json) * 0.25)]

    fittest_language = [e for e in fittest if e['modality'] == 'language']
    fittest_imagery = [e for e in fittest if e['modality'] == 'imagery']

    if len(fittest_language) > 0:
        fittest_language_age = [int((now() - e['timestamp']) / (60 * 60 * 24 * 7)) for e in fittest_language]
        fittest_language_age = [fittest_language_age.count(e) for e in range(max(fittest_language_age) + 1)]
    else:
        fittest_language_age = []

    if len(fittest_imagery) > 0:
        fittest_imagery_age = [int((now() - e['timestamp']) / (60 * 60 * 24 * 7)) for e in fittest_imagery]
        fittest_imagery_age = [fittest_imagery_age.count(e) for e in range(max(fittest_imagery_age) + 1)]
    else:
        fittest_imagery_age = []

    return fittest_language_age, fittest_imagery_age