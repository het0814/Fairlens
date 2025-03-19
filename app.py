from flask import Flask
import os
import secrets
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads"
app.secret_key = secrets.token_hex(16)  # This generates a 32-character hexadecimal secret key

# Import route handlers
from routes.home import home_bp
from routes.resume_analyzer import resume_analyzer_bp
from routes.job_profile import job_profile_bp 

# Register blueprints
app.register_blueprint(home_bp)
app.register_blueprint(resume_analyzer_bp, url_prefix='/resume_analyzer')
app.register_blueprint(job_profile_bp) 

# Configuration
class Config:
    AWS_REGION = "us-east-1"
    TABLE_NAME = "Job_Profile"
    
    # API Keys
    OPENAI_API_KEY = "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"
    HF_API_KEY = "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"
    AWS_ACCESS_KEY = 'AKIAW5WU44QWFRJXFF54'
    AWS_SECRET_KEY = '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'

app.config.from_object(Config)

if __name__ == '__main__':
    # Ensure upload directory exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)