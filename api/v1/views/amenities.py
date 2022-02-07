#!/usr/bin/python3
""" view for Amenity objects that handles
all default RESTFul API actions """

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_my_amenities():
    """ list of all Amenity objects: GET /api/v1/amenities """

    am = storage.all(Amenity)

    ls = []
    for key in am.values():
        ls.append(key.to_dict())

    return jsonify(ls)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ retrive amenity object """

    am = storage.get(Amenity, amenity_id)
    if am is None:
        abort(404)

    return jsonify(am.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """ delete a amenity object """

    am = storage.get(Amenity, amenity_id)

    if am is None:
        abort(404)

    storage.delete(am)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ create Amenity """

    req = request.get_json()
    if (not req):
        abort(400, 'Not a JSON')

    if ('name' not in req):
        abort(400, 'Missing name')

    am = Amenity(**req)
    am.save()
    return make_response(jsonify(am.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ update amenity """

    am = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for key, val in request.get_json().items():
        if (key not in ["id", "created_at", "updated_at"]):
            setattr(am, key, val)

    storage.save()
    return jsonify(am.to_dict())
