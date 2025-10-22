from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .connectors import db
from .models import Water_sample

prediction_bp = Blueprint('prediction', __name__, url_prefix='/predict')

@prediction_bp.route('/result', methods=["POST"])
@login_required
def analyze_water_quality():
    try:
        data = request.get_json()
        new_sample = Water_sample(
            ph=float(data['ph']),
            hardness=float(data['hardness']),
            chloramines=float(data['chloramines']),
            sulfate=float(data['sulfate']),
            organic_carbon=float(data['organic_carbon']),
            trihalomethanes=float(data['trihalomethanes']),
            chemist_id=current_user.id
        )
        db.session.add(new_sample)
        db.session.commit()

        return jsonify({"status": "success"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"}), 500
