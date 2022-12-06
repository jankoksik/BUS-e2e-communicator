import random
import string
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os
import requests
import pickle
import json

class Server:
  def __init__(self, key):
    self.username = "SERVER"
    self.key = key


#returns privatekey, publickey
def GenerateKeys(): 
    #key specs
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    #generate private key
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )
    #generate public key
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return private_key, public_key

def SavePrivateAndSendPublicKey(private_key, public_key,conn, cursor):
    path = './key/key.pickle'
#Creating directory and saving private key
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    u = None
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
        with open('key.pickle', 'wb') as handle:
            pickle.dump(u, handle, protocol=pickle.HIGHEST_PROTOCOL)
            SaveDataToDB("SERVER",public_key,conn, cursor)
            u = Server(private_key)
    else:
        with open('key.pickle', 'rb') as handle:
            u = pickle.load(handle)
    return u



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



