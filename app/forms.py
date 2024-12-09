from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, PasswordField, SubmitField, IntegerField ,FloatField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo , NumberRange

class LoginForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign up & set-up the company’s Profile')

class CompanyProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    industry_type = StringField('Industry Type', validators=[DataRequired()])
    num_employees = IntegerField('Number of Employees', validators=[DataRequired()])
    street = StringField('Street/Building', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    province = StringField('Province', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    website = StringField('Website', validators=[DataRequired()])
    employee_data = FileField('Upload Employee Data', validators=[
        FileAllowed(['csv'], 'Only CSV files are allowed!')])
    submit = SubmitField('Confirm and Next')

class DiversityGoalForm(FlaskForm):
    male_representation = DecimalField('Male Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    female_representation = DecimalField('Female Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    transgender_representation = DecimalField('Transgender Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    lgbtq_representation = DecimalField('LGBTQ Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    indigenous_representation = DecimalField('Indigenous Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    disability_representation = DecimalField('Disability Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    minority_representation = DecimalField('Minority Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    veteran_representation = DecimalField('Veteran Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    submit = SubmitField('Set-up and Complete')

class JobForm(FlaskForm):
    job_id = StringField("Job ID", validators=[DataRequired()])
    position = StringField("Name of the Position", validators=[DataRequired()])
    department_id = StringField("Department ID", validators=[DataRequired()])
    department_name = StringField("Department Name", validators=[DataRequired()])
    description = TextAreaField("Job Description", validators=[DataRequired()])
    start_date = StringField("Start Date", validators=[DataRequired()])
    close_date = StringField("Close Date", validators=[DataRequired()])
    total_applicant = StringField("Total Applicant", validators=[DataRequired()])
    status = StringField("Status", validators=[DataRequired()])
    submit = SubmitField("Create")

class ResumeUploadForm(FlaskForm):
    resume_files = MultipleFileField("Upload Resumes", validators=[DataRequired(),
        FileAllowed(['pdf','docx'], 'Only PDF and DOCX files are allowed!')])
    analyze = SubmitField("Analyze")
