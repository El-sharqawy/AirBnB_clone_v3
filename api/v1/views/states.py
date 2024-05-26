#!/usr/bin/python3
"""handle all the API actions for states"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get():
    """get method that retrives states"""
    states = []

    for state in storage.all(State).values():
        states.append(state.to_dict())

    return make_response(jsonify(states), 200)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state_id(state_id):
    """get state by ID"""
    state = storage.get(State, state_id)

    if state:
        return make_response(jsonify(state.to_dict()), 200)

    abort(404)


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state_id(state_id):
    """Delete a state using it's ID"""
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

    newState = State(**state)
    newState.save()
    return make_response(jsonify(newState.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def put_state(state_id):
    """Update State Method"""
    state = storage.get(State, state_id)
    ignored = ['id', 'created_at', 'updated_at']
    myData = request.get_json()

    if not state:
        abort(404)

    if not myData:
        return make_response("Not a JSON", 400)

    for k, v in myData.items():
        if k not in ignored:
            setattr(state, k, v)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
