from flask import Blueprint, render_template, request
import requests
import controller

views = Blueprint(__name__, "views")

@views.route("/")
def MainPage():
    return render_template("index.html")

