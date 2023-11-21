from flask import Flask, render_template, request, redirect, url_for, session, Response, flash
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

@app.route('/catalogo')
def form():
    return render_template('catalogo.html')

@app.route('/carrito')
def crudd():
    return render_template('carrito.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')



@app.route('/login', methods= ["GET", "POST"])
def login():

    notificacion = Notify()

    if request.method == 'POST':
        correo = request.form['correo']
        admin_password = request.form['admin_password']

        cursor = db.database.cursor()
        #cursor.execute("SELECT * FROM Administrador WHERE correo=%s and admin_password=%s",(correo, admin_password))
        cursor.execute("SELECT * FROM Administrador WHERE correo=%s ",(correo, ))

        admins = cursor.fetchone()
        nombres_columnas = [columna[0] for columna in cursor.description]   
        admin_dict = dict(zip(nombres_columnas, admins))
        cursor.close()

        if len(admins)>0:
            if admin_password == admin_dict['admin_password']:
                print(session)
                session['nombre'] = admin_dict['nombre']
                session['correo'] = admin_dict['correo']

                return render_template('admin.html')


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
        cursor.execute("INSERT INTO Administrador (nombre, correo, admin_password, documento) VALUES (%s,%s,%s,%s)", (nombre, correo, admin_password, documento,))
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
    stock = request.form['stock']
    imagen = request.form['imagen']

    if nombre and descripcion and precio and cantidad and imagen and stock:
        cursor = db.database.cursor()
        sql = "insert into Productos (nombre, descripcion, precio, cantidad, imagen) values (%s, %s, %s, %s, %s, %s)"
        data = (nombre, descripcion, precio, cantidad, imagen, stock)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('crud'))

#ELIMINAR PRODUCTOS
@app.route('/delete/<string:id>' )
def deleteProduct(id):
        cursor = db.database.cursor()
        sql = "delete from Productos where id=%s "
        data = (id,)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('crud'))

#EDITAR PRODUCTOS
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    stock = request.form['stock']
    imagen = request.form['imagen']


    if nombre and descripcion and precio and cantidad and imagen and stock:
        cursor = db.database.cursor()
        sql = "update Productos set nombre= %s, descripcion= %s, precio= %s, cantidad= %s, imagen= %s, stock= %s where id= %s "
        data = (nombre, descripcion, precio, cantidad, imagen, stock, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('crud'))


@app.route('/getProducts')
def getProducts():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM Productos")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario para obtener las keys de ellos
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    return insertObject


#PEDIDOS
@app.route('/pedidos')
def pedidos():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM Pedidos")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario para obtener las keys de ellos
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()

    #return insertObject
    return render_template('pedido.html', data=insertObject)


#AGREGAR PEDIDOS CON EL FORMULARIO DE COMPRA
@app.route('/addpedido', methods=['POST', 'GET'])
def addPedido():

    if request.method == 'GET':
        return render_template('carrito.html' )

    else:
        nombre_cliente = request.form['nombre_cliente']
        direccion_cliente = request.form['direccion_cliente']
        numero_cliente = request.form['numero_cliente']
        #talla = request.form['talla']
        metodo_pago = request.form['metodo_pago']

        cursor = db.database.cursor()
        sql = "insert into Pedidos (nombre_cliente, direccion_envio, numero_cliente, metodo_pago) values (%s, %s, %s, %s)"
        data = (nombre_cliente, direccion_cliente, numero_cliente, metodo_pago)
        cursor.execute(sql, data)
        db.database.commit()
    #return redirect(url_for('catalogo.html'))
        return render_template('catalogo.html' )



#ELIMINAR PEDIDO POR ID
@app.route('/delete/<string:id>' )
def deletePedido(id):
        cursor = db.database.cursor()
        sql = "delete from Pedidos where id=%s "
        data = (id,)
        cursor.execute(sql, data)
        db.database.commit()
        return redirect(url_for('admin.html'))

#EDITAR PEDIDO POR ID
@app.route('/edit/<string:id>', methods=['POST'])
def editPedido(id):
    nombre_cliente = request.form['nombre_cliente']
    direccion_cliente = request.form['direccion_cliente']
    numero_cliente = request.form['numero_cliente']
    #talla = request.form['talla']
    metodo_pago = request.form['metodo_pago']

    if nombre_cliente and direccion_cliente and numero_cliente and metodo_pago:
        cursor = db.database.cursor()
        sql = "update Productos set nombre_cliente= %s, direccion_envio= %s, numero_cliente= %s, metodo_pago= %s where id= %s "
        data = (nombre_cliente, direccion_cliente, numero_cliente, metodo_pago, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('admin.html'))






if __name__ == '__main__':
    app.secret_key = "LuLu"
    app.run(debug=True, port=4000)


    
