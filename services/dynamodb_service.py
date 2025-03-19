import boto3
from flask import current_app

def get_dynamodb_client():
    return boto3.client(
        'dynamodb',
        region_name=current_app.config['AWS_REGION'],
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY']
    )

def get_all_jobs():
    dynamodb = get_dynamodb_client()
    try:
        response = dynamodb.scan(TableName=current_app.config['TABLE_NAME'])
        jobs = response.get("Items", [])
        parsed_jobs = [{
            "job_id": job.get("id", {}).get("N", ""),
            "job_name": job.get("Job_name", {}).get("S", ""),
            "job_description": job.get("Job_description", {}).get("S", "")
        } for job in jobs if "id" in job and "Job_name" in job and "Job_description" in job]
        return parsed_jobs
    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return []

def get_job_by_id(job_id):
    dynamodb = get_dynamodb_client()
    response = dynamodb.get_item(
        TableName=current_app.config['TABLE_NAME'], 
        Key={"id": {"N": job_id}}
    )
    return response.get("Item")