from flask import Blueprint, render_template, jsonify
from flask_login import login_required,  current_user


views = Blueprint('views', __name__)
api = Blueprint('api', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@api.route('/api/get_user_info', methods=['GET'])
@login_required
def get_user_info_api():
    return jsonify({'authenticated': True, 'user_id': current_user.id})
print(current_user)
