from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import SqlConfig

print("------初始化中-----")
app = Flask(__name__)
app.config.from_object(SqlConfig)
db = SQLAlchemy(app)
def create_app():
    return app

# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SECRET_KEY'] = "1qaz@WSX#EDC

def create_db():

    # print("调用绑定app后的db")
    return db

def create_migrate():
    db = create_db()
    migrate = Migrate(app, db)
    # print("调用绑定app与db后migrate")
    return migrate