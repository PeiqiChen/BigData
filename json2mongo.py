import pymongo
import json

def insert_json_to_mongodb(filename, collection):
    # 读取JSON文件内容并转换为Python字典对象
    with open(filename, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)

    # 将字典插入集合
    collection.insert_one(data_dict)

# 建立MongoDB连接
client = pymongo.MongoClient("mongodb://localhost:27017/")

# 选择数据库
db = client["bigdata"]

# 选择集合
collection = db["final"]

# 插入多个JSON文件到MongoDB
insert_json_to_mongodb("data.json", collection)
insert_json_to_mongodb("data_analyst.json", collection)
insert_json_to_mongodb("data_scientist.json", collection)
