from flask import Flask, request, jsonify, render_template, redirect, session, url_for
import requests
from flask_cors import CORS
from config import OPENWEATHER_API_KEY
from jokes import temp_jokes, wind_jokes, humidity_jokes, cloud_jokes
import random
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from dotenv import load_dotenv
import os
from routes.auth import auth_bp
from routes.weather import weather_bp
from datetime import timedelta
from database import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8000"}}, supports_credentials=True)
# CORS(app)
load_dotenv

# Database config from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")

db_name = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.config["JWT_SECRET_KEY"] = "JWT_SECRET_KEY"


jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(weather_bp)


with app.app_context():
    db.create_all()
    print("✅ Users table created!")

# ------------------------
# Flask routes
# ------------------------
@app.route("/")
@jwt_required
def home():
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        return render_template("index.html", username=current_user)
    except NoAuthorizationError:
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
