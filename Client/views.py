from flask import Blueprint, render_template, request
import requests
import controller
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

views = Blueprint(__name__, "views")

@views.route("/")
def MainPage():
    return render_template("index.html")

@views.route("/register")
def RegisterPage():
    privKey, pubKey = controller.GenerateKeys()
    return controller.SavePrivateAndSendPublicKey("user", privKey, pubKey)

@views.route("/auth", methods=["POST"])
def authorize():
    try:
        content = request.get_json()
        secret = content['secret']
        msg = rsa.decrypt(secret,controller.user.getKey()).decode('ascii')
        x = requests.post("http://bus-e2e-communicator_server_1:6060/pubkey")
        ServerPublicKey = x.text
        encrypt =  rsa.encrypt(msg.encode(),ServerPublicKey)
        return encrypt
    except:
        return False 



