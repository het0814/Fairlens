from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import SignupForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Signup successful! Please set up your company profile.', 'success')
        return redirect(url_for('main.company_setup'))
    return render_template('signup.html', form=form)

@main.route('/company-setup')
def company_setup():
    return render_template('company.html')