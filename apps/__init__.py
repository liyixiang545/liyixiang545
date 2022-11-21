from flask import (
    Flask)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import SqlConfig
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(SqlConfig)

def create_app():
    return app

def create_db():
    db = SQLAlchemy(app)
    db.init_app(app)
    return db

def create_migrate():
    db = create_db()
    migrate = Migrate(app,db)
    return migrate

def create_mail():
    mail = Mail(app)
    return mail