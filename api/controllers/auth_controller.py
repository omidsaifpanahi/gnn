from flask import request, redirect, url_for, session,Blueprint,render_template
from api.models.user import UserModel
from api.controllers.dashboard_controller import dashboard_bp
auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_model = UserModel()

    user = user_model.validate(username, password)

    if user:
        session['logged_in'] = True
        session['username']  = user['username']
        session['user_id']   = user['id']
        session['role']      = user['role']
        return redirect("/dashboard")
        # return redirect(url_for("dashboard_bp.dashboard"))
    else:
        return render_template("index.html",error='نام کاربری یا رمز عبور اشتباه است')
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")