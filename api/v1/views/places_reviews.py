#!/usr/bin/python3
"methods for reviews class"
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<string:place_id>/reviews",
                 strict_slashes=False)
def list_of_reviews(place_id):
    listed_reviews = []
    place_to_check = storage.get(Place, place_id)
    if place_to_check is None:
        abort(404)
    for value in storage.all(Review).values():
        if value.place_id == place_to_check.id:
            listed_reviews.append(value.to_dict())
    return jsonify(listed_reviews)


@app_views.route("/reviews/<string:review_id>", strict_slashes=False)
def retrieve_review(review_id):
    review_to_retrieve = storage.get(Review, review_id)
    if review_to_retrieve is None:
        abort(404)
    return jsonify(review_to_retrieve.to_dict())


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    review_to_delete = storage.get(Review, review_id)
    if review_to_delete is None:
        abort(404)
    review_to_delete.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    place_to_review = storage.get(Place, place_id)
    if place_to_review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "user_id" not in request.get_json():
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    user_review = storage.get(User, request.get_json().get('user_id'))
    if user_review is None:
        abort(404)
    if "text" not in request.get_json():
        return make_response(jsonify({"error": "Missing text"}), 400)
    request.get_json()["place_id"] = place_id
    new_review = Review(**request.get_json())
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<string:review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    review_to_update = storage.get(Review, review_id)
    if review_to_update is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review_to_update, key, value)
    storage.save()
    return make_response(jsonify(review_to_update.to_dict()), 200)
