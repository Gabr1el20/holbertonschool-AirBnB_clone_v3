#!/usr/bin/python3
"""View routes for city related tasks"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort
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
