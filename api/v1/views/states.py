#!/usr/bin/python3
"""
create flask app blueprint
"""
from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """
    retreieves the list of all state objects
    """
    sates = storage.all(State).values()
    state_list = [state.to_dict() for state in state_list]
    return jsonify(state_list)


@app_views.route('/states/<state.id>', strict_slashes=False)
def get_state(state_id):
    """
    """
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state.id>', method=['DELETE'], strict_slashes=False)
def get_state(state_id):
    """
    """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state.id>', methods=['POST'], strict_slashes=False)
def get_state(state_id):
    """
    """
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(400, 'Missing name')
        state = State(**kwargs)
        state.save()
        return jsonify(state.to_dict()), 200


@app_views.route('/states/<state.id>', methods=['PUT'], strict_slashes=False)
def get_state(state_id):
    """
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'create_at', 'update_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
                state.save()
                return jsonify(state.to_dict()), 200
            else:
                return abort(404)
