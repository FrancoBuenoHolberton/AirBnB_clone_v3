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
    if pl is None:
        abort(404)

    req = request.get_json()
    if (not req):
        abort(400, 'Not a JSON')

    if ('user_id' not in req):
        abort(400, 'Missing user_id')

    us = storage.get(User, ['user_id'])
    if us is None:
        abort(404)

    if ('text' not in req):
        abort(400, 'Missing text')

    req['place_id'] = place_id
    rev = Review(**req)
    rev.save()
    return make_response(jsonify(rev.to_dict()), 201)


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
