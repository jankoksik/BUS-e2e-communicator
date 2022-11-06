from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


#1. sprawdź czy masz konto
#jeśli nie to wygeneruj konto: losowanie nazwy usera, wpisywanie hasła, OTP, generacja kluczy, wysłanie do serwera
#jeśli tak to wczytaj login, podaj hasło i otp, sprawdź wiadomości

#2. poproś o klucze publiczne odbiorców, wyślij wiadomość (zakodowaną kluczem(kluczami) odbiorcy(ów) i swoim)/odczytaj wiadomość


#returns privatekey, publickey
def GenerateKeys(): 
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    return private_key, public_key
