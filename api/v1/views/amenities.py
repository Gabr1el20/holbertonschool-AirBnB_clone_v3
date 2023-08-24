#!/usr/bin/python3
"Methods for amenity class"
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import place_amenity
from flask import request, jsonify, abort, make_response


@app_views.route("/amenities", strict_slashes=False)
def retrieve_amenities():
    listed_amenities = []
    for value in storage.all(Amenity).values():
        listed_amenities.append(value.to_dict())
    return jsonify(listed_amenities)


@app_views.route("/amenities/<string:amenity_id>",
                 strict_slashes=False)
def retrieve_amenity(amenity_id):
    amenity_to_retrieve = storage.get(Amenity, amenity_id)
    if amenity_to_retrieve is None:
        abort(404)
    return jsonify(amenity_to_retrieve.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity_to_delete = storage.get(Amenity, amenity_id)
    if amenity_to_delete is None:
        abort(404)
    amenity_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    new_amenity = storage.get(Amenity, amenity_id)
    if new_amenity is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(new_amenity, key, value)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 200)
