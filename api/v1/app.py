#!/usr/bin/python3
""" app entry point"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from flask_cors import CORS


app = Flask(__name__)

app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found_404(error):
    """Error 404 Handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(exception):
    """ Close Our Storage"""
    storage.close()


if __name__ == "__main__":
    """Port and Host Initialize"""
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)

    app.run(host=host, port=port, threaded=True)
