from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vyblinx-dev-secret-key-2024'
    
    from flask_app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app