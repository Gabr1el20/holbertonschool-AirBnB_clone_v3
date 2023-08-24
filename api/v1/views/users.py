#!/usr/bin/python3
"methods for user class"
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import make_response, jsonify, abort, request


@app_views.route("/users", strict_slashes=False)
def all_users():
    listed_users = []
    for value in storage.all("User").values():
        listed_users.append(value.to_dict())
    return jsonify(listed_users)


@app_views.route("/users/<string:user_id>", strict_slashes=False)
def a_single_user(user_id):
    user_to_retrieve = storage.get(User, user_id)
    if user_to_retrieve is None:
        abort(404)
    return jsonify(user_to_retrieve.to_dict())


@app_views.route("/users/<string:user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    user_to_delete = storage.get(User, user_id)
    if user_to_delete is None:
        abort(404)
    user_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def create_user():
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    new_user = User(**request.get_json())
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<string:user_id", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    user_to_update = storage.get(User, user_id)
    if user_to_update is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_to_update, key, value)
    storage.save()
    return make_response(jsonify(user_to_update.to_dict()), 200)
