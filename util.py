import numpy as np
import re


def cos_dist(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return 1 - dot_product / (norm_a * norm_b)


def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count


def sample_spherical(npoints, ndim=3):
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    vec = np.transpose(vec)
    return vec


'''
from sentence_transformers import SentenceTransformer, util
model=SentenceTransformer('clip-ViT-B-32')

def similarity(x, y):
    emb_x=model.encode(x, convert_to_tensor=True)
    emb_y=model.encode(y, convert_to_tensor=True)
    return util.cos_sim(emb_x, emb_y)


'''