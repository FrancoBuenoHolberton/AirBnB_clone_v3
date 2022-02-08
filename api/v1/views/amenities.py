#!/usr/bin/python3
""" view for Amenity objects that handles
all default RESTFul API actions """

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def all_my_amenities():
    """ list of all Amenity objects: GET /api/v1/amenities """
    if request.method == 'GET':
        am = storage.all(Amenity).values()
        ls = []
        for key in am:
            ls.append(key.to_dict())
    return jsonify(ls)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ retrive amenity object """
    if request.method == 'GET':
        am = storage.get(Amenity, amenity_id)
        if am is not None:
            return jsonify(am.to_dict())
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """ delete a amenity object """
    if request.method == 'DELETE':
        am = storage.get(Amenity, amenity_id)
        if am is not None:
            storage.delete(am)
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ create Amenity """
    if request.method == 'POST':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        req_name = request.get_json()
        if 'name' not in req_name:
            return jsonify('Missing name'), 400
        am = Amenity(**dict_req_name)
        am.save()
        return jsonify(am.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ update amenity """
    if request.method == 'PUT':
        am = storage.get(Amenity, amenity_id)
        req = request.headers.get('Content-Type')
        if req != 'application/json':
            return jsonify('Not a JSON'), 400
        req_two = request.get_json()
        if am is not None:
            if 'name' in req_two:
                am.name = req_two['name']
                am.save()
                return jsonify(am.to_dict()), 200
