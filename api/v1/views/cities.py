#!/usr/bin/python3
"""handle all the API actions for Cities"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves a list of all States"""
    list_cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a specific City By ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City using it's ID"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a new State and save it"""
    state = storage.get(State, state_id)
    data = request.get_json()

    if not state:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    newCity = City(**data)
    newCity.state_id = state.id
    newCity.save()
    return make_response(jsonify(newCity.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update City Method"""
    city = storage.get(City, city_id)
    ignored = ['id', 'state_id', 'created_at', 'updated_at']
    data = request.get_json()

    if not city:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    for k, v in data.items():
        if k not in ignored:
            setattr(city, k, v)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
