import random
import string
import pyotp


# Generate login with random upper, lower and digits
def GenerateLogin(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
    




    

