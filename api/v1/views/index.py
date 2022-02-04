#!usr/bin/python3
"""
indexpy
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """ Return Json Status """
    json = {"status": "OK"}
    return json
