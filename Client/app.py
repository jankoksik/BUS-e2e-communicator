from flask import Flask, render_template, Blueprint,  flash, g, redirect, render_template, request, session, url_for
from views import views
import requests
import os

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/" )


#logowanie
#pobranie wiadomosci
#wyslanie wiadomosci



if __name__ == '__main__':
    app.run(debug=True)
