from flask import render_template, session,Blueprint
from api.models.molecule import MoleculeModel
from api.middlewares.auth_user import auth_user
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route("/")
@auth_user
def dashboard():
    molecule_model = MoleculeModel()
    result = molecule_model.fetch_all(draw=1,page=1, limit=1, conditions={'prediction': 1,'is_delete':0})

    return render_template("dashboard.html", username=session['username'], title='آمار',data=result)
