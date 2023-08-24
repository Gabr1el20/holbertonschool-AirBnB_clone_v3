#!/usr/bin/python3
"""View routes for city related tasks"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("states/<string:state_id>/cities",
                 strict_slashes=False,)
def get_city_by_state(state_id):
    state_primary = storage.get(State, state_id)
    if state_primary is None:
        abort(404)
    listed_cities = []
    for city in state_primary.cities:
        listed_cities.append(city.to_dict())
    return make_response(jsonify(listed_cities), 200)


@app_views.route("/cities/<string:city_id>", strict_slashes=False)
def get_a_city(city_id):
    new_city = storage.get(City, city_id)
    if new_city is None:
        abort(404)
    storage.save()
    return jsonify(new_city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    city_to_delete = storage.get(City, city_id)
    if city_to_delete is None:
        abort(404)
    city_to_delete.delete()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<string:state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    state_to_check = storage.get(State, state_id)
    if state_to_check is None:
        abort(404)
    new_city = City(**request.get_json())
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<string:city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    city_to_update = storage.get(City, city_id)
    if city_to_update is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_to_update, key, value)
    city_to_update.save()
    return make_response(jsonify(city_to_update.to_dict()), 200)
