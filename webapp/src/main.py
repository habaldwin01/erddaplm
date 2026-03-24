from flask import Flask, render_template, Response
from flasgger import Swagger
from werkzeug.middleware.proxy_fix import ProxyFix
import os
import json

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

from basic_api import basic_api
app.register_blueprint(basic_api)

@app.errorhandler(404)
def not_found_error_handler(e):
    return Response(json.dumps({
            "error": "notFound",
            "msg": "URI not found"
            }), status=404, mimetype='application/json')

@app.route("/")
def home_screen():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
