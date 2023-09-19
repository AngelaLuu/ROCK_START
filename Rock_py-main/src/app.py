from flask import Flask, render_template, request, redirect, url_for, session, Response
import os 
import database as db
from notifypy import Notify

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
#static_dir = os.path.join(template_dir, 'src', 'static')



app = Flask(__name__, template_folder= template_dir)
#app = Flask(__name__, template_folder='../templates', static_folder='../static')

#LOGIN Y REGISTER
@app.route('/')
def home():
    return render_template('layout.html')    

@app.route('/form')
def form():
    return render_template('asd.html')

@app.route('/crudd')
def crudd():
    return render_template('index.html')


@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        correo = request.form['correo']
        admin_password = request.form['admin_password']

        cursor = db.database.cursor()
        #cursor.execute("SELECT * FROM Administrador WHERE correo=%s and admin_password=%s",(correo, admin_password))
        cursor.execute("SELECT * FROM Administrador WHERE correo=%s ",(correo,))

        admins = cursor.fetchone()
        nombres_columnas = [columna[0] for columna in cursor.description]
        admin_dict = dict(zip(nombres_columnas, admins))
        cursor.close()

        if len(admins)>0:
            if admin_password == admin_dict['admin_password']:
                print(session)
                session['nombre'] = admin_dict['nombre']
                session['correo'] = admin_dict['correo']

                return render_template('index.html')


            else:
                notificacion.title = "Error de Acceso"
                notificacion.message="Correo o contraseña no valida"
                notificacion.send()
                return render_template('login.html')
        else:
            notificacion.title = "Error de Acceso"
            notificacion.message="No existe el usuario"
            notificacion.send()
            return render_template('login.html')
        
    else:
        
        return render_template('login.html')


@app.route('/registro', methods =['GET','POST'])
def registro():
     """cursor = db.database.cursor()
     cursor.execute("SELECT * FROM Administrador")
     myresult = cursor.fetchall()
     cursor.close()"""  

     if request.method == 'GET':
        return render_template('registerUser.html' )
    
     else:
        nombre = request.form['nombre']
        correo = request.form['correo']
        admin_password = request.form['admin_password']
        documento = request.form['documento']

        cursor = db.database.cursor()
        cursor.execute("INSERT INTO Administrador (nombre, correo, admin_password, documento) VALUES (%s,%s,%s,%s)", (nombre, correo, admin_password,documento))
        db.database.commit()
        return redirect(url_for('login'))




@app.route('/crud')
def crud():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM Productos")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario para obtener las keys de ellos
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return render_template('index.html', data=insertObject)

#Ruta pa guardar productos
@app.route('/products', methods=['POST'])
def addProduct():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.form['imagen']

    if nombre and descripcion and precio and cantidad and imagen:
        cursor = db.database.cursor()
        sql = "insert into Productos (nombre, descripcion, precio, cantidad, imagen) values (%s, %s, %s, %s, %s)"
        data = (nombre, descripcion, precio, cantidad, imagen)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('crud'))

@app.route('/delete/<string:id>' )
def deleteProduct(id):
        cursor = db.database.cursor()
        sql = "delete from Productos where id=%s "
        data = (id,)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('crud'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    imagen = request.form['imagen']


    if nombre and descripcion and precio and cantidad and imagen:
        cursor = db.database.cursor()
        sql = "update Productos set nombre= %s, descripcion= %s, precio= %s, cantidad= %s, imagen= %s where id= %s "
        data = (nombre, descripcion, precio, cantidad, imagen, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('crud'))



if __name__ == '__main__':
    app.secret_key = "LuLu"
    app.run(debug=True, port=4000)


    
