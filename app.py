from flask import Flask
import os
import secrets
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
app.secret_key = secrets.token_hex(16)  # This generates a 32-character hexadecimal secret key
from dotenv import load_dotenv

# Import route handlers
from routes.home import home_bp
from routes.resume_analyzer import resume_analyzer_bp
from routes.job_profile import job_profile_bp 

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(resume_analyzer_bp, url_prefix='/resume_analyzer')
app.register_blueprint(job_profile_bp) 

#Loading the OS File
load_dotenv(dotenv_path="os.env")
# Configuration
class Config:
    AWS_REGION = "us-east-1"
    TABLE_NAME = "Job_Profile"
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    HF_API_KEY = os.getenv("HF_API_KEY")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET")

app.config.from_object(Config)

if __name__ == '__main__':
    # Ensure upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)