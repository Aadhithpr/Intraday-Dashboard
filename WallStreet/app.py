from os import path
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = "database.db"
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'blendnetai'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    login_manager.init_app(app)

    from WallStreet.views import views, api
    from WallStreet.auth import auth
    from WallStreet.models import User

    @api.route('/get_user_info', methods=['GET','POST'])
    def get_user_info():
        if current_user.is_authenticated:
            return jsonify({'authenticated': True, 'user_id': current_user.id})
        else:
            return jsonify({'authenticated': False})

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api/')

    with app.app_context():
        db.create_all()

    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('WallStreet/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


if __name__ == "__main__":
    app = create_app()
    create_database(app)
    app.run(debug=True)
