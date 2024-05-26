#!/usr/bin/python3
""" handle all the API actions for states"""

from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get():
    """get method that retrives states"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return make_response(jsonify(state), 200)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state_id(state_id):
    """get state by ID"""
    state = storage.get(State, state_id)
    if state:
        return make_response(jsonify(state.to_dict()), 200)
    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state_id(state_id):
    """delete a state using it's ID"""
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states', methods=['POST'])
def post_state():
    """Creates a new State and save it"""
    state = request.get_json()

    if not state:
        return make_response("Not a JSON", 400)

    if 'name' not in state:
        return make_response("Missing name", 400)

    new_state = State(**state)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def put_state(state_id):
    """Update Method to Update states"""
    state = storage.get(State, state_id)
    ignored_keys = ['id', 'updated_at', 'created_at']
    data = request.get_json()

    if not state:
        abort(404)

    if not data:
        return make_response("Not a JSON", 400)

    for k, v in data.items():
        if k not in ignored_keys:
            setattr(state, k, v)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
