from pymongo import MongoClient

def find_jobs_in_location_and_title(title, location= None):
    # 连接数据库
    client = MongoClient('mongodb://localhost:27017')
    db = client['bigdata']
    collection = db['final']

    # 搜索
    jobs = collection.find({
        "jobtitle": title,
        "data": {
            "$elemMatch": {
                "job_city": location
            }
        }
    })

    # 继续判断然后添加到return结果中
    matching_jobs = []
    for document in jobs:
        for job in document["data"]:
            if document["jobtitle"] == title and job["job_city"] == location:
                matching_jobs.append(job)

    # Close connection to MongoDB
    client.close()

    return matching_jobs

#测试：
#jobs = find_jobs_in_location_and_title("data analyst")
#print(jobs)
