from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://recg_user:recg_pass@localhost/face_recg_db'
db = SQLAlchemy(app)

from app import routes
