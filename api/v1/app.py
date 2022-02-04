#!/usr/bin/python3
"""
Python flask
"""


from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def downtear(self):
    """ Cierra storage"""
    storage.close()


if __name__ == '__main__':
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'

    if getenv('HBNB_API_PORT'):
        puerto = getenv('HBNB_API_PORT')
    else:
        puerto = '5000'
    app.run(host=host, port=puerto, threaded=True)
