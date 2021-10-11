from typing import Text
import numpy as np
import streamlit as st
import json
import pandas as pd
from time import time as now
from datetime import datetime, date, time
from pytz import timezone
import math
from util import cos_dist, syllable_count
import re
from textblob import TextBlob
from collections import Counter


def fetch_conceptarium():
    # conceptarium_url = st.session_state.conceptarium_url
    # if conceptarium_url[-1] != '/':
    #    conceptarium_url += '/'
    #
    # conceptarium_url += 'find/lang/json?content=irrelevant&top_k=10&silent=True'
    # conceptarium_json = requests.get(conceptarium_url).json()
    # st.session_state.conceptarium_json = conceptarium_json
    st.session_state.conceptarium_json = json.load(open('data/dummy.json'))


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


def variability_over_past_week():
    data = variability_per_week()['variability']
    return round(data[0], 2), round(data[0] - data[1], 2)


def variability_over_past_month():
    data = variability_per_month()['variability']
    if len(data) < 2:
        return round(data[0], 2), None

    return round(data[0], 2), round(data[0] - data[1], 2)


def aggregate_variability():
    conceptarium = st.session_state.conceptarium_json
    embeddings = [e['embedding'] for e in conceptarium]
    centroid = np.mean(embeddings, axis=0)
    return round(np.mean([cos_dist(e, centroid) for e in embeddings]) * 100, 2)


def variability_of_fittest_quartile():
    conceptarium = st.session_state.conceptarium_json
    conceptarium = sorted(conceptarium, key=lambda x: x['activation'])
    fittest = conceptarium[:math.ceil(len(conceptarium) * 0.25)]
    embeddings = [e['embedding'] for e in fittest]
    centroid = np.mean(embeddings, axis=0)
    return round(np.mean([cos_dist(e, centroid) for e in embeddings]) * 100, 2)


def variability_per_week():
    conceptarium = st.session_state.conceptarium_json
    
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 7))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    variabilities = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        if len(thoughts) > 1:
            embeddings = [e['embedding'] for e in thoughts]
            centroid = np.mean(embeddings, axis=0)
            variabilities[age] = np.mean([cos_dist(e, centroid) for e in embeddings]) * 100

    data = pd.DataFrame()
    data['age'] = [e for e in range(max_age) if variabilities[e] != 0]
    data['variability'] = [e for e in variabilities if e != 0]
    return data


def variability_per_month():
    conceptarium = st.session_state.conceptarium_json
    
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 30))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    variabilities = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        if len(thoughts) > 1:
            embeddings = [e['embedding'] for e in thoughts]
            centroid = np.mean(embeddings, axis=0)
            variabilities[age] = np.mean([cos_dist(e, centroid) for e in embeddings]) * 100

    data = pd.DataFrame()
    data['age'] = [e for e in range(max_age) if variabilities[e] != 0]
    data['variability'] = [e for e in variabilities if e != 0]
    return data


def drift_over_past_week():
    data = drift_per_week()
    return round(data[0], 2), round(data[0] - data[1], 2)


def drift_over_past_week_percent_of_max():
    data = drift_per_week()
    percent_of_max_past_week = round(data[0] / max(data), 2) * 100
    percent_of_max_previous_week = round(data[1] / max(data), 2) * 100
    return str(percent_of_max_past_week) + '%', str(round(percent_of_max_past_week - percent_of_max_previous_week, 2)) + '%'


def drift_over_past_month():
    data = drift_per_month()
    if len(data) < 2:
        return round(data[0], 2), None
    return round(data[0], 2), round(data[0] - data[1], 2)


def drift_over_past_month_percent_of_max():
    data = drift_per_month()
    percent_of_max_past_week = round(data[0] / max(data), 2) * 100

    if len(data) < 2:
        return percent_of_max_past_week, None

    percent_of_max_previous_week = round(data[1] / max(data), 2) * 100
    return str(percent_of_max_past_week) + '%', str(percent_of_max_past_week - percent_of_max_previous_week) + '%'


def drift_per_week():
    conceptarium = st.session_state.conceptarium_json
    
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 7))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    centroids = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        embeddings = [e['embedding'] for e in thoughts]
        centroids[age] = np.mean(embeddings, axis=0)

    drifts = [cos_dist(centroids[e], centroids[e + 1]) * 100 for e in range(max_age - 1)]
    return drifts


def drift_per_month():
    conceptarium = st.session_state.conceptarium_json
    
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 30))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    centroids = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        embeddings = [e['embedding'] for e in thoughts]
        centroids[age] = np.mean(embeddings, axis=0)

    drifts = [cos_dist(centroids[e], centroids[e + 1]) * 100 for e in range(max_age - 1)]
    return drifts


