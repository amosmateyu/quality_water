
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Water_sample
import joblib
import pandas as pd

analysis_bp = Blueprint("analysis_bp", __name__)



def check_water(data):
    normal, abnormal, recommendations = [], [], []

    if 6.5 <= data['ph'] <= 8.5:
        normal.append("pH")
    else:
        abnormal.append("pH")
        recommendations.append("Adjust pH between 6.5 and 8.5")

    if data['hardness'] <= 500:
        normal.append("Hardness")
    else:
        abnormal.append("Hardness")
        recommendations.append("Reduce hardness below 500 mg/L")

    if data['chloramines'] <= 4:
        normal.append("Chloramines")
    else:
        abnormal.append("Chloramines")
        recommendations.append("Keep chloramines below 4 mg/L")

    if data['sulfate'] <= 250:
        normal.append("Sulfate")
    else:
        abnormal.append("Sulfate")
        recommendations.append("Keep sulfate below 250 mg/L")

    if data['trihalomethanes'] <= 80:
        normal.append("Trihalomethanes")
    else:
        abnormal.append("Trihalomethanes")
        recommendations.append("Keep trihalomethanes below 80 µg/L")

    if data['organic_carbon'] <= 2:
        normal.append("Organic Carbon")
    else:
        abnormal.append("Organic Carbon")
        recommendations.append("Keep organic carbon below 2 mg/L")

    who_status = "Safe" if not abnormal else "Not Safe"

    return {
        "normal": normal,
        "abnormal": abnormal,
        "recommendations": recommendations,
        "who_status": who_status
    }

def predict(data):
    input_df = pd.DataFrame([{
        "Chloramines": data['chloramines'],
        "Sulfate": data['sulfate'],
        "ph": data['ph'],
        "Trihalomethanes": data['trihalomethanes'],
        "Organic_carbon": data['organic_carbon'],
        "Hardness": data['hardness']
    }])

    model = joblib.load("water_quality.pkl")
    pred = model.predict(input_df)[0]

    prediction = "Safe" if pred == 1 else "Not Safe"
    return {"prediction": prediction}


def final_status(check_results, model_prediction):
    if check_results["who_status"] == "Safe" and model_prediction["prediction"] == "Safe":
        return "Safe"
    return " Not Safe"


@analysis_bp.route("/water", methods=["GET"])
def analyze_water():
   
    sample_obj = Water_sample.query.filter_by(chemist_id=current_user.id)\
     .order_by(Water_sample.id.desc()).first()

    sample = {
     "chloramines": sample_obj.chloramines,
     "sulfate": sample_obj.sulfate,
     "ph": sample_obj.ph,
     "trihalomethanes": sample_obj.trihalomethanes,
     "organic_carbon": sample_obj.organic_carbon,
     "hardness": sample_obj.hardness
    }
    


    check_results = check_water(sample)
    model_prediction = predict(sample)
    final = final_status(check_results, model_prediction)

    return jsonify({
        "sample": sample,
        "check_results": check_results,
        "final_status": final
    })



