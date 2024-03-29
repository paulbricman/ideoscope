import numpy as np
import streamlit as st
import requests
import pandas as pd
from time import time as now
from datetime import datetime, date, time
import math
from util import cos_dist, sample_spherical, syllable_count
import re
from textblob import TextBlob
from collections import Counter
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


def fetch_conceptarium():
    conceptarium_url = st.session_state['conceptarium_url']
    if not conceptarium_url.startswith('http://'):
        conceptarium_url = 'http://' + conceptarium_url
    if conceptarium_url[-1] == '/':
        conceptarium_url = conceptarium_url[:-1]

    conceptarium_url += ':8000/find'
    conceptarium = requests.get(conceptarium_url, params={
        'query': '',
        'return_embeddings': True
    }, headers={
        'authorization': 'Bearer ' + st.session_state['access_token']
    }).json()
    conceptarium = conceptarium['authorized_thoughts']

    for e_idx, e in enumerate(conceptarium):
        conceptarium[e_idx]['embedding'] = conceptarium[e_idx]['embeddings']['text_image']
        conceptarium[e_idx]['activation'] = np.log(e['interest'] / (1 - 0.9)) - \
            0.9 * np.log((now() - e['timestamp']) / (3600 * 24) + 0.1)

    st.session_state['conceptarium_json'] = conceptarium


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
    conceptarium = st.session_state.conceptarium_json
    timestamps = pd.DataFrame(conceptarium)['timestamp'].values
    midnight = datetime.combine(datetime.today(), time.min).timestamp()

    timestamps = [midnight - e for e in timestamps]
    timestamps = [int(1 + e / (60 * 60 * 24)) for e in timestamps]
    timestamps = sorted(timestamps)
    data = [timestamps.count(e) for e in range(max(timestamps) + 1)]
    return data


def birth_rate_by_day_of_week():
    conceptarium = st.session_state.conceptarium_json
    timestamps = pd.DataFrame(conceptarium)['timestamp'].values

    data = [date.fromtimestamp(e).strftime('%a') for e in timestamps]
    return pd.DataFrame(data, columns=['weekday'])


def birth_rate_by_time_of_day():
    conceptarium = st.session_state.conceptarium_json
    timestamps = pd.DataFrame(conceptarium)['timestamp'].values

    data = [datetime.fromtimestamp(e, tz=datetime.now(
    ).astimezone().tzinfo).strftime('%H:%M') for e in timestamps]
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
    conceptarium = st.session_state.conceptarium_json
    conceptarium = sorted(conceptarium, key=lambda x: x['activation'])
    fittest = conceptarium[:math.ceil(len(conceptarium) * 0.25)]

    fittest_text = [e for e in fittest if e['modality'] == 'text']
    fittest_imagery = [e for e in fittest if e['modality'] == 'image']

    if len(fittest_text) > 0:
        fittest_text_age = [
            int((now() - e['timestamp']) / (60 * 60 * 24 * 7)) for e in fittest_text]
        fittest_text_age = [fittest_text_age.count(
            e) for e in range(max(fittest_text_age) + 1)]
    else:
        fittest_text_age = []

    if len(fittest_imagery) > 0:
        fittest_imagery_age = [
            int((now() - e['timestamp']) / (60 * 60 * 24 * 7)) for e in fittest_imagery]
        fittest_imagery_age = [fittest_imagery_age.count(
            e) for e in range(max(fittest_imagery_age) + 1)]
    else:
        fittest_imagery_age = []

    return fittest_text_age, fittest_imagery_age


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
    fittest = conceptarium[: math.ceil(len(conceptarium) * 0.25)]
    embeddings = [e['embedding'] for e in fittest]
    centroid = np.mean(embeddings, axis=0)
    return round(np.mean([cos_dist(e, centroid) for e in embeddings]) * 100, 2)


def variability_per_week():
    conceptarium = st.session_state.conceptarium_json

    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 7))

    max_age = max([e['age'] for e in conceptarium]) + 1
    variabilities = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        if len(thoughts) > 1:
            embeddings = [e['embedding'] for e in thoughts]
            centroid = np.mean(embeddings, axis=0)
            variabilities[age] = np.mean(
                [cos_dist(e, centroid) for e in embeddings]) * 100

    data = pd.DataFrame()
    data['age'] = [e for e in range(max_age) if variabilities[e] != 0]
    data['variability'] = [e for e in variabilities if e != 0]
    return data


