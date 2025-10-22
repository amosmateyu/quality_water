# auth.py
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from .models import Chemist
from .connectors import db
import re

auth_bp = Blueprint("auth", __name__)

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com|hotmail\.com)$")

def safe_json_response(status, message, code):
    return jsonify({"status": status, "message": message}), code

def is_valid_email(email):
    return bool(email and EMAIL_PATTERN.match(email))

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    try:
        data = request.get_json(silent=True) or request.form
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return safe_json_response("error", "Email and password are required.", 400)
        if not is_valid_email(email):
            return safe_json_response("error", "Invalid email. Only Gmail, Outlook, or Hotmail allowed.", 400)

        user = Chemist.query.filter_by(email=email).first()
        if not user:
            return safe_json_response("error", "Email not found!", 404)
        if not check_password_hash(user.password, password):
            return safe_json_response("error", "Invalid credentials!", 401)

        login_user(user)
        return safe_json_response("success", "Login successful!", 200)

    except SQLAlchemyError as e:
        db.session.rollback()
        return safe_json_response("error", f"Database error: {str(e)}", 500)
    except Exception as e:
        return safe_json_response("error", f"Unexpected error: {str(e)}", 500)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("account.html")
    try:
        data = request.get_json(silent=True) or request.form
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return safe_json_response("error", "Email and password are required.", 400)
        if not is_valid_email(email):
            return safe_json_response("error", "Invalid email. Only Gmail, Outlook, or Hotmail allowed.", 400)

        existing_user = Chemist.query.filter_by(email=email).first()
        if existing_user:
            return safe_json_response("error", "Email already exists.", 409)

        new_user = Chemist(email=email, password=generate_password_hash(password, method="pbkdf2:sha256"))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return safe_json_response("success", "Account created successfully!", 201)

    except SQLAlchemyError as e:
        db.session.rollback()
        return safe_json_response("error", f"Database error: {str(e)}", 500)
    except Exception as e:
        return safe_json_response("error", f"Unexpected error: {str(e)}", 500)


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("reset_password.html")
    
    try:
        data = request.get_json(silent=True) or request.form
        email = data.get("email")
        new_password = data.get("new_password")  # <-- match JS field name

        if not email or not new_password:
            return safe_json_response("error", "Email and new password are required.", 400)
        
        if not is_valid_email(email):
            return safe_json_response("error", "Invalid email. Only Gmail, Outlook, or Hotmail allowed.", 400)

        user = Chemist.query.filter_by(email=email).first()
        if not user:
            return safe_json_response("error", "Email not found.", 404)

        # Optional: add password length check
        if len(new_password) < 6:
            return safe_json_response("error", "Password must be at least 6 characters long.", 400)

        user.password = generate_password_hash(new_password, method="pbkdf2:sha256")
        db.session.commit()
        return safe_json_response("success", "Password changed successfully!", 200)

    except SQLAlchemyError as e:
        db.session.rollback()
        return safe_json_response("error", f"Database error: {str(e)}", 500)
    except Exception as e:
        return safe_json_response("error", f"Unexpected error: {str(e)}", 500)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
