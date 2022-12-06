from flask import Flask, render_template, flash, request, redirect
from time import sleep
from flaskext.mysql import MySQL
import secrets
from datetime import datetime
import controller
import os

#Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex()

#Database config
app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_DATABASE_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_DATABASE_PASSWORD']
app.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DATABASE_DB']
app.config['MYSQL_DATABASE_HOST'] = os.environ['MYSQL_DATABASE_HOST']
app.config['MYSQL_DATABASE_PORT'] = int(os.environ['MYSQL_DATABASE_PORT'])


sleep(1)
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
#init
privKey, pubKey = controller.GenerateKeys()
server = controller.SavePrivateAndSendPublicKey(privKey, pubKey,conn, cursor)

server = None


@app.route("/register", methods=["POST"])
def RegisterPage():
    content = request.get_json()
    username = content['username']
    publicKey = content['PubKey']
    usernameWithHash = controller.GetUsername(username, conn, cursor)
    controller.SaveDataToDB(usernameWithHash,publicKey, conn, cursor)
    return str(usernameWithHash)


if __name__ == '__main__':
    app.run(debug=True)
    
