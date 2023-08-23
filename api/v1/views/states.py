#!/usr/bin/python3
"""_summary_"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import Flask, jsonify, make_response, abort, request


@app_views.route("/states", strict_slashes=False)
def states():
    listed_states = []
    for state in storage.all(State).values():
        listed_states.append(state.to_dict())
    return jsonify(listed_states)


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def state_by_id(state_id):
    for k, instance in storage.all(State).items():
        if instance.id == state_id:
            return jsonify(instance.to_dict())
    abort(404)


@app_views.route("/states/<string:state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    obtained_state = storage.get(State, state_id)
    if obtained_state is not None:
        obtained_state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def post_state():
    if request.get_json() is None:
        return jsonify({"error": "Not a JSON"}, 400)
    if "name" not in request.get_json():
        return jsonify({"error": "Missing name"}, 400)
    new_state = State(**request.get_json())
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", strict_slashes=False,
                 methods=["PUT"])
def update_state(state_id):
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}, 400)
    new_state = storage.get(State, state_id)
    if new_state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(new_state, key, value)
    storage.save()
    return jsonify(new_state.to_dict(), 200)
