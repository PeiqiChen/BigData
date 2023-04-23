import pymongo
import json
import os

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
# 待插入的JSON文件所在目录
json_dir = "data"

# 遍历目录下的所有JSON文件，并插入到MongoDB中
for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(json_dir, filename)
        insert_json_to_mongodb(filepath, collection)
        insert_json_to_mongodb(filepath, collection)
