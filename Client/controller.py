import rsa
import os
import requests
import pickle
import json
from time import gmtime, strftime

#1. sprawdź czy masz konto
#jeśli nie to wygeneruj konto: losowanie nazwy usera, wpisywanie hasła, OTP, generacja kluczy, wysłanie do serwera
#jeśli tak to wczytaj login, podaj hasło i otp, sprawdź wiadomości

#2. poproś o klucze publiczne odbiorców, wyślij wiadomość (zakodowaną kluczem(kluczami) odbiorcy(ów) i swoim)/odczytaj wiadomość


class user:
    def __init__(self, username, key):
        self.username = username
        self.key = key

    def getKey(self):
        return self.key

    def getUsername(self):
        return self.username



#returns privatekey, publickey
def GenerateKeys(): 
    #key specs
    (pubkey, privkey) = rsa.newkeys(2048, poolsize=8)
    return privkey,pubkey

def SavePrivateAndSendPublicKey(username, private_key, public_key):
    path = './key/'
    url = 'http://bus-e2e-communicator-server-1:6060/register'
    #Creating directory and saving private key
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
    
    #Sending public key and username
    publicKeyPkcs1PEM = public_key.save_pkcs1('PEM')#.decode('utf8') 
    pack = {'username': str(username), 'PubKey': str(publicKeyPkcs1PEM)}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    x = requests.post(url, data=json.dumps(pack), headers=headers)
    print(x.text)
    u = user(x.text, private_key)
    with open(path+'key.pickle', 'wb') as handle:
        pickle.dump(u, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return x.text

# Returns false if key doesn't exist and ture if everything seems ok
def LoadPrivateKey():    
    path = './key/'
    with open(path+'key.pickle', 'rb') as handle:
        u:user = pickle.load(handle)
        return u
    return False

def RequestUserKey(req_user):
    url = 'http://bus-e2e-communicator-server-1:6060/usrpubkey'
    msg = {'req_user': str(req_user)}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    x = requests.post(url, data=json.dumps(msg), headers=headers)
    print(x.text)
    return x.text

def SendMsg(sender, receiver, encoded_to, msg):
    url = 'http://bus-e2e-communicator-server-1:6060/send'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    send_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    key = RequestUserKey(receiver)
    msg = msg.encode('utf-8')
    encrypt =  rsa.encrypt(msg, key)
    data = {'sender': str(sender), 'receiver': str(receiver), 'encoded_to': str(encoded_to), 'send_time': send_time, 'msg':str(encrypt), 'Opened': 0}
    x = requests.post(url, data=json.dumps(data), headers=headers)
    print(x.text)
    return x.text

def ReceiveMsg(msg):
    key=LoadPrivateKey().getKey()
    decrypt = rsa.decrypt(msg, key)
    print(decrypt.decode('utf-8'))
    return decrypt.decode('utf-8')

def SendMsgTest(sender, receiver, encoded_to, msg):
    url = 'http://bus-e2e-communicator-server-1:6060/send'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    send_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    data = {'sender': str(sender), 'receiver': str(receiver), 'encoded_to': str(encoded_to), 'send_time': send_time, 'msg':str(msg), 'Opened': 0}
    x = requests.post(url, data=json.dumps(data), headers=headers)
    print(x.text)
    return x.text
