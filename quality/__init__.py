from flask import Flask, redirect, url_for
from .connectors import db, login_manager, init_extensions
from .central_router import register_blueprints
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # Initialize extensions
    init_extensions(app)

    # Setup database migration
    migrate = Migrate(app, db)

    # Register blueprints
    register_blueprints(app)

    # Import models AFTER db is initialized
    from .models import Chemist,  Water_sample

    @login_manager.user_loader
    def load_user(user_id):
        return Chemist.query.get(int(user_id))

    # Redirect root to login
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
