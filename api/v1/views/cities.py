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
    for city in storage.all(City).values():
        if city.get('id') == state_primary.id:
            listed_cities.append(city.to_dict())
    return jsonify(listed_cities)
