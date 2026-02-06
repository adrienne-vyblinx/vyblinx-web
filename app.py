from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'flask_app/templates'),
            static_folder=os.path.join(basedir, 'flask_app/static'))

app.secret_key = os.urandom(24)

from flask_app.routes.auth import auth_bp
from flask_app.routes.merchant import merchant_bp
from flask_app.routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(merchant_bp)
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)