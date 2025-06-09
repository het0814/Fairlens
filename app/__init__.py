from flask import Flask
from app.Dashboard import init_dashboard
import boto3
from flask_session import Session


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['DYNAMODB'] = boto3.resource('dynamodb', region_name="us-east-1",aws_access_key_id='enter your id here',aws_secret_access_key='enter your key here')
    app.config['AWS_S3_BUCKET'] = 'fairlens'
    app.config['S3_RESOURCE'] = boto3.resource('s3', region_name='us-east-1',aws_access_key_id='enter your id here',aws_secret_access_key='enter your key here')
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = "/tmp/flask_session"
    app.config["SESSION_PERMANENT"] = False
    #start dash 
    init_dashboard(app)
    Session(app)
    
    # Import and register routes
    from .routes import main
    app.register_blueprint(main)

    return app
