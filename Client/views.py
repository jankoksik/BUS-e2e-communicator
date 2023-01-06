import json
from flask import Blueprint, render_template, request
import requests
import controller
import rsa

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
        user = controller.LoadPrivateKey()
        msg = rsa.decrypt(secret,rsa.PrivateKey.load_pkcs1(user.getKey())).decode('utf-8')
        x = requests.post("http://bus-e2e-communicator_server_1:6060/pubkey")
        ServerPublicKey = x.text
        pubkey = rsa.PrivateKey.load_pkcs1(ServerPublicKey)
        SECMSG = msg.encode('utf-8')
        encrypt =  rsa.encrypt(SECMSG, pubkey)
        return encrypt
    except:
        return str(False)

@views.route("/authTest")
def testAuth():
    user = controller.LoadPrivateKey()
    pack = {'username': str(user.getUsername())}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    x = requests.post("http://bus-e2e-communicator_server_1:6060/authRequest", data=json.dumps(pack), headers=headers)
    secret = x.text
    msg = x.text
    #msg = rsa.decrypt(bytes(secret, encoding='utf-8'),user.getKey()).decode('utf-8')
    p = requests.post("http://bus-e2e-communicator_server_1:6060/pubkey")
    ServerPublicKey = bytes(p.text, encoding='utf-8')
    pubkey = rsa.PublicKey.load_pkcs1(ServerPublicKey)
    SECMSG = msg.encode('utf-8')
    encrypt =  rsa.encrypt(SECMSG, pubkey)

    pack = {'ENC': str(secret), 'SEC' : str(encrypt)}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://bus-e2e-communicator_server_1:6060/verify", data=json.dumps(pack), headers=headers)
    return r.text

@views.route("/getUsername")
def testUsername():
    user = controller.LoadPrivateKey()
    return str(user.getUsername())


