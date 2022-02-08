#!/usr/bin/python3
""" view for Review object that handles
all default RESTFul API actions"""

from api.v1.views import app_views
from models.user import User
from models.review import Review
from models.place import Place
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
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


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ retrieve a review """

    rev = storage.get(Review, review_id)

    if rev is None:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review_by_id(review_id):
    """ delete review """

    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)

    rev.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ create review """

    pl = storage.get(Place, place_id)

    if not place:
        abort(404)

    if request.method == 'POST':
        req_type = request.headers.get('Content-Type')
        if (req_type != 'application/json'):
            return jsonify("Not a JSON"), 400

    req_dict = request.get_json()
    if "user_id" not in req_dict:
        return jsonify("Missing user_id"), 400

    us = storage.get(User, review_dict["user_id"])
    if not us:
        abort(404)

    if "text" not in review_dict:
        return jsonify("Missing text"), 400

    rev_n = Review(**req_dict)
    rev_n.user_id = req_dict["user_id"]
    rev_n.place_id = place_id
    rev_n.save()
    return jsonify(rev_n.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updates review """

    rev = storage.get(Review, review_id)
    if rev is None:
        abort(404)

    req = request.get_json()
    if (not rec):
        abort(400, "Not a JSON")

    for key, val in req.items():
        if (key not in ["id", 'user_id', 'place_id',
                        "created_at", "updated_at"]):
            setattr(rev, key, val)

    re.save()
    return make_response(jsonify(rev.to_dict()), 200)
