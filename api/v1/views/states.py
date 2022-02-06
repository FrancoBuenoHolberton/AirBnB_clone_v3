#!/usr/bin/python3
""" Manage STates """

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all
    state objects: GET /api/v1/states"""

    sta = storage.all(State)
    ls = []

    for sta in states.values():
        ls.append(sta.to_dict())

    return jsonify(ls)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""

    id_sta = storage.get(State, state_id)

    if id_sta is None:
        abort(404)

    return jsonify(id_sta.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_id(state_id):
    """Deletes a State object::
    DELETE /api/v1/states/<state_id>"""

    id_sta = storage.get(State, state_id)

    if id_sta is None:
        abort(404)

    id_sta.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State: POST /api/v1/states"""

    cr = request.get_json()

    if (not cr):
        abort(400, 'Not a JSON')

    if ('name' not in cr):
        abort(400, 'Missing name')

    id_sta = State(**cr)
    id_sta.save()
    return make_response(jsonify(id_sta.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update"""

    id_sta = storage.get(State, state_id)
    if id_sta is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for sta, val in request.get_json().items():
        if (sta not in ["id", "created_at", "updated_at"]):
            setattr(id_sta, sta, val)

    id_sta.save()
    return jsonify(id_sta.to_dict())
