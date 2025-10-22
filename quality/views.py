from flask import Blueprint, render_template, make_response
from flask_login import login_required

main_bp = Blueprint("main", __name__)


def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@main_bp.route("/")
@login_required  
def home():
    resp = make_response(render_template("home.html"))
    return no_cache(resp)

@main_bp.route("/monitoring")
@login_required  
def monitoring():
    resp = make_response(render_template("monitoring.html"))
    return no_cache(resp)

@main_bp.route("/about")
@login_required 
def about():
    resp = make_response(render_template("about.html"))
    return no_cache(resp)

@main_bp.route("/results")
def results():
    resp = make_response(render_template("results.html"))
    return no_cache(resp)


@main_bp.route("/alerts")
@login_required 
def alerts():
    resp = make_response(render_template("alerts.html"))
    return no_cache(resp)


