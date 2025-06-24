# Routes API (GET / POST / FILTER / etc....)

from flask import Blueprint, jsonify, request
from services.accident_service import fetch_accidents, filter_by_year

accident_bp = Blueprint("accidents", __name__)

@accident_bp.route("/", methods=["GET"])
def get_all():
    data = fetch_accidents()
    return jsonify(data)

@accident_bp.route("/year/<int:year>", methods=["GET"])
def get_by_year(year):
    data = filter_by_year(year)
    return jsonify(data)
