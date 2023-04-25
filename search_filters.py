import pymongo
import datetime
import pandas as pd


client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["bigdata"]

collections = ["cloud_developer", "data_scientist", "researcher", "software_engineer", "technical_manager"]


def search_jobs(job_title=None, location=None, date_posted=None, remote_jobs_only=None, employment_type=None):
    query = {}
    if job_title:
        query["job_title"] = {"$regex": job_title, "$options": "i"} # Use a case-insensitive regex for partial matching
    if location:
        query["$or"] = [{"job_city": {"$regex": location, "$options": "i"}},
                        {"job_state": {"$regex": location, "$options": "i"}},
                        {"job_country": {"$regex": location, "$options": "i"}}]
    if date_posted:
        current_time = datetime.datetime.now()
        if date_posted == "past_24_hours":
            time_threshold = current_time - datetime.timedelta(days=1)
        elif date_posted == "past_week":
            time_threshold = current_time - datetime.timedelta(weeks=1)
        elif date_posted == "past_month":
            time_threshold = current_time - datetime.timedelta(weeks=4)
        else:  # Default to any time
            time_threshold = None
        if time_threshold:
            query["job_posted_at_datetime_utc"] = {"$gte": time_threshold.isoformat()}
    if remote_jobs_only:
        query["job_is_remote"] = True
    if employment_type:
        query["job_employment_type"] = {"$regex": employment_type, "$options": "i"}

    matching_jobs = []
    
    for collection_name in collections:
        collection = db[collection_name]
        for job in collection.find(query):
            matching_jobs.append(job)

    return matching_jobs


if __name__ == "__main__":
    job_title_filter = input("Enter job title (e.g., Data Scientist): ")
    location_filter = input("Enter location (city, state, or country): ")
    date_posted_filter = input("Enter date posted (any_time, past_24_hours, past_week, past_month): ")
    remote_jobs_only_filter = input("Remote jobs only? (y/n): ").lower() == "y"
    employment_type_filter = input("Enter employment type (FULLTIME, CONTRACTOR, PARTTIME, INTERN): ")


result = search_jobs(job_title=job_title_filter, location=location_filter, date_posted=date_posted_filter,
                     remote_jobs_only=remote_jobs_only_filter, employment_type=employment_type_filter)


# Create a pandas DataFrame from the job data
df = pd.DataFrame(result)

# Save the DataFrame to an Excel file
df.to_excel('result.xlsx', index=False)
