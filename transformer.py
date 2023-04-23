from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import json


# 连接到 MongoDB 数据库
client = MongoClient('mongodb://localhost:27017/')
joblist={}

# 选择数据库
db = client['bigdata']

# 获取数据库中所有集合的名称
collections = db.list_collection_names()

# 加载句向量模型
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

for collection_name in db.list_collection_names():
    collection = db[collection_name]
    cursor = collection.find()

    # Iterate through all documents in the collection
    for document in cursor:
        # Extract job description field
        for jobid in document.keys():
            if jobid.isdigit():
                job_description = document[jobid].get('job_description', None)
                if job_description is not None:
                    job_vector = model.encode(job_description)
                    joblist[job_description]= job_vector.tolist()
with open('transformer.json', 'w', encoding='utf-8') as f:
    json.dump(joblist, f, ensure_ascii=False)