def mean_fitness():
    data = fitness_distribution()
    data = round(np.mean(data), 2)
    return data


def fitness_interquartile_mean():
    data = fitness_distribution()
    q1, q3 = np.percentile(data, [25, 75])
    data = [e for e in data if q1 <= e and e <= q3]
    data = np.mean(data)
    return round(data, 2)


def fitness_interquartile_range():
    data = fitness_distribution()
    q1, q3 = np.percentile(data, [25, 75])
    return round(q3 - q1, 2)


def memetic_load():
    data = fitness_distribution()
    data = round((np.max(data) - np.mean(data)) / np.max(data), 2)
    return data


def fitness_distribution():
    conceptarium = st.session_state.conceptarium_json
    data = [e['activation'] for e in conceptarium]
    return data


def conciseness_per_week():
    conceptarium = st.session_state.conceptarium_json
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 7))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        lengths = [len(e['content'].split(' ')) / 130 * 60 for e in thoughts if e['modality'] == 'language']
        data[age] = np.mean(lengths)

    return data


def conciseness_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int((now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1]
    data = [len(e['content'].split(' ')) / 130 * 60 for e in thoughts if e['modality'] == 'language']
    return data


def readability_per_week():
    conceptarium = st.session_state.conceptarium_json
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 7))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age and e['modality'] == 'language']
        text = ' '.join([e['content'] for e in thoughts])
        blob = TextBlob(text)
        asl = len(blob.words) / len(text)
        asw = np.mean([syllable_count(e) for e in text.split(' ') if len(re.split(r'[.!?]+', e)) == 1 and len(e) > 0])
        data[age] = 0.39 * asl + 11.8 * asw - 15.59

    return data


def readability_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int((now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1 and e['modality'] == 'language']
    data = [0] * len(thoughts)
    
    for thought_idx, thought in enumerate(thoughts):
        text = thought['content']
        blob = TextBlob(text)
        asl = len(blob.words) / len(blob.sentences)
        asw = np.mean([syllable_count(e) for e in text.split(' ') if len(re.split(r'[.!?]+', e)) == 1 and len(e) > 0])
        data[thought_idx] = 0.39 * asl + 11.8 * asw - 15.59

    return data


def objectivity_per_week():
    conceptarium = st.session_state.conceptarium_json
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 7))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age and e['modality'] == 'language']
        text = TextBlob(' '.join([e['content'] for e in thoughts]))
        data[age] = 1 - text.sentiment[1]

    return data


def objectivity_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int((now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1 and e['modality'] == 'language']
    data = [0] * len(thoughts)
    
    for thought_idx, thought in enumerate(thoughts):
        text = TextBlob(thought['content'])
        data[thought_idx] = 1 - text.sentiment[1]

    return data


def sentiment_per_week():
    conceptarium = st.session_state.conceptarium_json
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int((now() - thought['timestamp']) / (60 * 60 * 24 * 7))
    
    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age
    
    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age and e['modality'] == 'language']
        text = TextBlob(' '.join([e['content'] for e in thoughts]))
        data[age] = text.sentiment[0]

    return data


def sentiment_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int((now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1 and e['modality'] == 'language']
    data = [0] * len(thoughts)
    
    for thought_idx, thought in enumerate(thoughts):
        text = TextBlob(thought['content'])
        data[thought_idx] = text.sentiment[0]

    return data


def interests():
    conceptarium = st.session_state.conceptarium_json
    language_thoughts = [e for e in conceptarium if e['modality'] == 'language']
    language_thoughts = sorted(language_thoughts, key=lambda x: x['timestamp'])
    text = ' '.join([e['content'] for e in language_thoughts])
    text = TextBlob(text.lower())
    keywords = text.noun_phrases
    keywords = [e.singularize() for e in keywords]
    keywords = Counter(keywords)
    keywords = [e for e in keywords.keys() if keywords[e] > 2]
    data = pd.DataFrame(columns=['keyword', 'start', 'end', 'count'])
    
    for keyword in keywords:
        instances = [e for e in language_thoughts if keyword in e['content']]
        if keyword == 'kernel function':
            print([(e['timestamp'], e['content']) for e in instances])
        if len(instances) > 0:
            start = datetime.fromtimestamp(instances[0]['timestamp']).strftime('%Y-%m-%d')
            end = datetime.fromtimestamp(instances[-1]['timestamp']).strftime('%Y-%m-%d')
            if start == end:
                end = datetime.fromtimestamp(instances[-1]['timestamp'] + (60 * 60 * 24)).strftime('%Y-%m-%d')
            data.loc[len(data.index)] = [keyword, start, end, len(instances)]

    data = data.sort_values(by='start')
    return data