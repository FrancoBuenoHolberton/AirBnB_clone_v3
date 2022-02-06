#!/usr/bin/python3
""" view for Place objects that handles
all default RESTFul API actions """

from api.v1.views import app_views
from models.city import City
from models.user import User
from models.place import Place
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def all_places(city_id):
    """ list all places """

    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)

    ls = []
    for pl in ct.places:
        ls.append(pl.to_dict())

    return jsonify(ls)


@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ retrive a place """

    pl = storage.get(Place, place_id)

    if pl is None:
        abort(404)

    return jsonify(pl.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ delete a place """

    pl = storage.get(Place, place_id)

    if pl is None:
        abort(404)

    pl.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """create placq """

    req = request.get_json()

    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)

    if (not req):
        abort(400, 'Not a JSON')

    if ('user_id' not in req):
        abort(400, 'Missing user_id')

    us = storage.get(User, req['user_id'])
    if us is None:
        abort(404)

    if ('name' not in req):
        abort(400, 'Missing name')

    req['city_id'] = city_id
    pl = Place(**req)
    pl.save()
    return make_response(jsonify(pl.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ update place """

    pl = storage.get(Place, place_id)
    if pl is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for key, val in request.get_json().items():
        if (key not in ["id", "user_id", "city_id", "created_at", "updated_at"]):
            setattr(pl, key, val)

    pl.save()
    return jsonify(pl.to_dict())
