import random
import string
import rsa
import base64
import os
import requests
import pickle
import json

class Server:
    def __init__(self, key):
        self.username = "SERVER"
        self.key = key
    
    def getKey(self):
        return self.key

SERV = None

#returns privatekey, publickey
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
        with open(path+'key.pickle', 'wb') as handle:
            SERV = Server(private_key)
            pickle.dump(SERV, handle, protocol=pickle.HIGHEST_PROTOCOL)
            publicKeyPkcs1PEM = public_key.save_pkcs1().decode('utf8') 
            SaveDataToDB("SERVER",publicKeyPkcs1PEM,conn, cursor)
    else:
        with open(path+'key.pickle', 'rb') as handle:
            SERV = pickle.load(handle)
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


# returns unencrypted and encrypted secret
def AuthTaskGeneration(user, conn, cursor):
    pk = None
    characters = string.digits + string.ascii_letters + string.punctuation
    SEC = ''.join(random.choice(characters) for i in range(128))
    cursor.execute("SELECT * from Users WHERE username= %(login)s", {'login': user})
    conn.commit()
    data = cursor.fetchall()
    if(len(data) == 1):
        pk = data[0][2]
        pubkey = rsa.PublicKey.load_pkcs1(pk)
        SECMSG = SEC.encode('utf-8')
        encrypt =  rsa.encrypt(SECMSG, pubkey)
        return encrypt, SEC
    else:
        return False, False

def LoadPrivateKey():    
    with open('./key/key.pickle', 'rb') as handle:
        u:Server = pickle.load(handle)
        return u
    return False

#save private key as pem text and try to read it that way
def Decrypt(text):
    msg = rsa.decrypt(bytes(text, encoding='utf-8'), LoadPrivateKey().getKey())
    return msg.decode('utf-8')
    

def SaveMsgToDB(senderid, receiver, part, msg, conn, cursor):
        cursor.execute("INSERT INTO MSG (sender, to, participants, msg) VALUES ( %(sid)s,%(r)s,%(p)s,%(m)s)", {'sid': senderid, 't':receiver, 'p':part, 'm':msg})
        conn.commit()

def SendUserKey(req_user, conn, cursor):
    cursor.execute("SELECT PublicKey from Users WHERE username= %(r_user)s", {'r_user': req_user})
    conn.commit()
    key=cursor.fetchall()
    if(len(key)==0):
        return False
    else:
        return key


