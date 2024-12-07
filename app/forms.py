from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, IntegerField ,FloatField
from wtforms.validators import DataRequired, Email, EqualTo , NumberRange

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
    male_representation = FloatField('Male Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    female_representation = FloatField('Female Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    transgender_representation = FloatField('Transgender Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    lgbtq_representation = FloatField('LGBTQ Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    indigenous_representation = FloatField('Indigenous Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    disability_representation = FloatField('Disability Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    minority_representation = FloatField('Minority Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    veteran_representation = FloatField('Veteran Representation (%)', validators=[DataRequired(), NumberRange(0, 100)])
    submit = SubmitField('Set-up and Complete')

