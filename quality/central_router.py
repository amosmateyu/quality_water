
from .auth import auth_bp
from .views import main_bp  
from .monitoring import prediction_bp
from .results import analysis_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/home")
    app.register_blueprint(prediction_bp, url_prefix="/predict")
    app.register_blueprint(analysis_bp, url_prefix="/analysis")
