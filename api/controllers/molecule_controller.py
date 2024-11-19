import os
from datetime import datetime
import jdatetime
from flask import Blueprint, request, jsonify, make_response, render_template, session,current_app
from api.gnn.utils import mol_file_to_mol, smiles_to_mol, mol_to_tensor_graph, get_model_predictions, draw_molecule
from api.models.molecule import MoleculeModel
from api.middlewares.auth_user import auth_user
from api.utils.print_utils import out
import shutil

molecule_bp = Blueprint('molecule', __name__)


@molecule_bp.route('/view-list', methods=['GET'])
@auth_user
def view_list_molecules():
    return render_template("molecule/list.html", username=session['username'], title='لیست مولکول ها')


@molecule_bp.route("/list", methods=["GET"])
@auth_user
def list_molecules():
    draw         = int(request.args.get('draw', 1))
    start        = int(request.args.get('start', 0))
    length       = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '').strip()

    order_column = request.args.get('order[0][name]', 'id')
    order_dir    = request.args.get('order[0][dir]', 'asc')

    conditions = {'is_delete':0}
    if search_value:
        conditions = {'name': '%'+search_value+'%','is_delete':0}

    page = (start // length) + 1
    limit = length

    molecule_model = MoleculeModel()
    result = molecule_model.fetch_all(draw=draw,page=page, limit=limit, conditions=conditions, order=(order_column, order_dir),is_test=True)

    for row in result['data']:
        if 'created_date' in row and row['created_date']:
            try:
                # بررسی اگر مقدار از نوع datetime است
                if isinstance(row['created_date'], datetime):
                    gregorian_date = row['created_date']
                else:
                    gregorian_date = datetime.strptime(row['created_date'], "%a, %d %b %Y %H:%M:%S %Z")
                
                # تبدیل تاریخ میلادی به شمسی
                jalali_date = jdatetime.datetime.fromgregorian(datetime=gregorian_date)
                row['created_date'] = jalali_date.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                row['created_date'] = "فرمت تاریخ نامعتبر است"

    return jsonify(result), 200


@molecule_bp.route("/view-add", methods=["GET"])
@auth_user
def new_molecule():
    return render_template("molecule/new.html", username=session['username'], title='مولکول جدید')


@molecule_bp.route("/add", methods=["POST"])
@auth_user
def add_molecule():
    prediction = None
    name = request.form.get("name")
    smiles = request.form.get("smiles")
    mol_file = request.files.get("mol_file")
    input_type = request.form.get("input_type")

    print(input_type, smiles)

    if input_type == 'file':
        temp_filename = "temp.mol"
        mol_file.save(temp_filename)
        loaded_molecule = mol_file_to_mol(temp_filename)
    else:
        loaded_molecule = smiles_to_mol(smiles)

    if loaded_molecule:
        image_upload_folder = current_app.config['IMAGE_UPLOAD_FOLDER']
        mol_upload_folder   = current_app.config['MOL_UPLOAD_FOLDER']

        graph          = mol_to_tensor_graph(loaded_molecule)
        prediction     = get_model_predictions(graph)
        molecule_image = draw_molecule(loaded_molecule)

        molecule_model = MoleculeModel()
        result = molecule_model.create({
            'input_type':input_type,
            'name':name,
            'smiles':smiles,
            "prediction": prediction
            },'name')
        
        if prediction == 1:
            prediction = "بله"
        else:
            prediction = "خیر"


        if(result['success']==False):
            response_body = out({}, result['msg'], False)
            response = make_response(jsonify(response_body), 400)
            return response

        mol_file_name = f"{result['id']}.mol"
        mol_file_path = os.path.join(mol_upload_folder, mol_file_name)

        shutil.move(temp_filename, mol_file_path)

        image_name = str(result['id'])+".png"
        molecule_image_path = os.path.join(image_upload_folder,image_name )
        molecule_image.save(molecule_image_path)

        data = {
            "prediction": prediction,
            "id" : result['id'],
            "image" : '/'+image_upload_folder+image_name
        }
        response_body = out(data, "مولکول با موفقیت افزوده شد", True)
        response = make_response(jsonify(response_body), 201)
    else:
        response_body = out({}, "خطا", False)
        response = make_response(jsonify(response_body), 400)

    return response

@molecule_bp.route('/edit/<int:molecule_id>', methods=['GET'])
@auth_user
def edit_molecule(molecule_id):
    molecule_model = MoleculeModel()
    result = molecule_model.read({'id': molecule_id})
    return render_template("molecule/edit.html", username=session['username'], title='ویرایش مولکول '+str(molecule_id),data=result)

@molecule_bp.route('/delete/<int:molecule_id>', methods=['DELETE'])
@auth_user
def delete_molecule(molecule_id):
    molecule_model = MoleculeModel()
    deleted_count = molecule_model.delete({'id': molecule_id})
    if deleted_count > 0:
        response_body = out({}, 'مولکول با موفقیت حذف شد.', True)
        response = make_response(jsonify(response_body), 200)
    else:
        response_body = out({}, 'مولکول یافت نشد یا حذف نشد.', False)
        response = make_response(jsonify(response_body), 404)

    return response