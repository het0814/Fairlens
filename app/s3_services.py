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

from io import BytesIO

def get_resumes_from_s3():
    
    bucket = get_s3bucket()
    prefix = "Resumes/samples/"
    all_objects = bucket.objects.filter(Prefix=prefix)

    categorized_resumes = {
        "male_resume": [],
        "female_resume": [],
        "transgender_resume": [],
        "lgbtq_resume": [],
        "indigenous_resume": [],
        "disability_resume": [],
        "minority_resume": [],
        "veteran_resume": []
    }

    folder_to_field = {
        "male": "male_resume",
        "female": "female_resume",
        "transgender": "transgender_resume",
        "lgbtq": "lgbtq_resume",
        "indigenous": "indigenous_resume",
        "disability": "disability_resume",
        "minority": "minority_resume",
        "veteran": "veteran_resume"
    }

    for obj in all_objects:
        key = obj.key
        if key.endswith('/'):
            continue

        try:
            category = key.split('Resumes/samples/')[1].split('/')[0]
        except IndexError:
            continue

        field_name = folder_to_field.get(category)
        if field_name:
            file_obj = obj.get()
            file_bytes = file_obj['Body'].read()
            filename = key.split('/')[-1]

            categorized_resumes[field_name].append((filename, file_bytes))

    return categorized_resumes
