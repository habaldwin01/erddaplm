import os
import json
import requests
import urllib
from datetime import datetime
from flask import Blueprint, request, render_template, Response, make_response, redirect

basic_api = Blueprint("basic_api", __name__)

@basic_api.route("/status")
def account_screen():
    return({"status": "ok"})
