#!/usr/bin/python3
"""
indexpy
"""
from api.v1.views import app_views
from models.amenity import Amenity
#from models.city import City
#from models.place import Place
#from models.review import Review
#from models.user import User
#from models.state import State
from models import storage


@app_views.route('/status')
def status():
    """ Return Json Status """
    return {"status": "OK"}

@app_views.route('/stats')
def stats():
    """ Stats """
    json = {"amenities": "storage.count(Amenity)"}
    return json