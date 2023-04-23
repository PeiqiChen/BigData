import pymongo
import json

def insert_json_to_mongodb(filename, collection):
    # 先把json换成字典
    with open(filename, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)

    # 将data插入collection
    job_dict = {}
    for i in range(len(data_dict["data"])):
        job_dict[str(i)] = data_dict["data"][i]
    collection.insert_one(job_dict)

# 建立MongoDB连接

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["jobs"]

collection = db["cloud_developer"]

# 插入多个JSON文件到MongoDB调用上面函数
insert_json_to_mongodb("cloud_developer.json", collection)
collection = db["data_analyst"]
insert_json_to_mongodb("data_analyst.json", collection)
collection = db["data_scientist"]
insert_json_to_mongodb("data_scientist.json", collection)
