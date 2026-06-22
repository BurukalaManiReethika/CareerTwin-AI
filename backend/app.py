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


@app.route('/register', methods=['POST'])
def register():

    data = request.json

    hashed_password = bcrypt.generate_password_hash(
        data['password']
    ).decode('utf-8')

    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User Registered Successfully"
    })


@app.route('/login', methods=['POST'])
def login():

    data = request.json

    user = User.query.filter_by(
        email=data['email']
    ).first()

    if not user:
        return jsonify({
            "message": "User Not Found"
        }), 404

    if bcrypt.check_password_hash(
        user.password,
        data['password']
    ):

        token = create_access_token(
            identity=user.id
        )

        return jsonify({
            "token": token
        })

    return jsonify({
        "message": "Invalid Credentials"
    }), 401


@app.route('/add-job', methods=['POST'])
@jwt_required()
def add_job():

    current_user = get_jwt_identity()

    data = request.json

    job = JobApplication(
        company=data['company'],
        role=data['role'],
        status=data['status'],
        user_id=current_user
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job Added"
    })


@app.route('/jobs')
@jwt_required()
def jobs():

    current_user = get_jwt_identity()

    job_list = JobApplication.query.filter_by(
        user_id=current_user
    )

    results = []

    for job in job_list:
        results.append({
            "company": job.company,
            "role": job.role,
            "status": job.status
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
