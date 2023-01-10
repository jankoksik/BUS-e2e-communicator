from datetime import datetime
import json
from flask import Blueprint, render_template, request
import requests
from chat import chat
import controller
import rsa
import base64

views = Blueprint(__name__, "views")

@views.route("/")
def MainPage():
    return render_template("index.html")

@views.route("/chatTest")
def chatTest():
    chats = []

    chat1 = chat("user1")
    chat1.setActive(True)
    chat1.setLastMsg("test msg 1")
    chat1.setNewMsgCount(1)
    chats.append(chat1)
    chat2 = chat("user2")
    chat2.setLastMsg("test msg 2")
    chats.append(chat2)
    chat3 = chat("user3")
    chat3.setLastMsg("test msg 3")
    chat3.setNewMsgCount(5)
    chats.append(chat3)
    return render_template("chat.html", chats = chats)

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
        x = requests.post("http://bus-e2e-communicator-server-1:6060/pubkey")
        ServerPublicKey = x.text
        pubkey = rsa.PrivateKey.load_pkcs1(ServerPublicKey)
        SECMSG = msg.encode('utf-8')
        encrypt =  rsa.encrypt(SECMSG, pubkey)
        return encrypt
    except:
        return str(False)

@views.route("/DownloadLastMsgs")
def LastMsg():
    user = controller.LoadPrivateKey()
    pack = {'username': str(user.getUsername())}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    x = requests.post("http://bus-e2e-communicator-server-1:6060/authRequest", data=json.dumps(pack), headers=headers)
    secret = x.text
    msg = rsa.decrypt(base64.b64decode(secret),user.getKey())
    p = requests.post("http://bus-e2e-communicator-server-1:6060/pubkey")
    ServerPublicKey = bytes(p.text, encoding='utf-8')
    pubkey = rsa.PublicKey.load_pkcs1(ServerPublicKey,'PEM')
    encrypt =  rsa.encrypt(msg, pubkey)
    encrypt = base64.b64encode(encrypt).decode('ascii')
    pack = {'ENC': str(secret), 'SEC' : str(encrypt), 'username' : str(user.getUsername())}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://bus-e2e-communicator-server-1:6060/DownloadLastMsgs", data=json.dumps(pack), headers=headers)
    print(r.text)
    return r.text

@views.route("/chat")
def chatz():
    chats = []
    jlm = json.loads(LastMsg())
    username = testUsername()
    ChoosedChat = request.args.get('chch')
    if not ChoosedChat is None:
        x = ChoosedChat.split("-")
        ChoosedChat = x[0] + "#" + x[1]
        print("trying to read chat with " , ChoosedChat)
    for c in jlm :
        chati = None
        if not c["reciver"] == username:
            chati = chat(c["reciver"])
        elif not c["sender"] == username:
             chati = chat(c["sender"])
        if not ChoosedChat is None and  chati.getName() == ChoosedChat:
            chati.setActive(True)
        if len(c["msg"]) > 12:
             chati.setLastMsg(c["msg"][:12]+"...")
        else : 
            chati.setLastMsg(c["msg"])
        chati.setLastMsgDate(datetime.strptime(c["send_time"], '%Y-%m-%d %H:%M:%S'))
        if not c["Opened"] :
            chati.setNewMsg(True)
        chats.append(chati)
    if len(chats)>0 and ChoosedChat is None:
        chats[0].setActive(True)
        
    return render_template("chat.html", chats = chats)

@views.route("/getUsername")
def testUsername():
    user = controller.LoadPrivateKey()
    return str(user.getUsername())

#All the time "rsa.pkcs1.DecryptionError: Decryption failed" error....
@views.route("/testMSG")
def testMSG():
    p = requests.post("http://bus-e2e-communicator-server-1:6060/pubkey")
    ServerPublicKey = bytes(p.text, encoding='utf-8')
    pubkey = rsa.PublicKey.load_pkcs1(ServerPublicKey,'PEM')
    msg = "TEST_12345"
    SECMSG = msg.encode('utf-8')
    encrypt =  rsa.encrypt(SECMSG, pubkey)
    encrypt = base64.b64encode(encrypt).decode('ascii')
    pack = {'msg':encrypt}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://bus-e2e-communicator-server-1:6060/testMSG", data=json.dumps(pack), headers=headers)
    return r.text

@views.route("/sendMsgTest")
def sendmsgtest():
    #send_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    sender='user#5452'
    receiver='user#5452'
    encoded_to='user#5452'
    msg='TEEEEEEEEST'
    x=controller.SendMsgTest(sender,receiver,encoded_to,msg)
    return x

