import uuid
from flask import Blueprint, render_template, redirect, url_for, flash,request, session
from app.forms import LoginForm,SignupForm,CompanyProfileForm,DiversityGoalForm,JobForm,ResumeUploadForm
from datetime import datetime
import os
from app.AI_services import *
from app.db_services import *
from app.DG_services import *
from app.Chart_Generator_services import*
from app.s3_services import*
from app.textExtraction_services import *

import boto3
from botocore.exceptions import ClientError
import hmac
import hashlib
import base64

main = Blueprint('main', __name__)

COGNITO_REGION = "us-east-1"
COGNITO_USER_POOL_ID = "us-east-1_lcY7osG9F"
COGNITO_CLIENT_ID = "egsqef5om3gqsf2mnqaunt0p0"
COGNITO_CLIENT_SECRET = "1c9s6s2r20445r36atckb3v9c4u6ms3q850vtj77734mqc1622v8"

def generate_secret_hash(username, client_id, client_secret):

    message = username + client_id
    dig = hmac.new(
        client_secret.encode("utf-8"),
        msg=message.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    return base64.b64encode(dig).decode()

def authenticate_user(username, password):

    client = boto3.client("cognito-idp", region_name=COGNITO_REGION)
    try:
        response = client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": username,
                "PASSWORD": password,
                "SECRET_HASH": generate_secret_hash(username, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET),
            },
        )
        return "Success", response 
    except ClientError as e:
        return None, e.response["Error"]["Message"]  

def sign_up_user(first_name, last_name, email, password):
    client = boto3.client("cognito-idp", region_name=COGNITO_REGION)
    try:
        response = client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            SecretHash=generate_secret_hash(email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET),
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "given_name", "Value": first_name},
                {"Name": "family_name", "Value": last_name},
                {"Name": "email", "Value": email},
            ],
        )
        return "Success", response
    except ClientError as e:
        return None, e.response["Error"]["Message"]   

