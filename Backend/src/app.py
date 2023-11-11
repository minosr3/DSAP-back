from flask import Flask
from Routes.UsersRoutes import main
from Routes.authRoutes import authMain, status401, status404
#from flask_sqlalchemy import SQLAlchemy
from utils.setup import db, loginManagerApp, csrf
from config import config
from flask_cors import CORS

def createApp(config_name):
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object(config[config_name])

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/dasp_project'
    app.config['SQLALCHEMY_TRACK_MOTIFICATIONS'] = False
    db.init_app(app)

    loginManagerApp.init_app(app)
    csrf.init_app(app)

    # blueprints
    app.register_blueprint(main)
    app.register_blueprint(authMain)

    # Error handlers
    app.register_error_handler(401, status401)
    app.register_error_handler(404, status404)

    return app


