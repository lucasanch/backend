from flask import Flask # importamos nuestro framework, en este caso Flask
from flask import render_template, request, redirect,send_from_directory # importamos funcion para permitir el render de los html, tomar valores y redirigir la pagina
from flask_mysqldb import MySQL  # importamos el modulo que permite conectarnos a la base de datos
app = Flask(__name__) # creamos la aplicacion
from datetime import datetime # importar libreria datetime nos permitirá darle nombre de la foto con el horario
import os  #importamos paquetes de interfaz del sistema operativo


# creamos la referencia la host, para que se conecte a la

app.config['MYSQL_HOST']='localhost'  # base de datos MySQL utilizamos el host localhost
app.config['MYSQL_PORT'] = 3307  # cambiar al puerto que tenemos configurados en el xampp
app.config['MYSQL_USER']='root' # indicamos el usuario, por defecto es 'user'
app.config['MYSQL_PASSWORD']=''  # sin contraseña. se puede omitir
app.config['MYSQL_DB']='gastos'  # nombre de nuestra base de datos
mysql = MySQL(app) # creamos la conexion a la base de datos

#guardamos la ruta de la carpeta "uploads" en nuestra app
CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA

# Generamos el acceso a la carpeta uploads.
# El método uploads que creamos nos dirige a la carpeta (variable CARPETA)
# y nos muestra la foto guardada en la variable nombreFoto.
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)


#----------------------------------

@app.route('/')  # ruta raiz del sitio
def index():
# creamos una variable que va a contener la consulta sql 
    sql = "SELECT * FROM `gastos`"
        
    conn = mysql.connect # conectamos a la conexion mysql.init_app(app)
    cursor = conn.cursor() # almacenaremos lo que devuelva la consulta
    cursor.execute(sql) # ejecutamos la sentencia sql
    
    db_gastos = cursor.fetchall()

    print("-"*60)
    
    for gasto in db_gastos:
        print(gasto)
        print("-"*60)
        
    cursor.close()
 
    return render_template('peliculas/index.html', gastos=db_gastos)

#----------------------------------

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect # conectamos a la conexion mysql.init_app(app)
    cursor = conn.cursor() # almacenaremos lo que devuelva la consulta
    cursor.execute("DELETE FROM `gastos` WHERE `ID entrada`=%s", (id,)) # ejecutamos la sentencia
    conn.commit()  # "comiteamos" (cerramos la conexion)
    return redirect('/')


#----------------------------------

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect # conectamos a la conexion mysql.init_app(app)
    cursor = conn.cursor() # almacenaremos lo que devuelva la consulta
    cursor.execute("SELECT * FROM `gastos` WHERE `ID entrada`=%s", (id,)) # ejecutamos la sentencia
    gastos = cursor.fetchall()
    cursor.close()
    return render_template('peliculas/edit.html', gastos=gastos)

#----------------------------------

@app.route('/update', methods=['POST'])  # pagina de almacenamiento de datos del sitio
def update():
# creamos una variable que va recibiendo los valores del formulario y luego pasar a variables local 
    _monto = request.form['txtMonto']
    _fecha = request.form['txtFecha']
    _rubro = request.form['txtRubro']
    _pago = request.form['txtPago']
    _origen = request.form['txtOrigen']
    _foto = request.files['txtFoto']
    _id = request.form['txtID']
  

    conn = mysql.connect # conectamos a la conexion mysql.init_app(app)
    cursor = conn.cursor() # almacenaremos lo que devuelva la consulta
    now = datetime.now() # guardamos los datos de fecha y hora
    
    # actualizacion de campos excepto foto          
    sql = "UPDATE `gastos`.`gastos` SET `Monto`=%s, `Fecha`=%s, `Rubro`=%s, `Forma de pago`=%s, `Origen`=%s WHERE `ID entrada`=%s"
    params = (_monto,_fecha,_rubro,_pago,_origen,_id)
    cursor.execute(sql, params) # ejecutamos la sentencia sql
    
    # actualizacion de la foto si se proporciona una nueva
    if _foto.filename!='':
        tiempo = now.strftime("%Y_%m_%d_%H_%M_") # almacenamos el tiempo como cadena de texto
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)


        
        # consultamos la foto anterior para borrarla del servidor
        cursor.execute("SELECT Foto FROM gastos.gastos WHERE `ID entrada`=%s", (_id,))
        fila = cursor.fetchone()
        if fila and fila[0] is not None:
            nombreFotoAnterior = fila[0]
            rutaFotoAnterior = os.path.join(app.config['CARPETA'],nombreFotoAnterior)
            if os.path.exists(rutaFotoAnterior):
                os.remove(rutaFotoAnterior)         
            
    # actualizamos la base de datos con el nuevo nombre de la foto
    cursor.execute("UPDATE gastos.gastos SET Foto=%s WHERE `ID entrada`=%s", (nuevoNombreFoto, _id))
            
    conn.commit()  # "comiteamos" (cerramos la conexion)
    cursor.close()
    return redirect('/')

#----------------------------------

@app.route('/create')  # pagina del ingreso de datos del sitio
def create():
# creamos una variable que va a contener el ingreso de datos 
    return render_template('peliculas/create.html')

#----------------------------------

@app.route('/store', methods=['POST'])  # pagina de almacenamiento de datos del sitio
def storage():
# creamos una variable que va recibiendo los valores del formulario y luego pasar a variables local 
    _monto = request.form['txtMonto']
    _fecha = request.form['txtFecha']
    _rubro = request.form['txtRubro']
    _pago = request.form['txtPago']
    _origen = request.form['txtOrigen']
    _foto = request.files['txtFoto']

    
    now = datetime.now() # guardamos los datos de fecha y hora
    tiempo = now.strftime("%Y_%m_%d_%H_%M_") # almacenamos el tiempo como cadena de texto
    if _foto.filename!='':
        nuevoNombreFoto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    else:
        nuevoNombreFoto=_foto
        
    datos = (_monto,_fecha,_rubro,_pago,_origen,nuevoNombreFoto)

        
    sql = "INSERT INTO `gastos`.`gastos` (`ID entrada`, `Monto`, `Fecha`, `Rubro`, `Forma de pago`, `Origen`, `Foto`)\
    VALUES (NULL, %s, %s, %s, %s, %s, %s)"
        
    conn = mysql.connect # conectamos a la conexion mysql.init_app(app)
    cursor = conn.cursor() # almacenaremos lo que devuelva la consulta
    cursor.execute(sql, datos) # ejecutamos la sentencia sql
    conn.commit()  # "comiteamos" (cerramos la conexion)
 
    return redirect('/')
    

if __name__=='__main__':
    # corremos la aplicacion en modo debug
    app.run(debug=True)