@main.route('/')
def index():
    form = LoginForm()
    return render_template('login.html',form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        session['username']=username
        password = form.password.data

        message, response = authenticate_user(username, password)

        if message == "Success":
            flash("Login successful!", "success")
            return redirect("/home")
        else:
            flash(f"Login failed: {response}", "danger")
            return render_template("login.html",form=form)  
    return render_template("login.html",form=form)  

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        session['username']=email
        password = form.password.data

        message, response = sign_up_user(first_name, last_name, email, password)
        if message == "Success":
            flash('Signup successful! Please set up your company profile.', 'success')
            return redirect(url_for('main.company_setup'))
        else:            
            flash(f"Sign-up failed: {response}", "danger")
    return render_template('signup.html', form=form)

@main.route('/company-setup', methods=['GET', 'POST'])
def company_setup():
    form = CompanyProfileForm()
    if form.validate_on_submit():
        company_id = str(uuid.uuid4())
        user_id=session.get('username')
        link_Company_User(company_id,user_id)
        insert_company(company_id,form.company_name.data,form.industry_type.data,form.num_employees.data,form.street.data,form.city.data,form.province.data,form.postal_code.data,form.phone.data,form.email.data,form.website.data)
        if form.employee_data.data:
            file = form.employee_data.data
            upload_CompanyData(company_id,file)
        flash('Company profile saved successfully!', 'success')
        return redirect(url_for('main.diversity_goal_setup', company_id=company_id))
    return render_template('company.html', form=form)

@main.route('/diversity-goal-setup/<company_id>', methods=['GET', 'POST'])
def diversity_goal_setup(company_id):
    form = DiversityGoalForm()
    province=get_company_by_companyid(company_id)["province"]
    suggestions= get_diversity_weights(province)
    if form.validate_on_submit():
        diversity_id = str(uuid.uuid4())
        insert_diversity(diversity_id,form.male_representation.data,form.female_representation.data,form.transgender_representation.data,form.lgbtq_representation.data,form.indigenous_representation.data,form.disability_representation.data,form.minority_representation.data,form.veteran_representation.data)
        flash('Diversity goals saved successfully!', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('diversity_goal.html', form=form,suggestions=suggestions)


@main.route('/home')
def home():
    company_id = get_company_by_userid(session.get('username'))
    if company_id:
        s3_file = get_CompanyData(company_id)
        df = pd.read_csv(s3_file)
        
        # Save to local dummy file
        data_path = os.path.join("app", "Dashboard_Pages", "data", "data.csv")
        df.to_csv(data_path, index=False)
    return render_template('home.html')

@main.route('/job-management')
def job_management():

    jobs=get_all_jobs()
    stats = {
        "total_jobs": len(jobs),
        "active_jobs": len([job for job in jobs if job["status"] == "Active"]),
        "deadlines_today": len([job for job in jobs if job["status"] == "Deadline Today"])
    }
    return render_template('job_management.html', jobs=jobs, stats=stats)


@main.route('/create-job', methods=['GET', 'POST'])
def create_job():
    form = JobForm()
    if form.validate_on_submit():
        insert_job(form.job_id.data,form.position.data,form.department_id.data,form.department_name.data,form.description.data,form.looking_for.data,form.total_applicant.data,form.status.data,form.start_date.data,form.close_date.data)
        flash("Job created successfully!", "success")
        return redirect(url_for('main.job_management'))
    
    return render_template('create_job.html', form=form)

@main.route('/edit-job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job=get_job_by_jobid(job_id)
    form = JobForm(data=job)

    if form.validate_on_submit():
        update_job(form.job_id.data,form.position.data,form.department_id.data,form.department_name.data,form.description.data,form.looking_for.data,form.total_applicant.data,form.status.data,form.start_date.data,form.close_date.data)
        flash("Job updated successfully!", "success")
        return redirect(url_for('main.job_management'))

    return render_template('edit_job.html', form=form, job_id=job_id)

@main.route('/delete-job/<job_id>', methods=['GET', 'POST'])
def delete_job(job_id):
    if request.method == 'POST':
        delete_job_item(job_id)
        flash(f"Job {job_id} deleted successfully!", "success")
        return redirect(url_for('main.job_management'))
    return render_template('delete_job.html', job_id=job_id)

@main.route('/analyze-resume/<job_id>', methods=['GET', 'POST'])
def analyze_resume(job_id):
    job=get_job_by_jobid(job_id)
    user_id=session.get('username')
    form = ResumeUploadForm()

    if form.validate_on_submit():
        uploaded_files = form.resume_files.data
        job_description = job["description"]

        if not uploaded_files:
            flash("No resumes uploaded", "error")
            return render_template("analyze_resumes.html",form=form,job=job,message='no resume')
        
        if not job_description:
            flash("Job description is required", "error")
            return render_template("analyze_resumes.html",form=form,job=job,message='no job')

        analysis = []
        score_data=[]
        for resume_file in uploaded_files:
            # file_path = os.path.join("uploads", resume_file.filename)
            # resume_file.save(file_path)
            file_copy = BytesIO(resume_file.read())  
            file_copy.seek(0)

            upload_Resume(job_id,resume_file)
            resume_text=extract_text(file_copy,resume_file.filename)
            
            # Perform analysis
            resume_analysis = analyze_resume_service(resume_text, job_description)
            score = score_resume(resume_text,job_description)
            donut_analysis = donut_score_resume(resume_text,job_description)

            # Generate charts
            charts = generate_resume_charts(score, donut_analysis)
            analysis.append({                       # will have to remove later
                "file_name": resume_file.filename, 
                "analysis": resume_analysis, 
                "score": score,
                "donut_analysis": donut_analysis,
                "charts": charts
            })
            analysis_data=[{
                "file_name": resume_file.filename, 
                "analysis": resume_analysis, 
                "score": score,
                "donut_analysis": donut_analysis,
            }]
            score_data.append({
                "file_name": resume_file.filename, 
                "score": score,
                "donut_analysis": donut_analysis,
            })
            resume_id = str(uuid.uuid4())
            insert_analysis(user_id,resume_id,job_id,resume_file.filename,analysis_data)
        rank=score_data

        return render_template("resume_analysis_result.html", analyses=analysis, job_info=job,rank=rank)
    return render_template("analyze_resume.html", form=form,job=job)
   