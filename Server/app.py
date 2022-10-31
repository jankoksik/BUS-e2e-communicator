from flask import Flask
from views import views
from time import sleep
from flaskext.mysql import MySQL
from datetime import datetime
import os


app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Kaczka'
app.config['MYSQL_DATABASE_DB'] = 'DB'
app.config['MYSQL_DATABASE_HOST'] = 'DB'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.register_blueprint(views, url_prefix="/" )
sleep(8)
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

if __name__ == '__main__':
    app.run(debug=True, port = 8080)


        #szukaj = request.form['kaczkoSzukator']
        #print(f'SELECT id, Imie_kaczki from KaczkoLista WHERE Imie_kaczki LIKE \'%%%s%%\' '% (szukaj))
        #cursor.execute(f'SELECT id, Imie_kaczki from KaczkoLista WHERE Imie_kaczki LIKE \'%%%s%%\' '% (szukaj))
        #conn.commit()
        #data = cursor.fetchall()
        #SearchTime =  round((datetime.now()-start).total_seconds(),2)