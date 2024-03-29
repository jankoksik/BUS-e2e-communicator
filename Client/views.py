from datetime import datetime
import json
import os
from flask import Blueprint, render_template, request,redirect, redirect, url_for, flash
import requests
from msg import msg
from chat import chat
import controller
import rsa
import base64

views = Blueprint(__name__, "views")

@views.route("/")
def MainPage():
    path = './key/'
    isExist = os.path.exists(path)
    if not isExist:
        #if request.method == 'POST':
            #user=request.form['Login']
            #print(user)
            #redirect(url_for(RegisterPage))
        return redirect(request.base_url+"register", code=302)
    else:
        return redirect(request.base_url+"chat", code=302)

@views.route("/register", methods=('GET', 'POST'))
def RegisterPage():
    #user='aa'
    if request.method == 'POST':
        user=request.form.get("Login")
        privKey, pubKey = controller.GenerateKeys()
        controller.SavePrivateAndSendPublicKey(user, privKey, pubKey)
        return redirect("/chat", code=302)
    return render_template("register.html")

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

def DownMsg(participant:str, page:int):
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
    #    participant = content['participant'], page = int(content['page'])
    pack = {'ENC': str(secret), 'SEC' : str(encrypt), 'username' : str(user.getUsername()), 'participant' : str(participant), 'page':page}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post("http://bus-e2e-communicator-server-1:6060/DownloadMsgs", data=json.dumps(pack), headers=headers)
    print(r.text)
    return r.text


