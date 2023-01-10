import random
import string
import rsa
import base64
import os
import requests
import pickle
import json

class Server:
    def __init__(self, pubkey, prvkey):
        self.username = "SERVER"
        self.pubkey = pubkey
        self.prvkey=prvkey
    #def __init__(self):
    #    self.username = "SERVER"

    def getPubKey(self):
        return self.pubkey
    def getPrvKey(self):
        return self.prvkey
    def setPubKey(self, pubkey):
        self._pubkey = pubkey
    def setPrvKey(self, prvkey):
        self._prvkey = prvkey

SERV = None
#returns new privatekey, publickey
def GenerateKeys(): 
    #key specs
    (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)
    return privkey,pubkey

def SavePrivateAndSendPublicKey(private_key, public_key,conn, cursor):
    path = './key/'
#Creating directory and saving private key
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
        #with open(path+'key.pickle', 'wb') as handle:
            #SERV = Server(public_key,private_key)
            #SERV.setPrvKey(private_key)
            #SERV.getPubKey(public_key)
            #pickle.dump(SERV, handle, protocol=pickle.HIGHEST_PROTOCOL)
            #publicKeyPkcs1PEM = public_key.save_pkcs1().decode('utf8') 
        SERV = Server(public_key,private_key)
        with open(path+'privatekey.pem', 'wb') as file:
            file.write(private_key.save_pkcs1('PEM'))
        with open(path+'publickey.pem', 'wb') as file:
            file.write(public_key.save_pkcs1('PEM'))
        SaveDataToDB("SERVER",public_key,conn, cursor)
    else:
        #with open(path+'key.pickle', 'rb') as handle:
            #SERV:Server = pickle.load(handle)
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
    while True:
        login = GenerateLogin(username,4)
        cursor.execute("SELECT id from Users WHERE username= %(login)s", {'login': login})
        conn.commit()
        data = cursor.fetchall()
        if(len(data) == 0):
            return login

def SaveDataToDB(username,key,conn, cursor):
        cursor.execute("INSERT INTO Users (username, PublicKey) VALUES ( %(u)s,%(p)s)", {'u': username, 'p':key})
        conn.commit()

def DownloadLastMsgs(username,conn, cursor):
    cursor.execute("SELECT reciver, sender, encoded_to, msg, send_time, Opened \
    FROM \
     (SELECT reciver, sender, encoded_to, msg, send_time, Opened,  \
                  @msg_rank := IF(@current_sender = sender, @msg_rank + 1, 1) AS msg_rank, \
                  @current_sender := sender  \
       FROM MSG \
       ORDER BY sender, send_time DESC \
     ) ranked \
    WHERE (reciver =  %(u)s OR sender= %(u)s) AND encoded_to = %(u)s  AND msg_rank <= 1;", {'u': username}) 
    conn.commit()
    data = cursor.fetchall()
    return data


def DownloadMsgs(owner, sender,key,conn, cursor):
    cursor.execute("SELECT reciver, sender, encoded_to, msg, send_time, Opened \
    FROM MSG \
    ORDER BY send_time DESC \
    WHERE ((reciver =  %(o)s AND sender= %(s)s) OR (reciver =  %(s)s AND sender= %(o)s)) AND encoded_to = %(u)s \
    LIMIT 10;", {'o': owner, 's':sender}) 
    conn.commit()
    data = cursor.fetchall()
    return data

# returns unencrypted and encrypted secret
def AuthTaskGeneration(user, conn, cursor):
    pk = None
    characters = string.digits + string.ascii_letters + string.punctuation
    SEC = ''.join(random.choice(characters) for i in range(128))
    pk = SendUserKey(user, conn, cursor)
    pk = pk.replace(b'\\n', b'\n').decode('ascii')
    print(type(pk), pk)
    #key = b'-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAwC9NK0yGvK4Y3CazjBaXysRMNxd6oD0RJQfCrAODFF2+yS6Fn5Xb\nrhL+ZB7bUwFh/3gX0EBmRf+Sq96JWd1WPvRcU5N6Qg6TntKKgdtcTDL+l083oSi4\nziyQMXEkJE9/G/63V4l7hj5Vm2I9hZRoRSCP/yQbTmlOwxAWeH9aqnhk0a/C82Y0\nWa5av019NC9cWCu0uEwx5QfMivqrQGU4w9XZwtNlxJsl6o3f5ZyVewKTAR7s8m8e\nK3kep5Tv7lGsUWGXNOpPAreEuPKqKPH0VSzYVKF7l9iv9viZalyZRgf8z3odhrOl\n3JYkT44i1G3jyohC/f+ea8zYILpRzG1kIQIDAQAB\n-----END RSA PUBLIC KEY-----\n'
    pubkey = rsa.PublicKey.load_pkcs1(pk)
    SECMSG = SEC.encode('utf-8')
    encrypt =  rsa.encrypt(SECMSG, pubkey)
    encrypt = base64.b64encode(encrypt).decode('ascii')
    return encrypt, SEC


#def GetPublickey():
#    return SERV.getPubKey()

#def LoadPrivateKey():    
    with open('./key/key.pickle', 'rb') as handle:
        u:Server = pickle.load(handle)
        #key = rsa.PrivateKey.load_pkcs1(str(u.getKey()))
        #print(u.getKey().save_pkcs1().decode('utf8') )
        return u
        
    return False

#save private key as pem text and try to read it that way
def Decrypt(text, prvkey):
    msg = rsa.decrypt(base64.b64decode(text),prvkey)
    #msg = rsa.decrypt(bytes(text, encoding='utf-8'), prvkey)
    return msg.decode('utf-8')

#for test | Delete later 
#def getPrivateKeyString():
    return LoadPrivateKey().getKey().save_pkcs1().decode('utf8') 

def SaveMsgToDB(senderid, receiver, part, msg, conn, cursor):
        cursor.execute("INSERT INTO MSG (sender, to, participants, msg) VALUES ( %(sid)s,%(r)s,%(p)s,%(m)s)", {'sid': senderid, 't':receiver, 'p':part, 'm':msg})
        conn.commit()

def SendUserKey(req_user, conn, cursor):
    cursor.execute("SELECT PublicKey from Users WHERE username= %(r_user)s", {'r_user': req_user})
    conn.commit()
    key=cursor.fetchone() #fetchall returns a list of results
    if(len(key)==0):
        return False
    else:
        return key[0][2:-1].encode("ASCII")


