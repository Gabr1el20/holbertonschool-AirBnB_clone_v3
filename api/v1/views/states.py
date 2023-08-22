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
def post_new_state():
    