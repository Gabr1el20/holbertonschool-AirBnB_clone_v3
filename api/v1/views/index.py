#!/usr/bin/python3
"""Returns a jsoned status"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def jsoned():
    return jsonify({"status": "OK"})


cls_dict = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/stats")
def stats():
    """_summary_
    """
    dicted = {}
    for key, value in cls_dict.items():
        dicted[key] = storage.count(value)
    return jsonify(dicted)
