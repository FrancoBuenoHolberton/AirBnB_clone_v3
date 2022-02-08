#!/usr/bin/python3
""" view for Review object that handles
all default RESTFul API actions"""

from api.v1.views import app_views
from models.user import User
from models.review import Review
from models.place import Place
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'])
def all_reviews(place_id):
    """ retrieves the list all review """

    pl = storage.get(Place, place_id)
    if not pl:
        abort(404)

    if request.method == 'GET':
        req = storage.all(Review).values()
        ls = []
        for re in req:
            if re.place_id == place_id:
                ls.append(re.to_dict())

        return jsonfy(ls)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'])
def get_review(review_id):
    """ retrieve a review """

    rev = storage.get(Review, review_id)
    if not rev:
        abort(404)

    if request.method == 'GET':
        return jsonify(rev.to_dict())


@app_views.route('/place_id/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review_by_id(review_id):
    """ delete review """

    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'])
def create_review(place_id):
    """ create review """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400

        revi_dic = request.get_json()
        if "user_id" not in rev_dic:
            return jsonify("Missing user_id"), 400

        user = storage.get(User, revi_dic["user_id"])
        if not user:
            abort(404)

        if "text" not in rev_dic:
            return jsonify("Missing text"), 400

        n_rev = Review(**rev_dic)
        n_rev.user_id = rev_dic["user_id"]
        n_rev.place_id = place_id
        n_rev.save()
        return jsonify(n_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'])
def update_review(review_id):
    """ updates review """

    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)

    if request.method == 'PUT':

        content_type = request.headers.get('Content-Type')
        if (content_type != 'application/json'):
            return jsonify("Not a JSON"), 400

        review_dict = request.get_json()
        try:
            review.text = review_dict["text"]
            storage.save()

        except Exception as err:
            print(err)

        return jsonify(review.to_dict()), 200