def variability_per_month():
    conceptarium = st.session_state.conceptarium_json

    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 30))

    max_age = max([e['age'] for e in conceptarium]) + 1
    variabilities = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        if len(thoughts) > 1:
            embeddings = [e['embedding'] for e in thoughts]
            centroid = np.mean(embeddings, axis=0)
            variabilities[age] = np.mean(
                [cos_dist(e, centroid) for e in embeddings]) * 100

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
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 7))

    max_age = max([e['age'] for e in conceptarium]) + 1
    centroids = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        embeddings = [e['embedding'] for e in thoughts]
        centroids[age] = np.mean(embeddings, axis=0)

    drifts = [cos_dist(centroids[e], centroids[e + 1])
              * 100 for e in range(max_age - 1)]
    return drifts


def drift_per_month():
    conceptarium = st.session_state.conceptarium_json

    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 30))

    max_age = max([e['age'] for e in conceptarium]) + 1
    centroids = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        embeddings = [e['embedding'] for e in thoughts]
        centroids[age] = np.mean(embeddings, axis=0)

    drifts = [cos_dist(centroids[e], centroids[e + 1])
              * 100 for e in range(max_age - 1)]
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
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 7))

    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age'] == age]
        lengths = [len(e['content'].split(' ')) / 130 *
                   60 for e in thoughts if e['modality'] == 'text']
        data[age] = np.mean(lengths)

    return data


def conciseness_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int(
        (now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1]
    data = [len(e['content'].split(' ')) / 130 *
            60 for e in thoughts if e['modality'] == 'text']
    return data


def readability_per_week():
    conceptarium = st.session_state.conceptarium_json
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 7))

    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age']
                    == age and e['modality'] == 'text']
        text = ' '.join([e['content'] for e in thoughts])
        blob = TextBlob(text)
        asl = len(blob.words) / len(blob.sentences)
        asw = np.mean([syllable_count(e) for e in text.split(
            ' ') if len(re.split(r'[.!?]+', e)) == 1 and len(e) > 0])
        data[age] = 0.39 * asl + 11.8 * asw - 15.59

    return data


def readability_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int(
        (now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1 and e['modality'] == 'text']
    data = [0] * len(thoughts)

    for thought_idx, thought in enumerate(thoughts):
        text = thought['content']
        blob = TextBlob(text)
        asl = len(blob.words) / len(blob.sentences)
        asw = np.mean([syllable_count(e) for e in text.split(
            ' ') if len(re.split(r'[.!?]+', e)) == 1 and len(e) > 0])
        data[thought_idx] = 0.39 * asl + 11.8 * asw - 15.59

    return data


def objectivity_per_week():
    conceptarium = st.session_state.conceptarium_json
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 7))

    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age']
                    == age and e['modality'] == 'text']
        text = TextBlob(' '.join([e['content'] for e in thoughts]))
        data[age] = 1 - text.sentiment[1]

    return data


def objectivity_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int(
        (now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1 and e['modality'] == 'text']
    data = [0] * len(thoughts)

    for thought_idx, thought in enumerate(thoughts):
        text = TextBlob(thought['content'])
        data[thought_idx] = 1 - text.sentiment[1]

    return data


def sentiment_per_week():
    conceptarium = st.session_state.conceptarium_json
    for thought_idx, thought in enumerate(conceptarium):
        conceptarium[thought_idx]['age'] = int(
            (now() - thought['timestamp']) / (60 * 60 * 24 * 7))

    max_age = max([e['age'] for e in conceptarium]) + 1
    data = [0] * max_age

    for age in range(max_age):
        thoughts = [e for e in conceptarium if e['age']
                    == age and e['modality'] == 'text']
        text = TextBlob(' '.join([e['content'] for e in thoughts]))
        data[age] = text.sentiment[0]

    return data


def sentiment_distribution_over_past_month():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if int(
        (now() - e['timestamp']) / (60 * 60 * 24 * 30)) < 1 and e['modality'] == 'text']
    data = [0] * len(thoughts)

    for thought_idx, thought in enumerate(thoughts):
        text = TextBlob(thought['content'])
        data[thought_idx] = text.sentiment[0]

    return data


