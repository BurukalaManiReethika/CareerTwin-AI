from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from models import db, User, JobApplication

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///career_twin.db'
app.config['JWT_SECRET_KEY'] = 'career_twin_secret'

db.init_app(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
