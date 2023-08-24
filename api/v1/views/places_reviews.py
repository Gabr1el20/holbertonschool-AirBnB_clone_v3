#!/usr/bin/python3
"methods for reviews class"
from api.v1.views import app_views
from flask import abort, request, make_response, jsonify
from models import storage
from models.review import Review
from models.place import Place


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
