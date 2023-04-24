from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
import pandas as pd

with open('transformer.json', 'r', encoding='utf-8') as f:
    # Load the contents of the file into a dictionary
    data = json.load(f)
def recommend(userprofile, data):
    # using bert
    klist = list(data.keys())
    embeddinglist = [list(map(float, data[k])) for k in klist]
    model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    sentence_embedding = model.encode(userprofile)
    embeddinglist = [np.array(v, dtype=object) for v in embeddinglist]
    similarity_matrix = cosine_similarity([sentence_embedding] , embeddinglist).flatten()
    df=pd.DataFrame({"sentence":klist,"similarityscore":similarity_matrix})
    df = df.sort_values(by=["similarityscore"], ascending=False).head(5)
    return list(df["sentence"])
print(recommend("researcher  new york", data))
