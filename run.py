from flask import Flask, redirect, url_for, session,render_template
from api.controllers.molecule_controller import molecule_bp
from api.controllers.auth_controller import auth_bp
from api.controllers.user_controller import user_bp
from api.controllers.post_controller import post_bp
from api.controllers.dashboard_controller import dashboard_bp
from dotenv import load_dotenv
import os

load_dotenv('.env')

IMAGE_UPLOAD_FOLDER = 'static/images/'
if not os.path.exists(IMAGE_UPLOAD_FOLDER):
    os.makedirs(IMAGE_UPLOAD_FOLDER)

MOL_UPLOAD_FOLDER = 'static/mols/'
if not os.path.exists(MOL_UPLOAD_FOLDER):
    os.makedirs(MOL_UPLOAD_FOLDER)


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER
    app.config['MOL_UPLOAD_FOLDER'] = MOL_UPLOAD_FOLDER

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(molecule_bp, url_prefix='/molecule')
    app.register_blueprint(post_bp, url_prefix='/post')

    @app.route('/')
    def index():
        if 'user_id' not in session:
            return render_template("index.html")
        return redirect('/dashboard')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, port=3000)
