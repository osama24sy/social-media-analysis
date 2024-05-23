from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import numpy as np
import pandas as pd


model = SentenceTransformer('Alibaba-NLP/gte-base-en-v1.5', trust_remote_code=True)
topics_embed = np.load('data/topics_emb.npy', nmap_mode='r')
topics_id = np.load('data/topics_id.npy')
topics = pd.read_csv('data/topics.csv')

def topic_classify(text, batch_size=500):
    text_emb = model.encode(text)
    similarities = []
    for i in range(0, len(topics_embed), batch_size):
        batch_embeddings = topics_embed[i:i + batch_size]
        batch_embeddings = np.array(batch_embeddings)  # Ensure proper numpy array
        scores = np.dot(text_emb, batch_embeddings.T)
        # scores = np.dot(text_emb.reshape(1, -1), topics_embed[i:i+batch_size].T)
        similarities.extend(scores.tolist()[0])

    max_score_idx = np.argmax(similarities)
    # get the topic with the id from topics df
    topic = topics[topics['topic_id'] == topics_id[max_score_idx]].iloc[0].text

    return topics_id[max_score_idx], scores[max_score_idx], topic