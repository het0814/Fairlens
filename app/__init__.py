from flask import Flask
from app.Dashboard import init_dashboard
import boto3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['DYNAMODB'] = boto3.resource('dynamodb', region_name="us-east-1",aws_access_key_id='AKIAYY7NL6Z7E74PS7EG',aws_secret_access_key='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')

    #start dash 
    init_dashboard(app)
    
    # Import and register routes
    from .routes import main
    app.register_blueprint(main)

    return app
