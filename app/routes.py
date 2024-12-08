from flask import Blueprint, render_template, redirect, url_for, flash,request
from app.forms import SignupForm,CompanyProfileForm,DiversityGoalForm,JobForm,ResumeUploadForm
from datetime import datetime


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Signup successful! Please set up your company profile.', 'success')
        return redirect(url_for('main.company_setup'))
    return render_template('signup.html', form=form)

@main.route('/company-setup', methods=['GET', 'POST'])
def company_setup():
    form = CompanyProfileForm()
    if form.validate_on_submit():
        # Save locally for now willconnect when aws is setuped
        if form.employee_data.data:
            file = form.employee_data.data
            file.save(f"uploads/{file.filename}")
        flash('Company profile saved successfully!', 'success')
        return redirect(url_for('main.diversity_goal_setup'))
    return render_template('company.html', form=form)

@main.route('/diversity-goal-setup', methods=['GET', 'POST'])
def diversity_goal_setup():
    form = DiversityGoalForm()
    if form.validate_on_submit():
        # diversity goals to database for now, justprint for virificaion
        diversity_goals = {
            "male_representation": form.male_representation.data,
            "female_representation": form.female_representation.data,
            "transgender_representation": form.transgender_representation.data,
            "lgbtq_representation": form.lgbtq_representation.data,
            "indigenous_representation": form.indigenous_representation.data,
            "disability_representation": form.disability_representation.data,
            "minority_representation": form.minority_representation.data,
            "veteran_representation": form.veteran_representation.data,
        }
        print(diversity_goals)

        if form.submit.data:
            return redirect(url_for('main.index'))
        flash('Diversity goals saved successfully!', 'success')

    return render_template('diversity_goal.html', form=form)


@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/job-management')
def job_management():

    jobs = [
        {"job_id": 1, "position": "Software Developer", "total_applicants": 100, "department": "Tech", "status": "Active"}
    ]
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
        job_data = {
            "job_id": form.job_id.data,
            "position": form.position.data,
            "department_id": form.department_id.data,
            "department_name": form.department_name.data,
            "description": form.description.data,
            "start_date": form.start_date.data,
            "close_date": form.close_date.data
        }

        # later to dynamo
        print(job_data)

        flash("Job created successfully!", "success")
        return redirect(url_for('main.job_management'))
    
    return render_template('create_job.html', form=form)

@main.route('/edit-job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    # query for dynamo
    job = {
        "job_id": job_id,
        "position": "Software Developer",
        "department_id": "101",
        "department_name": "Tech",
        "description": "Develop and maintain software.",
        "start_date":  datetime.strptime("2024-12-01", "%Y-%m-%d"),
        "close_date": datetime.strptime("2024-12-31", "%Y-%m-%d")
    }

    form = JobForm(data=job)

    if form.validate_on_submit():
        updated_job = {
            "job_id": form.job_id.data,
            "position": form.position.data,
            "department_id": form.department_id.data,
            "department_name": form.department_name.data,
            "description": form.description.data,
            "start_date": form.start_date.data,
            "close_date": form.close_date.data
        }
        print(f"Updated Job: {updated_job}")

        flash("Job updated successfully!", "success")
        return redirect(url_for('main.job_management'))

    return render_template('edit_job.html', form=form, job_id=job_id)

@main.route('/delete-job/<job_id>', methods=['GET', 'POST'])
def delete_job(job_id):
    if request.method == 'POST':
        # delete from dynamo
        print(f"Job with ID {job_id} has been deleted.")
        flash(f"Job {job_id} deleted successfully!", "success")
        return redirect(url_for('main.job_management'))

    return render_template('delete_job.html', job_id=job_id)

@main.route('/analyze-resume/<job_id>', methods=['GET', 'POST'])
def analyze_resume(job_id):
    # dynamo query
    job = {
        "job_id": job_id,
        "department_id": "101",
        "position": "Software Developer",
        "department_name": "Tech",
        "job_description": "Develop and maintain software.",
        "start_date":  datetime.strptime("2024-12-01", "%Y-%m-%d"),
        "close_date": datetime.strptime("2024-12-31", "%Y-%m-%d")
    }

    form = ResumeUploadForm()

    top_applicants=[]
     

    if form.validate_on_submit():
        if form.resume_files.data:
            for file in form.resume_files.data:
                file.save(f"uploads/{file.filename}")
                flash(f"Uploaded {file.filename}", "success")
        
        if form.analyze.data:
            # ai function call for shortlist
            top_applicants = {
                "Male": ["Applicant 1", "Applicant 2"],
                "Female": ["Applicant 3", "Applicant 4"],
                "Trans": ["Applicant 5"],
                "LGBTQ": ["Applicant 6"],
                "Minority": ["Applicant 7"],
                "Disability": ["Applicant 8"],
            }
            flash("Analysis completed successfully!", "success")

    return render_template("analyze_resume.html", form=form, job=job, top_applicants=top_applicants)