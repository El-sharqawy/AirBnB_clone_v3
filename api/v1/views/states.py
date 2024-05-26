#!/usr/bin/python3
"""handle all the API actions for states"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves a list of all States"""
    list_states = []

    for state in storage.all(State).values():
        list_states.append(state.to_dict())

    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State By ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state using it's ID"""

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new State and save it"""
    data = request.get_json()

    if not data:
        abort(400, description="Not a JSON")

    if 'name' not in data:
        abort(400, description="Missing name")

    newState = State(**data)
    newState.save()
    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update State Method"""
    state = storage.get(State, state_id)
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()

    if not state:
        abort(404)

    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
