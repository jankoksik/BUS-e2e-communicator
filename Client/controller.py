from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend
import os
import requests
import pickle
import json

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

def SavePrivateAndSendPublicKey(username, private_key, public_key):
    path = './key/'
    url = 'http://bus-e2e-communicator_server_1:6060/register'
#Creating directory and saving private key
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
    
#Sending public key and username
    pack = {'username': str(username), 'PubKey': str(public_key)}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    x = requests.post(url, data=json.dumps(pack), headers=headers)
    print(x.text)
    u = user(x.text, private_key)
    with open('key.pickle', 'wb') as handle:
        pickle.dump(u, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return x.text

# Returns false if key doesn't exist and ture if everything seems ok
def LoadPrivateKey():    
    with open('key.pickle', 'rb') as handle:
        u = pickle.laods(handle, protocol=pickle.HIGHEST_PROTOCOL)
        return True
    return False




