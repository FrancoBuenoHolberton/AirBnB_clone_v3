#!/usr/bin/python3
""" view for Review object that handles
all default RESTFul API actions"""

from api.v1.views import app_views
from models.user import User
from models.review import Review
from models.place import Place
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """ list all Review"""

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        all_reviews = storage.all(Review).values()
        place_reviews = []
        for review in all_reviews:
            if review.place_id == place_id:
                place_reviews.append(review.to_dict())
        return jsonify(place_reviews)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_reviews(place_id):
    """ Creates a review """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400
        review_dict = request.get_json()
        if "user_id" not in review_dict:
            return jsonify("Missing user_id"), 400
        user = storage.get(User, review_dict["user_id"])
        if not user:
            abort(404)
        if "text" not in review_dict:
            return jsonify("Missing text"), 400
        new_review = Review(**review_dict)
        new_review.user_id = review_dict["user_id"]
        new_review.place_id = place_id
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_id(review_id):
    """ Retrieves a review """

    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """  Updates a review """

    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'PUT':
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400
        review_dict = request.get_json()
        try:
            review.text = review_dict["text"]
            storage.save()
        except Exception as e:
            print(e)
        return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a review """

    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
