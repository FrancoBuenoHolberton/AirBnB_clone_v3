#!/usr/bin/python3
""" view for User object that handles
all default RESTFul API actions """

from api.v1.views import app_views
from models.user import User
from models import storage
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ list all user """

    if request.method == 'GET':

        ls = []
        for user in storage.all(User).values():
            ls.append(user.to_dict():

        return jsonify(ls)

@app_views.route('/users/<string:user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """ retrieve a user """

    us = storage.get(User, user_id)

    if us is None:
        abort(404)

    return jsonify(us.to_dict())


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ delete a user object """

    us = storage.get(User, user_id)

    if us is None:
        abort(404)

    us.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ create user """

    req = request.get_json()
    if (not req):
        abort(400, 'Not a JSON')

    if ('email' not in req):
        abort(400, 'Missing email')

    if ('password' not in req):
        abort(400, 'Missing password')

    us = User(**req)
    us.save()
    return make_response(jsonify(us.to_dict()), 201)


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ update User """

    us = storage.get(User, user_id)
    if us is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for key, val in request.get_json().items():
        if (key not in ["id", "created_at", "updated_at"]):
            setattr(us, key, val)

    us.save()
    return jsonify(us.to_dict())
