#!/usr/bin/python3
"methods for user class"
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import make_response, jsonify, abort, request


@app_views.route("/users", strict_slashes=False)
def all_users():
    listed_users = []
    for value in storage.all(User).values():
        listed_users.append(value.to_dict())
    return jsonify(listed_users)

@app_views.route("/users/<string:user_id>", strict_slashes=False)
def a_single_user(user_id):
    user_to_retrieve = storage.get(User, user_id)
    if user_to_retrieve is None:
        abort(404)
    return jsonify(user_to_retrieve.to_dict())
