from flask import render_template, session,Blueprint
from api.middlewares.auth_user import auth_user
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/")
@auth_user
def dashboard():
    return render_template("dashboard.html", username=session['username'], title='آمار')
