import collections
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
    c = tokenz.token(encrypt, sec, username)
    ENC_.append(c)
    return str(encrypt) #encrypt


@app.route("/verify", methods=["POST"])
def verify():
    content = request.get_json()
    username = content['username']
    enc = content['ENC']
    dec = controller.Decrypt(content['SEC'], server.getPrvKey())

    for token in ENC_:
        if not token.isExpired():
            if token.getEnc() == enc and token.getUsername() == username :
                if token.getSec() == dec:
                    ENC_.remove(token)
                    return str(True)
        else:
            ENC_.remove(token)
    return str(False)


#test function not completed yet
@app.route("/DownloadLastMsgs", methods=["POST"])
def Download():
    content = request.get_json()
    username = content['username']
    enc = content['ENC']
    dec = controller.Decrypt(content['SEC'], server.getPrvKey())

    for token in ENC_:
        if not token.isExpired() :
            if token.getEnc() == enc and token.getUsername() == username :
                if token.getSec() == dec:
                    ENC_.remove(token)
                    #download msg's
                    lastMsgs = controller.DownloadLastMsgs(username , conn, cursor)
                    objects_list = []
                    for c in lastMsgs:
                        d = collections.OrderedDict()
                        #to, sender, encoded_to, msg, time, Opened
                        d["reciver"] = c[0]
                        d["sender"] = c[1]
                        d["encoded_to"] = c[2]
                        d["msg"] = c[3]
                        d["send_time"] = c[4]
                        d["Opened"] = c[5]
                        objects_list.append(d)
                    print("AUTH OK ")
                    return json.dumps(objects_list,  default=str)
        else:
            ENC_.remove(token)
    print("AUTH FAILED")
    return str(False)
    


@app.route("/send", methods=["POST"])
def SenderPage():
    content = request.get_json()
    sender = content['sender']
    receiver = content['receiver']
    encoded_to = content['encoded_to']
    send_time = content['send_time']
    msg = content['msg']
    controller.SaveMsgToDB(sender, receiver, encoded_to,send_time, msg, conn, cursor)
    return str(sender)

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
    
