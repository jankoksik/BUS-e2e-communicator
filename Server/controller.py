from datetime import datetime, timedelta
import random
import string
import rsa
import base64
import os
import requests
import secrets
import json

class Server:
    def __init__(self, pubkey, prvkey):
        self.username = "SERVER"
        self.pubkey = pubkey
        self.prvkey=prvkey

    def getPubKey(self):
        return self.pubkey
    def getPrvKey(self):
        return self.prvkey
    def setPubKey(self, pubkey):
        self._pubkey = pubkey
    def setPrvKey(self, prvkey):
        self._prvkey = prvkey


#returns new privatekey, publickey
def GenerateKeys(): 
    #key specs
    (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)
    return privkey,pubkey

def SavePrivateAndSendPublicKey(private_key, public_key,conn, cursor):
    path = './key/privatekey.pem'
    path2 = './key/publickey.pem'
    #Creating directory and saving private key
    # Check whether the specified path exists or not
    SERV = Server(public_key,private_key)
    if not os.path.exists('./key/'):
        os.makedirs('./key/')

    if not os.path.exists(path) or not os.path.exists(path2):
        # Create a new directory because it does not exist 
        with open(path+'privatekey.pem', 'wb') as file:
            file.write(private_key.save_pkcs1('PEM'))
        with open(path+'publickey.pem', 'wb') as file:
            file.write(public_key.save_pkcs1('PEM'))
        #SaveUserToDB("SERVER",public_key,conn, cursor)
    else:
        with open(path+'privatekey.pem', 'rb') as file:
            SERV.setPrvKey(rsa.PrivateKey.load_pkcs1(file.read()))
        with open(path+'publickey.pem', 'rb') as file:
            SERV.setPubKey(rsa.PublicKey.load_pkcs1(file.read()))
    return SERV



# Generate login with random upper, lower and digits
def GenerateLogin(username,length):
    characters = string.digits
    hash = ''.join(random.choice(characters) for i in range(length))
    return username + "#" + hash
    


def GetUsername(username,conn, cursor):
    if len(username) > 27:
        username = username[:27]
    username = username.replace("#", "_")
    while True:
        login = GenerateLogin(username,4)
        cursor.execute("SELECT id from Users WHERE username= %(login)s", {'login': login})
        conn.commit()
        data = cursor.fetchall()
        if(len(data) == 0):
            return login

def SaveUserToDB(username,key,conn, cursor):
        cursor.execute("INSERT INTO Users (username, PublicKey) VALUES ( %(u)s,%(p)s)", {'u': username, 'p':key})
        conn.commit()

def DownloadLastMsgs(username,conn, cursor):
    cursor.execute("""SELECT * FROM MSG 
WHERE id IN (
    SELECT MAX(id) AS last_msg_id 
    FROM MSG WHERE (reciver= %(u)s OR sender =%(u)s) AND encoded_to = %(u)s 
    GROUP BY IF(sender = %(u)s, reciver, sender)
)""", {'u': username}) 
    data = cursor.fetchall()
    print(data)
    return data

#sender means 2nd participant here
def DownloadMsgs(owner:str, sender:str, page:int ,conn, cursor):
    p = page*5
    cursor.execute("""SELECT * 
    FROM MSG 
    WHERE ((reciver=%(o)s AND sender=%(s)s) OR (reciver=%(s)s AND sender=%(o)s)) AND encoded_to = %(o)s 
    ORDER BY send_time DESC 
    LIMIT 5 OFFSET %(p)s""", {'o': owner, 's':sender, 'p':page}) 
    data = cursor.fetchall()
    print("sql ok")
    print("PAAAAGEEEEE")
    print(type(page))
    print(page)
    for c in data:
        cursor.execute("""UPDATE MSG
        SET Opened = 1
        WHERE id = %(id)s""", {'id': c[0]})
    print(data)
    return data

# returns unencrypted and encrypted secret
def AuthTaskGeneration(user, conn, cursor):
    pk = None
    characters = string.digits + string.ascii_letters + string.punctuation
    SEC = ''.join(secrets.choice(characters) for i in range(128))
    pk = SendUserKey(user, conn, cursor)
    #pk = pk.replace(b'\\n', b'\n').decode('ascii')
    print(type(pk), pk)
    #key = b'-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAwC9NK0yGvK4Y3CazjBaXysRMNxd6oD0RJQfCrAODFF2+yS6Fn5Xb\nrhL+ZB7bUwFh/3gX0EBmRf+Sq96JWd1WPvRcU5N6Qg6TntKKgdtcTDL+l083oSi4\nziyQMXEkJE9/G/63V4l7hj5Vm2I9hZRoRSCP/yQbTmlOwxAWeH9aqnhk0a/C82Y0\nWa5av019NC9cWCu0uEwx5QfMivqrQGU4w9XZwtNlxJsl6o3f5ZyVewKTAR7s8m8e\nK3kep5Tv7lGsUWGXNOpPAreEuPKqKPH0VSzYVKF7l9iv9viZalyZRgf8z3odhrOl\n3JYkT44i1G3jyohC/f+ea8zYILpRzG1kIQIDAQAB\n-----END RSA PUBLIC KEY-----\n'
    pubkey = rsa.PublicKey.load_pkcs1(pk)
    SECMSG = SEC.encode('utf-8')
    encrypt =  rsa.encrypt(SECMSG, pubkey)
    encrypt = base64.b64encode(encrypt).decode('ascii')
    return encrypt, SEC

#save private key as pem text and try to read it that way
def Decrypt(text, prvkey):
    msg = rsa.decrypt(base64.b64decode(text),prvkey)
    #msg = rsa.decrypt(bytes(text, encoding='utf-8'), prvkey)
    return msg.decode('utf-8')

def SaveMsgToDB(sender, receiver, encoded_to,msg, opened,conn, cursor):
    #id	sender	reciver	encoded_to	send_time	msg	Opened
        time = (datetime.utcnow()+timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO MSG (sender, reciver, encoded_to, send_time, msg, Opened) VALUES ( %(sender)s,%(reciver)s,%(encoded_to)s, %(send_time)s,%(msg)s,%(Opened)s)", {'sender':sender, 'reciver':receiver, 'encoded_to':encoded_to, 'send_time':time, 'msg':msg, 'Opened':opened})
        conn.commit() 

def SendUserKey(req_user, conn, cursor):
    cursor.execute("SELECT PublicKey FROM Users WHERE username= %(r_user)s", {'r_user': req_user})
    key=cursor.fetchone() #fetchall returns a list of results
    print("=== KEY ===")
    print(key)
    if key is None or (len(key)==0):
        return False
    else:
        return (key[0][2:-1].encode("ASCII")).replace(b'\\n', b'\n').decode('ascii')


