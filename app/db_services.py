from flask import current_app

def get_dynamodb():
    return current_app.config['DYNAMODB']

def insert_user(user_id, first_name, last_name, email, password):
    table = get_dynamodb().Table('Users')
    table.put_item(
        Item={
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
        }
    )


def get_user_by_userid(user_id):
    table = get_dynamodb().Table('Users')
    response = table.scan(
        FilterExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id}
    )
    return response['Items'][0] if response['Items'] else None

def insert_company(company_id, company_name, industry_type, employee_count, street, city, province, postal_code, phone, email, website):
    table = get_dynamodb().Table('Companies')
    table.put_item(
        Item={
            'company_id': company_id,
            'company_name': company_name,
            'industry_type': industry_type,
            'num_employees': employee_count,
            'street': street,
            'city': city,
            'province': province,
            'postal_code': postal_code,
            'phone': phone,
            'email': email,
            'website': website
        }
    )


def get_company_by_companyid(company_id):
    table = get_dynamodb().Table('Companies')
    response = table.scan(
        FilterExpression="company_id = :company_id",
        ExpressionAttributeValues={":company_id": company_id}
    )
    return response['Items'][0] if response['Items'] else None

def insert_diversity(diversity_id, male_rep, female_rep, transgender_rep, lgbtq_rep, indigenous_rep, disability_rep, minority_rep, veteran_rep):
    table = get_dynamodb().Table('Diversity')
    table.put_item(
        Item={
            'diversity_id': diversity_id,
            'male_representation': male_rep,
            'female_representation':female_rep,
            'transgender_representation': transgender_rep,
            'lgbtq_representation': lgbtq_rep,
            'indigenous_representation': indigenous_rep,
            'disability_representation': disability_rep,
            'minority_representation': minority_rep,
            'veteran_representation': veteran_rep,
        }
    )


def get_diversity_by_diversityid(diversity_id):
    table = get_dynamodb().Table('Diversity')
    response = table.scan(
        FilterExpression="diversity_id = :diversity_id",
        ExpressionAttributeValues={":diversity_id": diversity_id}
    )
    return response['Items'][0] if response['Items'] else None

def insert_job(job_id, position, department_id, department_name, description,looking_for,total_applicant,status,start_date, close_date):
    table = get_dynamodb().Table('Jobs')
    table.put_item(
        Item={
            'job_id': job_id,
            'position': position,
            'department_id': department_id,
            'department_name': department_name,
            'description': description,
            'looking_for': looking_for,
            'total_aaplicant': total_applicant,
            'status':status,
            'start_date': start_date,
            'close_date': close_date
        }
    )


def get_job_by_jobid(job_id):
    table = get_dynamodb().Table('Jobs')
    response = table.scan(
        FilterExpression="job_id = :job_id",
        ExpressionAttributeValues={":job_id": job_id}
    )
    return response['Items'][0] if response['Items'] else None

def get_all_jobs():
    table = get_dynamodb().Table('Jobs')
    response = table.scan()  
    return response['Items'] if response['Items'] else []

def delete_job_item(job_id):
    table = get_dynamodb().Table('Jobs')
    response=table.delete_item(
        Key={
            'job_id': job_id
        })       
    return response

def update_job(job_id, position=None, department_id=None, department_name=None, description=None, looking_for=None, 
            total_applicant=None, status=None, start_date=None, close_date=None):
    table = get_dynamodb().Table('Jobs')
    
    update_expression = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    if position:
        update_expression.append("#position = :position")
        expression_attribute_values[":position"] = position
        expression_attribute_names["#position"] = "position"  
    if status:
        update_expression.append("#status = :status")
        expression_attribute_values[":status"] = status
        expression_attribute_names["#status"] = "status"  
    
    if department_id:
        update_expression.append("department_id = :department_id")
        expression_attribute_values[":department_id"] = department_id
    if department_name:
        update_expression.append("department_name = :department_name")
        expression_attribute_values[":department_name"] = department_name
    if description:
        update_expression.append("description = :description")
        expression_attribute_values[":description"] = description
    if looking_for:
        update_expression.append("looking_for = :looking_for")
        expression_attribute_values[":looking_for"] = looking_for    
    if total_applicant:
        update_expression.append("total_applicant = :total_applicant")
        expression_attribute_values[":total_applicant"] = total_applicant
    if start_date:
        update_expression.append("start_date = :start_date")
        expression_attribute_values[":start_date"] = start_date
    if close_date:
        update_expression.append("close_date = :close_date")
        expression_attribute_values[":close_date"] = close_date
    
    if not update_expression:
        raise ValueError("At least one field must be provided for updating.")
    
    update_expression_str = "set " + ", ".join(update_expression)
    
    response = table.update_item(
        Key={'job_id': job_id},
        UpdateExpression=update_expression_str,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names,  
        ReturnValues="ALL_NEW" 
    )
    
    return response['Attributes']
def link_Company_User(company_id,user_id):
    table = get_dynamodb().Table('Companie-Users')
    table.put_item(
        Item={
            'user_id': user_id,
            'company_id': company_id
        }
    )
def get_company_by_userid(user_id):
    table = get_dynamodb().Table('Companie-Users')
    response = table.scan(
        FilterExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": user_id}
    )
    return response['Items'][0]["company_id"] if response['Items'] else None

def insert_analysis(user_id,resume_id,job_id,file_name,analysis):
    table = get_dynamodb().Table('ResumeAnalysis')
    table.put_item(
        Item={
            'user_id': user_id,
            'resume_id': resume_id,
            'job_id': job_id, 
            'filename': file_name,
            'analysis': analysis
        }
    )

def get_analysis_by_filename(file_name):
    table = get_dynamodb().Table('ResumeAnalysis')
    response = table.scan(
        FilterExpression="filename = :filename",
        ExpressionAttributeValues={":filename": file_name}
    )
    return response['Items'][0] if response['Items'] else None
