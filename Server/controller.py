import random
import string
import pyotp



# Generate login with random upper, lower and digits
def GenerateLogin(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
    


def GetUsername(conn, cursor):
    while True:
        login = GenerateLogin(12)
        cursor.execute(f'SELECT id from Users WHERE username="%s"'% (login))
        conn.commit()
        data = cursor.fetchall()
        if(len(data) == 0):
            return login



