import os
import json
import requests
import urllib
from datetime import datetime
from flask import Blueprint, request, render_template, Response, make_response, redirect

basic_pages = Blueprint("basic_pages", __name__)

@project_pages.route("/result", methods=['GET'])
def result_page():
    return render_template("result.html")
