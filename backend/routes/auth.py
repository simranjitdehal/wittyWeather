from flask import Blueprint, request, jsonify, render_template, redirect, session, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta


auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not email or not password or not confirm_password:
        return jsonify({"msg":"All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"msg":"Passwords do not match"}), 400

    # check if username/email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"msg":"Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"msg":"Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg":"User created successfully!"}), 201

#login route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username=data.get("username")
    password = data.get("password")

    if not (username) or not password:
        return jsonify({"msg":"Username or email and password required"}), 400
    
    user = None
    if username:
        user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "User not registered in Database"}), 400
    
    if not check_password_hash(user.password_hash, password):
        return jsonify({"msg":"Invalid password or username"}), 400
    
    #create JWT token
    token = create_access_token(identity=username)
    return jsonify({"access_token": token}), 200

#logout rout
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # session.pop("user", None)  # remove session
    return {"msg": "Logged out successfully"}, 200