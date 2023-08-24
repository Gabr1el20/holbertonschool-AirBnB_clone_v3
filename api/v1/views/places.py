#!/usr/bin/python3
"HTTP methods for place class"
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
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


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    place_to_delete = storage.get(Place, place_id)
    if place_to_delete is None:
        abort(404)
    place_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<string:city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    city_to_attach = storage.get(City, city_id)
    if city_to_attach is None:
        abort(404)
    user_to_attach = storage.get(User, request.get_json()['user_id'])
    if user_to_attach is None:
        abort(404)
    request.get_json()['city_id'] = city_id
    new_place = Place(**request.get_json())
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=["PUT"],
                 strict_slashes=False)
def update_place(place_id):
    place_to_update = storage.get(Place, place_id)
    if place_to_update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json():
        if key not in ["id", "user_id", "created_at", "updated_at"]:
            setattr(place_to_update, key, value)
    storage.save()
    return make_response(jsonify(place_to_update.to_dict()), 200)
