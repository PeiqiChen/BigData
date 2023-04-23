from sentence_transformers import SentenceTransformer
from pymongo import MongoClient

# 连接到 MongoDB 数据库
client = MongoClient('mongodb://localhost:27017/')
joblist=[]

# 选择数据库
db = client['bigdata']

# 获取数据库中所有集合的名称
collections = db.list_collection_names()

# 加载句向量模型
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

for collection_name in collections:
    print(collection_name)
    # 获取集合
    collection = db[collection_name]

    # 搜索文档
    cursor = collection.find()
    for document in cursor:
        for jobnumber in document:
            for i in jobnumber:
                print(i)
            break
            job_description = jobnumber['job_description']
            job_vector = model.encode(job_description)
            joblist.append((job_description, job_vector))
print(joblist)
def recommend(userprofile):
    print("finish")
