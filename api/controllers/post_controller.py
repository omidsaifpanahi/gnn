from flask import Blueprint, request, jsonify,render_template,session,make_response
from api.middlewares.auth_admin import auth_admin
from api.models.post import PostModel
from api.utils.print_utils import out

post_bp = Blueprint('post', __name__)

@post_bp.route('/view-list', methods=['GET'])
@auth_admin
def list_molecules():
    return render_template("molecule/list.html", username=session['username'], title='لیست مولکول ها')


@post_bp.route('/list', methods=['GET'])
def list_posts():
    draw         = int(request.args.get('draw', 1))
    start        = int(request.args.get('start', 0))
    length       = int(request.args.get('length', 10))
    search_value = request.args.get('search[value]', '').strip()

    order_column = request.args.get('order[0][column]', '0')
    order_dir    = request.args.get('order[0][dir]', 'asc')
    order_column_name = 'column_name'

    conditions = {}
    if search_value:
        conditions = {'title': search_value}

    page = (start // length) + 1
    limit = length

    result = PostModel.fetch_all(draw=draw,page=page, limit=limit, conditions=conditions, order=(order_column_name, order_dir))

    return jsonify(result), 200


@post_bp.route("/view-add", methods=["GET"])
@auth_admin
def new_post():
    return render_template("post/form.html", username=session['username'], title='پست جدید')


@post_bp.route('/add', methods=['POST'])
@auth_admin
def add_post():
    title = request.form.get("title")
    description = request.files.get("description")
    tags = request.files.get("tags")
    post = PostModel.create({  'title' : title, 'description':description , 'tags' : tags })
    return jsonify({'message': 'پست با موفقیت افزوده شد'}), 201