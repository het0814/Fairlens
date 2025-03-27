import io
from flask import current_app
def get_s3bucket():
    return current_app.config['S3_RESOURCE'].Bucket('fairlens')

def upload_CompanyData(company_id,file):
    get_s3bucket().upload_fileobj(file,f"CompanyData/{company_id}/data.csv")

def upload_Resume(job_id,file):
    get_s3bucket().upload_fileobj(file,f"Resumes/{job_id}/{file.filename}")

def get_CompanyData(company_id):
    obj = get_s3bucket().Object(f"CompanyData/{company_id}/data.csv")
    csv_data = obj.get()['Body'].read().decode('utf-8')
    data = io.StringIO(csv_data)
    return data