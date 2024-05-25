#!/usr/bin/python3
""" Status Route"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """return OK if api is running"""
    return jsonify({"status": "OK"})
