#!/usr/bin/python3
"""Returns a jsoned status"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def jsoned():
    return jsonify({"status": "OK"})
