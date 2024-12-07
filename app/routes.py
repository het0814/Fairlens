from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignupForm,CompanyProfileForm,DiversityGoalForm

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
    return "<h1>Job & Resume Management Page</h1>"