#!/usr/bin/python3
""" Manage STates """

from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def all_state():
    """ List of all State objects: GET /api/v1/states """

    if request.method == 'GET':

        ls = []
        for sta in storage.all(State).values():
            ls.append(sta.to_dict())

        return jsonify(ls)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object:
    GET /api/v1/states/<state_id> """

    if request.method == 'GET':

        if storage.get(State, state_id) is not None:

            return jsonify(storage.get(State, state_id).to_dict())
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_id(state_id):
    """ Deletes a State object """

    if request.method == 'DELETE':

        if storage.get(State, state_id) is not None:

            storage.delete(storage.get(State, state_id))
            storage.save()

            return jsonify({}), 200
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """ creates State"""

    if request.method == 'POST':

        req = request.headers.get('Content-Type')

        if req != 'application/json':
            return jsonify('Not a JSON'), 400

        req_name = request.get_json()

        if 'name' not in req_name:
            return jsonify('Missing name'), 400

        new_sta = State(**req_name)

        new_sta.save()
        return jsonify(new_sta.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates state """

    if request.method == 'PUT':

        req = request.headers.get('Content-Type')

        if req != 'application/json':
            return jsonify('Not a JSON'), 400

        up_req = request.get_json()

        if storage.get(State, state_id) is not None:

            if 'name' in up_req:
                storage.get(State, state_id).name = up_req['name']
                storage.get(State, state_id).save()

                return jsonify(storage.get(State, state_id).to_dict()), 200
        abort(404)