@views.route("/chat",methods=["POST","GET"])
def chatz():
    chats = []
    Msgs = []
    username = testUsername()
    if username == "":
        return redirect(url_for('views.RegisterPage'), code=302)
    user = controller.LoadPrivateKey()
    ChoosedChat = request.args.get('chch')
    page = request.args.get('page')
    print("start")
    print(page)
    if not ChoosedChat is None and not ChoosedChat == "" and not ChoosedChat == "None" : 
        x = ChoosedChat.split("-")
        ChoosedChat = x[0] + "#" + x[1]
        print("trying to read chat with " , ChoosedChat)
    

        if request.method == "POST" and not username==ChoosedChat :
            #send msg
            data = request.form.get('msgBox')
            pack = {'req_user': str(ChoosedChat)}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            p = requests.post("http://bus-e2e-communicator-server-1:6060/usrpubkey", data=json.dumps(pack), headers=headers)
            ReciverPublicKey = bytes(p.text, encoding='utf-8')
            pubkey = rsa.PublicKey.load_pkcs1(ReciverPublicKey,'PEM')
            SECMSG = data.encode('utf-8')
            encrypt =  rsa.encrypt(SECMSG, pubkey)
            encrypt1 = base64.b64encode(encrypt).decode('ascii')
            print("encrypt 1 : ")
            print(encrypt1)
            pack = {'req_user': str(username)}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            p = requests.post("http://bus-e2e-communicator-server-1:6060/usrpubkey", data=json.dumps(pack), headers=headers)
            ReciverPublicKey = bytes(p.text, encoding='utf-8')
            pubkey = rsa.PublicKey.load_pkcs1(ReciverPublicKey,'PEM')
            SECMSG = data.encode('utf-8')
            encrypt =  rsa.encrypt(SECMSG, pubkey)
            encrypt2 = base64.b64encode(encrypt).decode('ascii')
            print("encrypt 2 : ")
            print(encrypt2)
            user = controller.LoadPrivateKey()
            pack = {'username': str(user.getUsername())}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            x = requests.post("http://bus-e2e-communicator-server-1:6060/authRequest", data=json.dumps(pack), headers=headers)
            secret = x.text
            msgz = rsa.decrypt(base64.b64decode(secret),user.getKey())
            p = requests.post("http://bus-e2e-communicator-server-1:6060/pubkey")
            ServerPublicKey = bytes(p.text, encoding='utf-8')
            pubkey = rsa.PublicKey.load_pkcs1(ServerPublicKey,'PEM')
            encrypt =  rsa.encrypt(msgz, pubkey)
            encrypt = base64.b64encode(encrypt).decode('ascii')
            #    participant = content['participant'], page = int(content['page'])
            print("SENDING")
            pack = {'ENC': str(secret), 'SEC' : str(encrypt), 'username' : str(user.getUsername()), 'participant' : str(ChoosedChat), 'msg':encrypt1, 'msg2':encrypt2}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post("http://bus-e2e-communicator-server-1:6060/MSG", data=json.dumps(pack), headers=headers)

        

    if not ChoosedChat is None:
        if page is None:
            page=0
        elif page.isnumeric():
            page = int(page)
        else:
            page=0

        print(page)
        print(type(page))
        if not type(page) == int:
            page = 0
        if page < 0:
            page = 0
        DownMsgs = json.loads(DownMsg(ChoosedChat, page))
        print (page)
        for m in reversed(DownMsgs):
            print(m)
            Msg = msg(m["sender"])
            Msg.setDate(datetime.strptime(m["send_time"], '%Y-%m-%d %H:%M:%S'))
            decodedMsg = rsa.decrypt(base64.b64decode(m["msg"]),user.getKey()).decode('utf-8')
            Msg.setMsg(decodedMsg)
            if Msg.getName() == username:
                Msg.setMe(True)
            Msgs.append(Msg)

    #Load in last messenges
    jlm = json.loads(LastMsg())
    for c in reversed(jlm) :
        chati = None
        if not c["reciver"] == username:
            chati = chat(c["reciver"])
        elif not c["sender"] == username:
             chati = chat(c["sender"])
        if not ChoosedChat is None and  chati.getName() == ChoosedChat:
            chati.setActive(True)
        decodedMsg = rsa.decrypt(base64.b64decode(c["msg"]),user.getKey()).decode('utf-8')
        if len(decodedMsg) > 12:
             chati.setLastMsg(decodedMsg[:12]+"...")
        else : 
            chati.setLastMsg(decodedMsg)
        chati.setLastMsgDate(datetime.strptime(c["send_time"], '%Y-%m-%d %H:%M:%S'))
        if not c["Opened"] :
            chati.setNewMsg(True)
        chats.append(chati)

    if len(chats)>0 and ChoosedChat is None : 
        return redirect(request.base_url+"?chch="+chats[0].getNameHTML(), code=302)
    # Load msgs
    if len(chats)>0 and ChoosedChat is None:
        ChoosedChat = chats[0].getName()
        chats[0].setActive(True)
        print("trying to read chat with " , ChoosedChat)
        DownMsgs = json.loads(DownMsg(ChoosedChat, page))
        print(page)
        for m in reversed(DownMsgs):
            Msg = msg(m["sender"])
            Msg.setDate(datetime.strptime(m["send_time"], '%Y-%m-%d %H:%M:%S'))
            decodedMsg = rsa.decrypt(base64.b64decode(m["msg"]),user.getKey()).decode('utf-8')
            Msg.setMsg(decodedMsg)
            if Msg.getName() == username:
                Msg.setMe(True)
            Msgs.append(Msg)
    return render_template("chat.html", chats = chats, Msgs= Msgs, username=username)

@views.route("/getUsername")
def testUsername():
    user = controller.LoadPrivateKey()
    if user == "":
        return ""
    return str(user.getUsername())

#All the time "rsa.pkcs1.DecryptionError: Decryption failed" error....
#@views.route("/testMSG")
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


#@views.route("/sendMsgTest")
def sendmsgtest():
    #send_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    sender='user#5452'
    receiver='user#5452'
    encoded_to='user#5452'
    msg='TEEEEEEEEST'
    x=controller.SendMsgTest(sender,receiver,encoded_to,msg)
    return x

