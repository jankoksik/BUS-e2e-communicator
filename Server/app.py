from flask import Flask, render_template, flash, request, redirect
from time import sleep
from flaskext.mysql import MySQL
import secrets
from datetime import datetime
import controller
import requests
import json
import os
import tokenz
import rsa

#Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()

#Database config
app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_DATABASE_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_DATABASE_PASSWORD']
app.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DATABASE_DB']
app.config['MYSQL_DATABASE_HOST'] = os.environ['MYSQL_DATABASE_HOST']
app.config['MYSQL_DATABASE_PORT'] = int(os.environ['MYSQL_DATABASE_PORT'])


sleep(1)
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
#init
privKey, pubKey = controller.GenerateKeys()
server = controller.SavePrivateAndSendPublicKey(privKey, pubKey,conn, cursor)
ENC_ = []


#server = None


@app.route("/register", methods=["POST"])
def RegisterPage():
    content = request.get_json()
    username = content['username']
    publicKey = str(content['PubKey'])
    usernameWithHash = controller.GetUsername(username, conn, cursor)
    controller.SaveDataToDB(usernameWithHash,publicKey, conn, cursor)
    return str(usernameWithHash)

@app.route("/pubkey", methods=["POST"])
def getPublicKey():
    return str(server.getPubKey().save_pkcs1().decode('utf8'))


#Get username of user that whant to authenticate
@app.route("/authRequest", methods=["POST"])
def auth():
    content = request.get_json()
    username = content['username']
    encrypt, sec = controller.AuthTaskGeneration(username , conn, cursor)
    if sec == False: 
        return str(False) 
    c = tokenz.token(encrypt, sec)
    ENC_.append(c)
    return str(encrypt) #encrypt


@app.route("/verify", methods=["POST"])
def verify():
    content = request.get_json()
    enc = content['ENC']
    #print(type(server.getPrvKey()))
    key = server.getPrvKey()
    key = key.save_pkcs1('PEM')
    print(key)
    #print(content['SEC'])
    dec = controller.Decrypt(content['SEC'], key)

    for token in enc:
        if not token.isExpired():
            if token.getEnc() == enc:
                if token.getSec() == dec:
                    ENC_.remove(token)
                    return str(True)
        else:
            ENC_.remove(token)
    return str(False)
    


@app.route("/send", methods=["POST"])
def SenderPage():
    content = request.get_json()
    senderid = content['senderid']
    receiver = content['receiver']
    participants = content['participants']
    msg = content['msg']
    controller.SaveMsgToDB(senderid, receiver, participants, msg, conn, cursor)
    return str(senderid)

@app.route("/usrpubkey", methods=["POST"])
def getUserPublicKey():
    content = request.get_json()
    req_user = content['req_user']
    key=controller.SendUserKey(req_user, conn, cursor)
    return str(key)


@app.route("/testMSG", methods=["POST"])
def testMSG():
    content = request.get_json()
    msg = content['msg']
    #value = {
    #    "msg": str(msg.encode),
    #    "pubkey": str(server.getPubKey().save_pkcs1('PEM')),
    #    "prvkey": str(server.getPrvKey().save_pkcs1('PEM'))
    #}
    #return json.dumps(value)
    #return str(msg.encode) + " : " + str(server.getPrvKey().save_pkcs1('PEM')) + ":" + str(server.getPubKey().save_pkcs1('PEM'))
    return controller.Decrypt(msg, server.getPrvKey())

#@app.route("/testpriv", methods=["GET"])
#def getprivatekey():
    return controller.LoadPrivateKey() + ":" 
    #return str(msg) + " : " + controller.getPrivateKeyString()
    #return controller.Decrypt(msg)

if __name__ == '__main__':
    app.run(debug=True)
    
