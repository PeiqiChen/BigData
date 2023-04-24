from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient


with open('transformer.json', 'r', encoding='utf-8') as f:
    # Load the contents of the file into a dictionary
    data = json.load(f)
def recommend(userprofile, data):
    # 这个是keylist
    klist = list(data.keys())
    #这个是valuelist，向量list
    embeddinglist = [list(map(float, data[k])) for k in klist]
    #model搞一个
    model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
    #encode一下user数据变成向量
    sentence_embedding = model.encode(userprofile)
    #valuelist变成向量
    embeddinglist = [np.array(v, dtype=object) for v in embeddinglist]
    #find similiarity
    similarity_matrix = cosine_similarity([sentence_embedding] , embeddinglist).flatten()
    #panda去sort
    df=pd.DataFrame({"sentence":klist,"similarityscore":similarity_matrix})
    result_list = df.sort_values(by=["similarityscore"], ascending=False).head(10)["sentence"].tolist()

    client = MongoClient('mongodb://localhost:27017')
    db = client['bigdata']
    ans=[]
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        cursor = collection.find()

        # Iterate through all documents in the collection
        for document in cursor:
            # Extract job description field
            job_description = document.get('job_description', None)
            job_title = document.get('job_title', None)
            job_apply_link = document.get('job_apply_link', None)
            if job_description in result_list:
                ans.append((job_title,job_apply_link))
    return set(ans)
print(recommend("researcher  new york", data))
