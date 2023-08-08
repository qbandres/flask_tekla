from flask import Flask, render_template, request, url_for,redirect,flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '20011074'
app.config['MYSQL_DB'] = 'qbandres'

mysql = MySQL(app)

#iniciar sesion
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tekladata WHERE RATIO > 230')
    data = cur.fetchall()
    return render_template('index.html',contacts =data)


@app.route('/add_items',methods=['POST'])
def add():
    if request.method == 'POST':
        id = request.form['id']
        barcode = request.form['barcode']
        esp = request.form['esp']
        quantity = request.form['quantity']
        weight = request.form['weight']
        ratio = request.form['ratio']
        traslado = request.form['traslado']
        pre_ensamble = request.form['pre_ensamble']
        montaje = request.form['montaje']
        torque = request.form['torque']
        punch = request.form['punch']

        # Vamos a ejecutar Mysql con una funcion
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tekladata (ID, BARCODE, ESP, QUANTITY, WEIGHT, RATIO, TRASLADO, PRE_ENSAMBLE, MONTAJE, TORQUE, PUNCH) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(id, barcode, esp, quantity, weight, ratio, traslado, pre_ensamble, montaje, torque, punch)) # dentro del execute se puede hacer las conusltas mysql
        mysql.connection.commit()
        flash('items Added Successfully')

        return redirect(url_for('index'))


@app.route('/edit/<string:id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tekladata WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit_contact.html',contact = data[0])

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tekladata WHERE id ={0}'.format(id))
    mysql.connection.commit()
    flash('Items removed Successfully')
    return redirect(url_for('index'))

@app.route('/update/<id>',methods = ['POST'])
def update(id):
        if request.method == 'POST':
            barcode = request.form['barcode']
            esp = request.form['esp']
            quantity = request.form['quantity']
            weight = request.form['weight']
            ratio = request.form['ratio']
            traslado = request.form['traslado']
            pre_ensamble = request.form['pre_ensamble']
            montaje = request.form['montaje']
            torque = request.form['torque']
            punch = request.form['punch']
            cur = mysql.connection.cursor()
            cur.execute("""
                        UPDATE tekladata
                        SET BARCODE = %s,
                            ESP = %s,
                            QUANTITY = %s,  
                            WEIGHT =  %s,
                            RATIO = %s,
                            TRASLADO = %s,
                            PRE_ENSAMBLE = %s, 
                            MONTAJE = %s,
                            TORQUE = %s,
                            PUNCH = %s
                        WHERE ID = %s
                        """,(barcode,esp,quantity,weight,ratio,traslado,pre_ensamble,montaje,torque,punch,id))
            mysql.connection.commit()
            flash('Contacts Upsate Successfully')
            return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port = 3000,debug = True)