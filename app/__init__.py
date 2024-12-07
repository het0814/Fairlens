from flask import Flask
from app.Dashboard import init_dashboard

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['UPLOAD_FOLDER'] = 'uploads'

    #start dash 
    init_dashboard(app)
    
    # Import and register routes
    from .routes import main
    app.register_blueprint(main)

    return app
