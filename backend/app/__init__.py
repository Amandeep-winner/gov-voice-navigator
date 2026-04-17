from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    CORS(app) # Allow Vue frontend and Vapi to communicate with the API

    # Database Configuration
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    sqlite_dir = os.path.join(basedir, 'data', 'sqlite')
    os.makedirs(sqlite_dir, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(sqlite_dir, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        # Import models here so they register before create_all
        from app.models import user, forum, notification
        db.create_all()

    # Register Blueprints
    from app.routes.vapi_routes import vapi_bp
    from app.routes.user_routes import user_bp
    from app.routes.forum_routes import forum_bp
    from app.routes.assistant_routes import assistant_bp

    app.register_blueprint(vapi_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(forum_bp, url_prefix='/api')
    app.register_blueprint(assistant_bp, url_prefix='/api')

    # Initialize Background Scheduler
    from apscheduler.schedulers.background import BackgroundScheduler
    from app.services.scanner import check_expiring_schemes
    
    scheduler = BackgroundScheduler()
    # Run the job every 10 minutes in prototyping (normally daily)
    scheduler.add_job(func=lambda: check_expiring_schemes(app), trigger="interval", minutes=10)
    scheduler.start()

    # Ensure scheduler shuts down when app exits
    import atexit
    atexit.register(lambda: scheduler.shutdown(wait=False))

    return app