def interests():
    conceptarium = st.session_state.conceptarium_json
    text_thoughts = [
        e for e in conceptarium if e['modality'] == 'text']
    text_thoughts = sorted(text_thoughts, key=lambda x: x['timestamp'])
    text = ' '.join([e['content'] for e in text_thoughts])
    text = TextBlob(text.lower())
    keywords = text.noun_phrases
    keywords = [e.singularize() for e in keywords]
    keywords = Counter(keywords)
    keywords = [e for e in keywords.keys() if keywords[e] > 2]
    data = pd.DataFrame(columns=['keyword', 'start', 'end', 'count'])

    for keyword in keywords:
        instances = [e for e in text_thoughts if keyword in e['content']]
        if len(instances) > 0:
            start = datetime.fromtimestamp(
                instances[0]['timestamp']).strftime('%Y-%m-%d')
            end = datetime.fromtimestamp(
                instances[-1]['timestamp']).strftime('%Y-%m-%d')
            if start == end:
                end = datetime.fromtimestamp(
                    instances[-1]['timestamp'] + (60 * 60 * 24)).strftime('%Y-%m-%d')
            data.loc[len(data.index)] = [keyword, start, end, len(instances)]

    data = data.sort_values(by='start')
    return data


def projection_2d():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if e['modality'] == 'text']
    embeddings = [e['embedding'] for e in thoughts]
    reducer = TSNE(2)
    embeddings_2d = reducer.fit_transform(embeddings)
    data = [[*emb, thoughts[emb_idx]['modality']]
            for emb_idx, emb in enumerate(embeddings_2d)]
    data = [e + ['*image*'] if e[2] == 'image' else e +
            [thoughts[e_idx]['content']] for e_idx, e in enumerate(data)]
    data = pd.DataFrame(data, columns=['x', 'y', 'modality', 'content'])
    data.content = data.content.str.wrap(40)
    data.content = data.content.apply(lambda x: x.replace('\n', '<br>'))
    return data


def projection_3d():
    conceptarium = st.session_state.conceptarium_json
    thoughts = [e for e in conceptarium if e['modality'] == 'text']
    embeddings = [e['embedding'] for e in thoughts]
    reducer = TSNE(3)
    embeddings_3d = reducer.fit_transform(embeddings)
    data = [[*emb, thoughts[emb_idx]['modality']]
            for emb_idx, emb in enumerate(embeddings_3d)]
    data = [e + ['*image*'] if conceptarium[e_idx]['modality'] ==
            'image' else e + [thoughts[e_idx]['content']] for e_idx, e in enumerate(data)]
    data = [e + [3] for e in data]
    data = pd.DataFrame(
        data, columns=['x', 'y', 'z', 'modality', 'content', 'size'])
    data.content = data.content.str.wrap(40)
    data.content = data.content.apply(lambda x: x.replace('\n', '<br>'))
    return data


def energy_spectrum():
    conceptarium = st.session_state.conceptarium_json
    embeddings = [e['embedding'] for e in conceptarium]
    reducer = PCA(20)
    embeddings = reducer.fit_transform(embeddings)
    data = reducer.explained_variance_ratio_
    return data


def explored_portion_of_semantic_space():
    n_probes = 500000
    hits = 0

    conceptarium = st.session_state.conceptarium_json
    probes = sample_spherical(n_probes, 512)
    embeddings = np.array([e['embedding'] for e in conceptarium])
    similarities = np.dot(probes, embeddings.T)
    max_similarities = np.max(similarities, axis=1)
    hits = np.count_nonzero(max_similarities > 0.19)

    hitrate = hits / n_probes
    data = pd.DataFrame(
        [['explored', hitrate], ['unexplored', 1 - hitrate]], columns=['name', 'value'])
    return data


def discovery_per_thought(explored_portion):
    conceptarium = st.session_state.conceptarium_json
    data = explored_portion / len(conceptarium)
    return data


def conceptarium_age():
    conceptarium = st.session_state.conceptarium_json
    conceptarium = sorted(conceptarium, key=lambda x: x['timestamp'])
    age = (now() - conceptarium[0]['timestamp']) / (60 * 60 * 24 * 365)
    return age
