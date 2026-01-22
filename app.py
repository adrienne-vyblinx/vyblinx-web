from flask import Flask
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'flask_app/templates'),
            static_folder=os.path.join(basedir, 'flask_app/static'))

app.secret_key = os.urandom(24)

from flask_app.routes.auth import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)