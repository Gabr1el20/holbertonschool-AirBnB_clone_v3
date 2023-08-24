#!/usr/bin/python3
"HTTP methods for place class"
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import jsonify, make_response, request, abort


@app_views.route("cities/<string:city_id>/places",
                 strict_slashes=False)
def list_places_of_city(city_id):
    listed_places = []
    new_city = storage.get(City, city_id)
    if new_city is None:
        abort(404)
    for place in storage.all(Place).values():
        if place.city_id == new_city.id:
            listed_places.append(place.to_dict())
    return jsonify(listed_places)


@app_views.route("/places/<string:place_id>",
                 strict_slashes=False)
def retrieve_a_place(place_id):
    new_place = storage.get(Place, place_id)
    if new_place is None:
        abort(404)
    return jsonify(new_place.to_dict())
