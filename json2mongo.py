import pymongo
import json

def insert_json_to_mongodb(filename, collection):
    # 先把json换成字典
    with open(filename, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)

    # 将字典插入collection
    collection.insert_one(data_dict)

# 建立MongoDB连接
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["bigdata"]

collection = db["final"]

# 插入多个JSON文件到MongoDB调用上面函数
insert_json_to_mongodb("data/cloud_developer.json", collection)
insert_json_to_mongodb("data/data_analyst.json", collection)
insert_json_to_mongodb("data/data_scientist.json", collection)
