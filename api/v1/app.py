#!/usr/bin/python3
"""app API entry point"""

from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def not_found_404(error):
    """handle pages that doesn't exist (404)"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """setup host and port"""
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)

    app.run(host=host, port=port, threaded=True)
