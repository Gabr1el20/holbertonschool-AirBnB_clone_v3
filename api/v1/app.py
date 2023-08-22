#!/usr/bin/python
"""v1 of the API"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def app_teardown_appcontext(self):
    """Remove the SQLAlchemy session"""
    storage.close()

if __name__ == "__main__":
    app.run(port=os.getenv("HBNB_API_PORT", '5000'),
            host=(os.getenv("HBNB_API_HOST", '0.0.0.0')))