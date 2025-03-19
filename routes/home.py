from flask import Blueprint, render_template, request
from services.dynamodb_service import get_all_jobs

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    message = request.args.get('message')
    jobs = get_all_jobs()
    return render_template("index.html", message=message, jobs=jobs)