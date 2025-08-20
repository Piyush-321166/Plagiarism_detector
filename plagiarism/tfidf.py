import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def tfidf_cosine(query: str, docs: list) -> list:
    vect = TfidfVectorizer(ngram_range=(1, 2))
    tfidf = vect.fit_transform([query] + docs)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    return sims.tolist()
