#!/usr/bin/python3
""" view for City objects that handles
alll default RESTFul API actions """

from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import Flask, jsonify, abort, request, make_response
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """ List of all cities """
    stor = storage.get(State, state_id)
    states_cities = []
    if not stor:
        abort(404)

    if request.method == 'GET':
        for citys in stor.cities:
            states_cities.append(citys.to_dict())
    return jsonify(states_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """ retrive a citie object """

    ct = storage.get(City, city_id)

    if ct is None:
        abort(404)

    return jsonify(ct.to_dict())


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city_id(city_id):
    """ Delete a city object """

    ct = storage.get(City, city_id)

    if ct is None:
        abort(404)

    storage.delete(ct)
    storage.save()
    return jsonify(({}), 200)


@app_views.route('/states/<string:state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ create city """

    sta = storage.get(State, state_id)
    if (not sta):
        abort(404)

    req = request.get_json()
    if (not req):
        abort(400, 'Not a JSON')

    if ('name' not in req):
        abort(400, 'Missing name')

    ct = City(**req)
    ct.state_id = sta.id
    ct.save()
    return make_response(jsonify(ct.to_dict()), 201)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update cities """

    ct = storage.get(City, city_id)
    if ct is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for key, val in request.get_json().items():
        if (key not in ["id", "created_at", "updated_at"]):
            setattr(ct, key, val)

    ct.save()
    return make_response(jsonify(ct.to_dict()), 200)
