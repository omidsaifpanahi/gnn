import os

from flask import Blueprint, request, jsonify, make_response, render_template, session,current_app
from api.gnn.utils import mol_file_to_mol, smiles_to_mol, mol_to_tensor_graph, get_model_predictions, draw_molecule
from api.models.molecule import MoleculeModel
from api.middlewares.auth_user import auth_user
from api.utils.print_utils import out

molecule_bp = Blueprint('molecule', __name__)


@molecule_bp.route('/view-list', methods=['GET'])
@auth_user
def view_list_molecules():
    return render_template("molecule/list.html", username=session['username'], title='لیست مولکول ها')


@molecule_bp.route("/list", methods=["GET"])
@auth_user
def list_molecules():
    user_id = request.args.get('user_id')
    page = request.args.get('start', default=0, type=int)
    limit = request.args.get('length', default=10, type=int)
    draw = request.args.get('draw', default=10, type=int)

    molecules = MoleculeModel.fetch_all(page=page, limit=limit, conditions={'user_id': user_id})
    return jsonify([molecule.to_dict() for molecule in molecules]), 200


@molecule_bp.route("/view-add", methods=["GET"])
@auth_user
def new_molecule():
    return render_template("molecule/new.html", username=session['username'], title='مولکول جدید')


@molecule_bp.route("/add", methods=["POST"])
@auth_user
def add_molecule():
    prediction = None
    smiles = request.form.get("smiles")
    mol_file = request.files.get("molFile")
    input_type = request.form.get("inputType")

    print(input_type, smiles)

    if input_type == 'file':
        temp_filename = "temp.mol"
        mol_file.save(temp_filename)
        loaded_molecule = mol_file_to_mol(temp_filename)
    else:
        loaded_molecule = smiles_to_mol(smiles)

    if loaded_molecule:
        image_upload_folder = current_app.config['IMAGE_UPLOAD_FOLDER']

        graph = mol_to_tensor_graph(loaded_molecule)
        prediction = get_model_predictions(graph)

        molecule_image = draw_molecule(loaded_molecule)
        molecule_image_path = os.path.join(image_upload_folder, "molecule.png")
        molecule_image.save(molecule_image_path)

        if prediction == 1:
            prediction = "بله"
        else:
            prediction = "خیر"

    data = {"prediction": prediction}
    response_body = out(data, "مولکول با موفقیت افزوده شد", True)
    response = make_response(jsonify(response_body), 201)
    return response
