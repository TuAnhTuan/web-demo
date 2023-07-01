from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_manager, LoginManager
from datetime import timedelta
from flask import render_template

db = SQLAlchemy()

load_dotenv()
SECRET_KEY = os.environ.get("KEY")
DB_NAME = os.environ.get("DB_NAME")

print(DB_NAME)
def create_database(app):
    if not os.path.exists("todoWeb/" + DB_NAME):
        db.create_all(app=app)
        print("Create DB!!!")
    #else: print("DB existed!!!")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .models import Note, User

    create_database(app)

    from .user import user
    from .view import view
    
    app.register_blueprint(user)
    app.register_blueprint(view)

    login_manager = LoginManager()
    login_manager.login_view="user.login"
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=1)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.errorhandler(404)
    def find_not_found(e):
        return render_template("404.html"), 404 
    return app